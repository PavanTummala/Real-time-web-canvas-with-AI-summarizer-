import cv2
import numpy as np
import base64
import re

def process_image_data(image_data_url: str) -> np.ndarray:
    """
    Decodes a Data URL and converts it into an OpenCV image.
    """
    try:
        # Split the metadata from the base64 string
        header, encoded = image_data_url.split(",", 1)
        # Decode the base64 string
        decoded = base64.b64decode(encoded)
        # Convert the binary data to a NumPy array
        image = np.frombuffer(decoded, dtype=np.uint8)
        # Decode the NumPy array into an OpenCV image
        image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)
        return image
    except Exception as e:
        print(f"Error processing image data url: {e}")
        return None

def find_drawn_object(image: np.ndarray) -> str:
    """
    A placeholder function to simulate object detection.
    In a real application, this would involve more sophisticated
    OpenCV techniques (e.g., contour detection, template matching)
    or a call to a vision model.
    """
    # For now, let's just return a mock analysis.
    # We could do some simple analysis, like counting non-white pixels.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        # A simple heuristic: if there are contours, something was drawn.
        return "An interesting shape has been drawn!"
    else:
        return "The canvas is empty."
