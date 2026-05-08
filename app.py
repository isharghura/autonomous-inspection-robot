from flask import Flask, Response, render_template_string, jsonify
import cv2
import threading
import time
import motors
import sensor
import vision

app = Flask(__name__)

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# shared state
latest_observation = "Waiting for first scan..."
scan_lock = threading.Lock()
scanning = False

# runs in background thread to update VLM observation every 5 seconds
def background_scanner():
    global latest_observation, scanning
    while True:
        time.sleep(20)
        scanning = True
        result = vision.analyze_frame(camera)
        with scan_lock:
            latest_observation = result
        vision.log_observation(result)
        scanning = False


scanner_thread = threading.Thread(target=background_scanner, daemon=True)
scanner_thread.start()

# shared state
latest_observation = "Waiting for first scan..."
scan_lock = threading.Lock()
scanning = False


def background_scanner():
    """Runs in a background thread — scans every 5 seconds."""
    global latest_observation, scanning
    while True:
        time.sleep(5)
        scanning = True
        result = vision.analyze_frame(camera)
        with scan_lock:
            latest_observation = result
        vision.log_observation(result)
        scanning = False


scanner_thread = threading.Thread(target=background_scanner, daemon=True)
scanner_thread.start()

DASHBOARD = """
<!DOCTYPE html>
<html>
<head>
  <title>Inspection Robot</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #0f0f0f;
      color: #e0e0e0;
      font-family: monospace;
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 100vh;
      padding: 20px;
      gap: 16px;
    }
    h1 { font-size: 18px; letter-spacing: 4px; color: #7cf; text-transform: uppercase; }
    #feed {
      border: 1px solid #333;
      border-radius: 6px;
      width: 100%;
      max-width: 640px;
    }
    #status {
      font-size: 13px;
      color: #888;
      display: flex;
      gap: 24px;
    }
    #dist-val { color: #7cf; }
    #action-val { color: #afc; }
    .controls {
      display: grid;
      grid-template-columns: repeat(3, 64px);
      grid-template-rows: repeat(3, 64px);
      gap: 6px;
    }
    .btn {
      background: #1a1a1a;
      border: 1px solid #333;
      border-radius: 6px;
      color: #ccc;
      font-size: 22px;
      cursor: pointer;
      transition: background 0.1s, border-color 0.1s;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .btn:active, .btn.active { background: #1a3a4a; border-color: #7cf; color: #7cf; }
    .btn.stop { grid-column: 2; grid-row: 2; font-size: 14px; color: #f77; border-color: #522; }
    .btn.stop:active { background: #3a1a1a; border-color: #f77; }
    #obs-panel {
      width: 100%;
      max-width: 640px;
      background: #141414;
      border: 1px solid #2a2a2a;
      border-radius: 8px;
      padding: 14px 16px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    #obs-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    #obs-label { font-size: 11px; letter-spacing: 2px; color: #555; text-transform: uppercase; }
    #obs-status { font-size: 11px; color: #555; }
    #obs-status.scanning { color: #fa3; }
    #obs-text { font-size: 13px; color: #ccc; line-height: 1.6; min-height: 40px; }
    #scan-btn {
      align-self: flex-end;
      background: #1a2a1a;
      border: 1px solid #3a5a3a;
      border-radius: 5px;
      color: #7cf;
      font-family: monospace;
      font-size: 12px;
      padding: 6px 14px;
      cursor: pointer;
    }
    #scan-btn:hover { background: #1a3a1a; }
    #scan-btn:disabled { opacity: 0.4; cursor: default; }
    .hint { font-size: 11px; color: #444; }
  </style>
</head>
<body>
  <h1>⬡ Inspection Robot</h1>
  <img id="feed" src="/video_feed" />
  <div id="status">
    <span>Distance: <span id="dist-val">-- cm</span></span>
    <span>Action: <span id="action-val">idle</span></span>
  </div>
  <div class="controls">
    <div></div>
    <button class="btn" onmousedown="cmd('forward')"  onmouseup="cmd('stop')" ontouchstart="cmd('forward')" ontouchend="cmd('stop')">▲</button>
    <div></div>
    <button class="btn" onmousedown="cmd('left')"     onmouseup="cmd('stop')" ontouchstart="cmd('left')"    ontouchend="cmd('stop')">◀</button>
    <button class="btn stop" onmousedown="cmd('stop')" ontouchstart="cmd('stop')">stop</button>
    <button class="btn" onmousedown="cmd('right')"    onmouseup="cmd('stop')" ontouchstart="cmd('right')"   ontouchend="cmd('stop')">▶</button>
    <div></div>
    <button class="btn" onmousedown="cmd('reverse')"  onmouseup="cmd('stop')" ontouchstart="cmd('reverse')" ontouchend="cmd('stop')">▼</button>
    <div></div>
  </div>
  <p class="hint">keyboard: arrow keys to drive · space to stop</p>
  <div id="obs-panel">
    <div id="obs-header">
      <span id="obs-label">🔍 VLM Observation</span>
      <span id="obs-status">auto-scan every 5s</span>
    </div>
    <div id="obs-text">Waiting for first scan...</div>
    <button id="scan-btn" onclick="manualScan()">Scan now</button>
  </div>
  <script>
    function cmd(action) {
      fetch('/cmd/' + action);
      document.getElementById('action-val').textContent = action;
    }
    const keyMap = {
      ArrowUp: 'forward', ArrowDown: 'reverse',
      ArrowLeft: 'left', ArrowRight: 'right', ' ': 'stop'
    };
    document.addEventListener('keydown', e => {
      if (keyMap[e.key]) { e.preventDefault(); cmd(keyMap[e.key]); }
    });
    document.addEventListener('keyup', e => {
      if (keyMap[e.key] && e.key !== ' ') cmd('stop');
    });
    setInterval(() => {
      fetch('/distance').then(r => r.text()).then(d => {
        document.getElementById('dist-val').textContent = d + ' cm';
      }).catch(() => {});
    }, 500);
    setInterval(() => {
      fetch('/observation').then(r => r.json()).then(data => {
        document.getElementById('obs-text').textContent = data.text;
        const statusEl = document.getElementById('obs-status');
        const btnEl = document.getElementById('scan-btn');
        if (data.scanning) {
          statusEl.textContent = '⏳ scanning...';
          statusEl.className = 'scanning';
          btnEl.disabled = true;
        } else {
          statusEl.textContent = 'auto-scan every 5s';
          statusEl.className = '';
          btnEl.disabled = false;
        }
      }).catch(() => {});
    }, 1000);
    function manualScan() {
      document.getElementById('scan-btn').disabled = true;
      document.getElementById('obs-status').textContent = '⏳ scanning...';
      fetch('/scan').then(r => r.json()).then(data => {
        document.getElementById('obs-text').textContent = data.text;
        document.getElementById('obs-status').textContent = 'auto-scan every 5s';
        document.getElementById('scan-btn').disabled = false;
      });
    }
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

@app.route('/observation')
def observation():
    with scan_lock:
        return jsonify({"text": latest_observation, "scanning": scanning})

@app.route('/scan')
def manual_scan():
    global latest_observation, scanning
    scanning = True
    result = vision.analyze_frame(camera)
    with scan_lock:
        latest_observation = result
    vision.log_observation(result)
    scanning = False
    return jsonify({"text": result})


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, threaded=True)
    finally:
        motors.cleanup()