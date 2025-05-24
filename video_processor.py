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

        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        top_text_path = "/workspace/top_text.txt"
        bottom_text_path = "/workspace/bottom_text.txt"

        if top_text:
            with open(top_text_path, "w", encoding="utf-8") as f:
                f.write(top_text)
        if bottom_text:
            with open(bottom_text_path, "w", encoding="utf-8") as f:
                f.write(bottom_text)

        # Resize + center the video
        vf_filter = (
            "scale=1080:-2:force_original_aspect_ratio=decrease,"
            "pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black"
        )

        # Text overlays positioned relative to actual video area (centered)
        if top_text:
            vf_filter += (
                f",drawtext=fontfile='{font_path}':textfile='{top_text_path}':"
                "fontsize=60:fontcolor=white:borderw=2:bordercolor=black:"
                "x=(w-text_w)/2:y=((oh-ih)/2)-80"
            )
        if bottom_text:
            vf_filter += (
                f",drawtext=fontfile='{font_path}':textfile='{bottom_text_path}':"
                "fontsize=60:fontcolor=white:borderw=2:bordercolor=black:"
                "x=(w-text_w)/2:y=((oh+ih)/2)+20"
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
