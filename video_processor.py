import os
import subprocess
import logging
from config import Config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class VideoProcessor:
    def __init__(self):
        self.video_dir = Config.VIDEO_DIR
        self.cookies_file = "/workspace/cookies/cookies.txt"
        os.makedirs(self.video_dir, exist_ok=True)

    def download_video(self, url, output_filename):
        output_path = os.path.join(self.video_dir, output_filename)
        command = [
            'yt-dlp',
            '--cookies', self.cookies_file,
            '--format', 'mp4',
            '--output', output_path,
            url
        ]
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            logger.debug(result.stdout)
            return os.path.exists(output_path), output_path
        except subprocess.CalledProcessError as e:
            logger.error(e.stderr)
            return False, e.stderr

    def process_video(self, input_file, output_filename, start, end, top_text, bottom_text):
        output_path = os.path.join(self.video_dir, output_filename)
        command = ['ffmpeg', '-i', input_file, '-ss', start, '-to', end, '-c:v', 'libx264', '-c:a', 'aac']
        filters = []

        if top_text:
            filters.append(f"drawtext=text='{top_text}':fontcolor=white:fontsize=24:box=1:boxcolor=black@0.5:x=(w-text_w)/2:y=10")
        if bottom_text:
            filters.append(f"drawtext=text='{bottom_text}':fontcolor=white:fontsize=24:box=1:boxcolor=black@0.5:x=(w-text_w)/2:y=h-th-10")
        if filters:
            command += ['-vf', ",".join(filters)]

        command += ['-y', output_path]

        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            logger.debug(result.stdout)
            return os.path.exists(output_path), output_path
        except subprocess.CalledProcessError as e:
            logger.error(e.stderr)
            return False, e.stderr
