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

        # Font that supports emojis
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

        # Base padding and scaling filter
        vf_filter = (
            "scale=1080:-2:force_original_aspect_ratio=decrease,"
            "pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black"
        )

        # Add top text
        if top_text:
            vf_filter += (
                f",drawtext=fontfile='{font_path}':text='{top_text}':"
                "fontsize=60:fontcolor=white:borderw=2:bordercolor=black:"
                "x=(w-text_w)/2:y=100:escape=1"
            )

        # Add bottom text
        if bottom_text:
            vf_filter += (
                f",drawtext=fontfile='{font_path}':text='{bottom_text}':"
                "fontsize=60:fontcolor=white:borderw=2:bordercolor=black:"
                "x=(w-text_w)/2:y=h-th-100:escape=1"
            )

        command = [
            'ffmpeg',
            '-ss', start,
            '-to', end,
            '-i', input_file,
            '-vf', vf_filter,
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-y', output_path
        ]

        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            logger.debug(result.stdout)
            return os.path.exists(output_path), output_path
        except subprocess.CalledProcessError as e:
            logger.error(e.stderr)
            return False, e.stderr
