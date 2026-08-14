from flask import Flask, request, render_template_string, send_from_directory
import buat_video
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>StudioShortVideo</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { font-family: sans-serif; max-width: 500px; margin: 20px auto; padding: 0 16px; background: #111; color: #eee; }
    input, button { width: 100%; padding: 12px; margin: 8px 0; font-size: 16px; box-sizing: border-box; }
    input { background: #222; color: #eee; border: 1px solid #444; border-radius: 6px; }
    button { background: #4a7dff; color: white; border: none; border-radius: 6px; cursor: pointer; }
    video { width: 100%; margin-top: 16px; border-radius: 8px; }
    .status { color: #aaa; margin-top: 12px; }
  </style>
</head>
<body>
  <h2>🎬 StudioShortVideo</h2>
  <form method="POST" action="/buat">
    <input name="topik" placeholder="Topik video, misal: Göbekli Tepe" required>
    <input name="durasi" placeholder="Durasi detik, misal: 55" value="55">
    <button type="submit">Buat Video</button>
  </form>
  {% if video %}
    <div class="status">✅ Video jadi!</div>
    <video controls src="/video/{{ video }}"></video>
  {% elif error %}
    <div class="status">❌ Error: {{ error }}</div>
  {% endif %}
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/buat", methods=["POST"])
def buat():
    topik = request.form["topik"]
    durasi = request.form.get("durasi", "55")
    try:
        buat_video.buat_video(topik, durasi)
        return render_template_string(HTML, video="MyComp.mp4")
    except Exception as e:
        return render_template_string(HTML, error=str(e))

@app.route("/video/<filename>")
def video(filename):
    return send_from_directory("out", filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
