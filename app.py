from flask import Flask, Response, render_template_string
import cv2
import threading
import motors
import sensor

app = Flask(__name__)
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

DASHBOARD = """
<!DOCTYPE html>
<html>
<head>
<title>Robot Inspector</title>
<style>
  body { background:#111; color:#eee; font-family:sans-serif; text-align:center; margin:0; padding:20px; }
  img  { border: 2px solid #444; border-radius:8px; max-width:100%; }
  .btn { background:#333; color:#eee; border:1px solid #555; border-radius:6px;
         padding:12px 24px; font-size:16px; cursor:pointer; margin:4px; }
  .btn:hover { background:#555; }
  #dist { font-size:18px; margin:10px; color:#7cf; }
</style>
</head>
<body>
  <h2>Inspection Robot</h2>
  <img src="/video_feed" /><br>
  <div id="dist">Distance: -- cm</div>
  <br>
  <button class="btn" onclick="cmd('forward')">▲ Forward</button><br>
  <button class="btn" onclick="cmd('left')">◀ Left</button>
  <button class="btn" onclick="cmd('stop')">■ Stop</button>
  <button class="btn" onclick="cmd('right')">▶ Right</button><br>
  <button class="btn" onclick="cmd('reverse')">▼ Reverse</button>
  <script>
    function cmd(action) { fetch('/cmd/' + action); }
    document.addEventListener('keydown', e => {
      const map = { ArrowUp:'forward', ArrowDown:'reverse',
                    ArrowLeft:'left', ArrowRight:'right', ' ':'stop' };
      if (map[e.key]) { e.preventDefault(); cmd(map[e.key]); }
    });
    document.addEventListener('keyup', () => cmd('stop'));
    setInterval(() => {
      fetch('/distance').then(r=>r.text()).then(d => {
        document.getElementById('dist').textContent = 'Distance: ' + d + ' cm';
      });
    }, 500);
  </script>
</body>
</html>
"""

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' +
               buffer.tobytes() + b'\r\n')

@app.route('/')
def index():
    return render_template_string(DASHBOARD)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cmd/<action>')
def command(action):
    actions = {
        'forward': motors.forward,
        'reverse': motors.reverse,
        'left':    motors.turn_left,
        'right':   motors.turn_right,
        'stop':    motors.stop,
    }
    if action in actions:
        actions[action]()
    return 'ok'

@app.route('/distance')
def distance():
    d = sensor.get_distance_cm()
    return f"{d:.1f}" if d else "timeout"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)