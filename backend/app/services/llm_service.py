import asyncio
import base64
import json
from io import BytesIO
from typing import Dict, Any

import httpx
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

# ---------------------------
# Model + client initialization
# ---------------------------

# Load BLIP once at import time (do NOT do this inside the function)
# You may want to move this into a startup hook in FastAPI in a real app.
blip_processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)
blip_model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

# URL of your running Ollama server
# - If you're running Ollama locally: "http://localhost:11434/api/generate"
# - If in Docker compose:           "http://ollama:11434/api/generate"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3:8b"  # or whatever model you pulled with `ollama pull`
# e.g. `llava:7b` etc.


# ---------------------------
# Helper functions
# ---------------------------

def _decode_base64_image(image_b64: str) -> Image.Image:
    """
    Takes a base64 *string* (optionally with 'data:image/..;base64,' prefix)
    and returns a PIL Image in RGB mode.
    """
    # Strip data URL header if present
    if "," in image_b64:
        _, image_b64 = image_b64.split(",", 1)

    image_bytes = base64.b64decode(image_b64)
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    return image


def _blip_caption(image: Image.Image) -> str:
    """
    Runs BLIP to generate a caption for the given image.
    """
    inputs = blip_processor(images=image, return_tensors="pt")
    with torch.no_grad():
        caption_ids = blip_model.generate(
            **inputs,
            max_new_tokens=32,
            num_beams=3
        )
    caption = blip_processor.decode(caption_ids[0], skip_special_tokens=True)
    return caption.strip()


async def _ollama_analyze(caption: str, prompt: str) -> Dict[str, Any]:
    """
    Sends the caption + user prompt to Ollama and asks it to return JSON
    with description, tags, confidence_score.
    """
    system_prompt = (
        "You are an image analysis assistant.\n"
        "You will be given an image caption and a user prompt.\n"
        "Return a JSON object with fields:\n"
        "  - description: string\n"
        "  - tags: list of short strings\n"
        "  - confidence_score: float between 0 and 1\n"
        "Respond with *only* valid JSON, no extra text.\n"
    )

    full_prompt = (
        f"{system_prompt}\n\n"
        f"Caption: {caption}\n"
        f"User prompt: {prompt}\n"
        f"JSON:"
    )

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": full_prompt,
            },
            timeout=60.0,
        )
        resp.raise_for_status()
        data = resp.json()

    # Ollama typically returns something like:
    # { "model": "...", "created_at": "...", "response": "....", ... }
    raw_text = data.get("response") or data.get("output", "")

    # Try to parse JSON from the model output
    try:
        parsed = json.loads(raw_text)
        # Basic sanity checks / defaults
        description = str(parsed.get("description", "")).strip()
        tags = parsed.get("tags") or []
        if not isinstance(tags, list):
            tags = [str(tags)]
        confidence = float(parsed.get("confidence_score", 0.7))
    except Exception:
        # Fallback if model doesn't give valid JSON
        description = raw_text.strip() or caption
        tags = []
        confidence = 0.7

    return {
        "description": description,
        "tags": tags,
        "confidence_score": confidence,
    }


# ---------------------------
# Public function
# ---------------------------

async def get_ai_analysis(
    image_b64: str,
    prompt: str = "What is in this image?"
) -> Dict[str, Any]:
    """
    Real implementation of the AI analysis pipeline:

    1. Decode base64 image.
    2. Use BLIP to generate a caption.
    3. Send caption + prompt to Ollama-hosted LLM.
    4. Return structured analysis: { description, tags, confidence_score }.
    """
    print("🤖 AI Service: Received request for analysis...")

    # 1. Decode base64 into PIL image
    image = _decode_base64_image(image_b64)

    # 2. BLIP caption
    caption = _blip_caption(image)
    print(f"🤖 AI Service: BLIP caption -> {caption!r}")

    # 3. Ask LLM (via Ollama) for structured analysis
    analysis = await _ollama_analyze(caption, prompt)

    print("🤖 AI Service: Analysis complete.")
    return analysis
