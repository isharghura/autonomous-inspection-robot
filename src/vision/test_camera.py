import cv2
import time

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

print("Camera opened! Press 'q' to quit. Taking test photo in 3 seconds...")

time.sleep(3)
ret, frame = cap.read()
if ret:
    cv2.imwrite("test_image.jpg", frame)
    print("Saved test_image.jpg")
else:
    print("Failed to capture image")

cap.release()