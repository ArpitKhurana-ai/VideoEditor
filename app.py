import os
import logging
from flask import Flask, request, jsonify, make_response, send_from_directory
from validators import validate_input
from video_processor import VideoProcessor
from config import Config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

video_processor = VideoProcessor()

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

@app.route('/')
def index():
    return jsonify({
        "message": "✅ YouTube Trimmer Flask API is running.",
        "status": "ok",
        "docs": "/process",
        "health_check": "/health"
    })

@app.route('/process', methods=['POST', 'OPTIONS'])
def process_video():
    if request.method == 'OPTIONS':
        return make_response('', 200)

    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400

    is_valid, errors = validate_input(data)
    if not is_valid:
        return jsonify({"status": "error", "message": errors}), 400

    url = data['url']
    start = data['start']
    end = data['end']
    top = data.get('top_text', '')
    bottom = data.get('bottom_text', '')
    row_id = data['row_id']

    input_name = f"{row_id}_input.mp4"
    output_name = f"{row_id}.mp4"
    input_path = os.path.join(Config.VIDEO_DIR, input_name)
    output_path = os.path.join(Config.VIDEO_DIR, output_name)

    success, path = video_processor.download_video(url, input_name)
    if not success:
        return jsonify({"status": "error", "message": path}), 500

    success, result = video_processor.process_video(
        input_path, output_name, start, end, top, bottom
    )
    if not success:
        return jsonify({"status": "error", "message": result}), 500

    return jsonify({
        "status": "success",
        "url": f"{request.url_root}static/outputs/{output_name}"
    })

@app.route('/static/outputs/<filename>')
def serve_clip(filename):
    return send_from_directory('static/outputs', filename)

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    logger.info(f"Starting Flask app on http://{Config.HOST}:{Config.PORT}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
