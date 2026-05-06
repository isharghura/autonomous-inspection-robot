import time
import motors
import sensor

SAFE_DISTANCE_CM = 25

def run():
    print("autonomous mode started. Ctrl+C to stop.")
    try:
        while True:
            dist = sensor.get_distance_cm()
            print(f"distance: {dist:.1f} cm" if dist else "sensor timeout")

            if dist is None or dist > SAFE_DISTANCE_CM:
                motors.forward(60)
            else:
                motors.stop()
                time.sleep(0.3)
                motors.reverse(60)
                time.sleep(0.5)
                motors.turn_right(60)
                time.sleep(0.4)

            time.sleep(0.05)
    except KeyboardInterrupt:
        print("stopping.")
        motors.cleanup()

if __name__ == '__main__':
    run()