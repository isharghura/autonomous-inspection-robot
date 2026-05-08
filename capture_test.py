import cv2
import os
import time

# output folder
SAVE_DIR = "imgs"

def main():
    # create folder if it doesn't exist
    os.makedirs(SAVE_DIR, exist_ok=True)

    # open camera
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("error: no camera")
        return

    # give camera time to warm up
    time.sleep(1)

    # capture frame
    ret, frame = cam.read()

    if not ret:
        print("error: failed to capture image")
        cam.release()
        return

    # filename with timestamp
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"{SAVE_DIR}/img_{timestamp}.jpg"

    # save image
    cv2.imwrite(filename, frame)

    print(f"saved image to {filename}")

    # cleanup
    cam.release()

if __name__ == "__main__":
    main()