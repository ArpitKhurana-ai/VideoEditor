import os
import logging
from flask import Flask, request, jsonify, make_response, send_from_directory
from validators import validate_input
from video_processor import VideoProcessor
from config import Config

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# Initialize the video processor
video_processor = VideoProcessor()

# Add CORS headers
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

# Handle OPTIONS requests for CORS preflight
@app.route('/process', methods=['OPTIONS'])
def options_process():
    return make_response('', 200)

@app.route('/process', methods=['POST'])
def process_video():
    data = request.get_json()
    if not data:
        logger.error("No JSON data received")
        return jsonify({"status": "error", "message": "No data provided"}), 400

    # Validate input
    is_valid, errors = validate_input(data)
    if not is_valid:
        logger.error(f"Input validation failed: {errors}")
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
        logger.info(f"Downloading video from {url}")
        download_success, download_result = video_processor.download_video(url, input_filename)
        if not download_success:
            logger.error(f"Failed to download video: {download_result}")
            return jsonify({"status": "error", "message": download_result}), 500

        logger.info(f"Processing video with start={start_time}, end={end_time}")
        process_success, process_result = video_processor.process_video(
            input_path, output_path, start_time, end_time, top_text, bottom_text
        )

        if not process_success:
            logger.error(f"Failed to process video: {process_result}")
            return jsonify({"status": "error", "message": process_result}), 500

        return jsonify({
            "status": "success",
            "file": output_filename,
            "url": f"{request.url_root}static/outputs/{output_filename}"
        })

    except Exception as e:
        logger.exception("Unexpected error during video processing")
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
            "/process": "POST - Process a YouTube video",
            "/health": "GET - Health check",
            "/static/outputs/<filename>": "GET - Download a processed clip"
        }
    })

if __name__ == '__main__':
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
