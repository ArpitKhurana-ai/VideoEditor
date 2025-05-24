import os
import logging
from flask import Flask, request, jsonify, make_response, send_from_directory
from validators import validate_input
from video_processor import VideoProcessor
from config import Config

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask
app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
video_processor = VideoProcessor()

# CORS Headers
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

@app.route('/process', methods=['OPTIONS'])
def options_process():
    return make_response('', 200)

@app.route('/process', methods=['POST'])
def process_video():
    data = request.get_json()
    if not data:
        logger.error("No JSON payload provided")
        return jsonify({"status": "error", "message": "Missing request data"}), 400

    is_valid, errors = validate_input(data)
    if not is_valid:
        return jsonify({"status": "error", "message": errors}), 400

    url = data['url']
    start_time = data['start']
    end_time = data['end']
    top_text = data.get('top_text', '')
    bottom_text = data.get('bottom_text', '')
    row_id = data['row_id']

    input_filename = f"{row_id}_input.mp4"
    output_filename = f"{row_id}.mp4"

    input_path = os.path.join(Config.VIDEO_DIR, input_filename)
    output_path = os.path.join(Config.VIDEO_DIR, output_filename)

    try:
        # Step 1: Download
        logger.info(f"Downloading from {url}")
        success, result = video_processor.download_video(url, input_filename)
        if not success:
            return jsonify({"status": "error", "message": result}), 500

        # Step 2: Process
        logger.info(f"Processing {input_filename} into {output_filename}")
        success, result = video_processor.process_video(
            input_path, output_filename, start_time, end_time, top_text, bottom_text
        )
        if not success:
            return jsonify({"status": "error", "message": result}), 500

        # Return link
        return jsonify({
            "status": "success",
            "file": output_filename,
            "url": f"{request.url_root}static/outputs/{output_filename}"
        })

    except Exception as e:
        logger.exception("Unexpected server error")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/static/outputs/<filename>')
def serve_output_file(filename):
    return send_from_directory('static/outputs', filename)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "up"})

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "name": "YouTube Video Trim API",
        "version": "1.0.0",
        "endpoints": {
            "/process": "POST - Trim and generate clip",
            "/static/outputs/<filename>": "GET - Download processed clip",
            "/health": "GET - Health check"
        }
    })

if __name__ == '__main__':
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
