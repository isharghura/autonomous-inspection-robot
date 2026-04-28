import cv2
import ollama
import base64
from PIL import Image
import io


def capture_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return None

    _, buffer = cv2.imencode(".jpg", frame)
    return buffer.tobytes()


def analyze_with_llm(image_bytes):
    # Convert image to base64 for Ollama vision input
    image = Image.open(io.BytesIO(image_bytes))
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    response = ollama.chat(
        model="llava:phi3",  # replace with your local model if needed
        messages=[
            {
                "role": "user",
                "content": (
                    "You are an autonomous inspection robot. "
                    "Analyze this image for anything unusual, damaged, or defective in an industrial or home setting. "
                    "Check for cracks, leaks, corrosion, missing parts, debris, water stains, heat damage, or anything that appears out of place. "
                    'Be concise and list findings clearly. If nothing is detected, respond with "All clear - no anomalies detected."'
                ),
                "images": [img_str],
            }
        ],
    )

    return response["message"]["content"]


if __name__ == "__main__":
    print("Capturing image and running inspection...")

    img_data = capture_image()
    if img_data is None:
        print("Camera capture failed")
    else:
        result = analyze_with_llm(img_data)
        print("\nInspection report:\n")
        print(result)