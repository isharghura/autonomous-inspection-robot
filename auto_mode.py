import time
import motors
import sensor
import vision
import cv2

SAFE_DISTANCE_CM = 25
DRIVE_SPEED      = 60
TURN_SPEED       = 60
SCAN_INTERVAL    = 8  # seconds between VLM scans while driving

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


def run():
    print("autonomous mode started. Ctrl+C to stop.")
    last_scan = 0

    try:
        while True:
            dist = sensor.get_distance_cm()
            now  = time.time()

            if dist is None:
                print("Sensor timeout — stopping")
                motors.stop()
            elif dist > SAFE_DISTANCE_CM:
                print(f"Clear ({dist:.1f} cm) — forward")
                motors.forward(DRIVE_SPEED)
            else:
                print(f"Obstacle at {dist:.1f} cm — avoiding")
                motors.stop()
                time.sleep(0.3)
                motors.reverse(DRIVE_SPEED)
                time.sleep(0.5)
                motors.turn_right(TURN_SPEED)
                time.sleep(0.4)

            # VLM scan on interval
            if now - last_scan >= SCAN_INTERVAL:
                motors.stop()
                print("Scanning with VLM...")
                observation = vision.analyze_frame(camera)
                vision.log_observation(observation)
                print(f"VLM: {observation}")
                last_scan = now

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nStopping.")
    finally:
        motors.cleanup()
        camera.release()


if __name__ == '__main__':
    run()