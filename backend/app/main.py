import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .websocket_manager import manager
from .services.llm_service import get_ai_analysis

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000", # Default React port
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DrawingData(BaseModel):
    imageDataUrl: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the IntelliDraw API"}

@app.post("/analyze")
async def analyze_drawing(data: DrawingData):
    """
    This endpoint receives the drawing from the client,
    sends it to the AI service for analysis, and returns the result.
    """
    analysis = await get_ai_analysis(data.imageDataUrl)
    # Broadcast the analysis to all connected clients
    await manager.broadcast(json.dumps({
        "type": "analysis_result",
        "payload": analysis
    }))
    return {"status": "Analysis complete", "analysis": analysis}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            # Receive drawing data from a client
            data = await websocket.receive_text()

            # Broadcast the drawing data to all other clients
            # This is the core of the real-time collaboration
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"Client #{client_id} disconnected.")
