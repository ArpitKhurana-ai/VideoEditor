import os
import subprocess
import logging
from config import Config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class VideoProcessor:
    def __init__(self):
        self.video_dir = Config.VIDEO_DIR
        os.makedirs(self.video_dir, exist_ok=True)

    def download_video(self, url, output_filename):
        output_path = os.path.join(self.video_dir, output_filename)
        try:
            command = [
                'yt-dlp',
                '--cookies', Config.COOKIE_PATH,
                '--format', 'mp4',
                '--output', output_path,
                url
            ]
            logger.debug(f"Running yt-dlp: {' '.join(command)}")
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            logger.debug(f"yt-dlp output: {result.stdout}")

            if os.path.exists(output_path):
                logger.info(f"Video downloaded to {output_path}")
                return True, output_path
            else:
                return False, "File not found after download"

        except subprocess.CalledProcessError as e:
            return False, f"yt-dlp error: {e.stderr}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"

    def process_video(self, input_file, output_filename, start_time, end_time, top_text, bottom_text):
        output_path = os.path.join(self.video_dir, output_filename)
        try:
            command = [
                'ffmpeg',
                '-i', input_file,
                '-ss', start_time,
                '-to', end_time,
                '-c:v', 'libx264',
                '-c:a', 'aac'
            ]

            filter_complex = []
            if top_text:
                filter_complex.append(
                    f"drawtext=text='{top_text}':fontcolor=white:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=10"
                )
            if bottom_text:
                filter_complex.append(
                    f"drawtext=text='{bottom_text}':fontcolor=white:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=h-th-10"
                )

            if filter_complex:
                command += ['-vf', ','.join(filter_complex)]

            command += ['-y', output_path]

            logger.debug(f"Running ffmpeg: {' '.join(command)}")
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            logger.debug(f"ffmpeg output: {result.stdout}")

            if os.path.exists(output_path):
                return True, output_path
            else:
                return False, "Output not found"

        except subprocess.CalledProcessError as e:
            return False, f"ffmpeg error: {e.stderr}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
