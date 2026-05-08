import cv2
import base64
import urllib.request
import json
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL      = "moondream:latest"

PROMPT = (
    "You are an inspection robot scanning an indoor room or hallway. "
    "Describe what you see concisely in 1-2 sentences. "
    "Note anything unusual, obstructed, damaged, or out of place. "
    "If the scene looks normal, just say so briefly."
)

# capture a JPEG frame from the camera and return as bytes
def capture_frame(camera: cv2.VideoCapture) -> bytes | None:
    success, frame = camera.read()
    if not success:
        return None
    _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
    return buffer.tobytes()

# capture frame, send to LLaVA via Ollama, return its description
def analyze_frame(camera: cv2.VideoCapture) -> str:
    frame_bytes = capture_frame(camera)
    if frame_bytes is None:
        return "error: could not capture frame from camera"

    image_b64 = base64.b64encode(frame_bytes).decode('utf-8')

    payload = json.dumps({
        "model": MODEL,
        "prompt": PROMPT,
        "images": [image_b64],
        "stream": False
    }).encode('utf-8')

    try:
        req = urllib.request.Request(
            OLLAMA_URL,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            return result.get("response", "No response from model.").strip()
    except Exception as e:
        return f"Vision error: {e}"

# add timestamped observation to the log file
def log_observation(description: str, log_path: str = "inspection_log.txt"):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a") as f:
        f.write(f"[{timestamp}] {description}\n")
