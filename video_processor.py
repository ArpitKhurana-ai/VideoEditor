import os
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class VideoProcessor:
    def __init__(self):
        self.video_dir = os.path.join("static", "outputs")
        os.makedirs(self.video_dir, exist_ok=True)

    def download_video(self, url, output_filename):
        """
        Download a YouTube video using yt-dlp
        """
        try:
            output_path = os.path.join(self.video_dir, output_filename)

            command = [
                'yt-dlp',
                '--format', 'mp4',
                '--output', output_path,
                url
            ]

            logger.debug(f"Running download command: {' '.join(command)}")
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            logger.debug(f"Download output: {result.stdout}")

            if os.path.exists(output_path):
                logger.info(f"Downloaded video to {output_path}")
                return True, output_path
            else:
                logger.error(f"File not found: {output_path}")
                return False, "File not found after download"

        except subprocess.CalledProcessError as e:
            logger.error(f"Download error: {e.stderr}")
            return False, f"Download error: {e.stderr}"

        except Exception as e:
            logger.error(f"Unexpected error in download_video: {str(e)}")
            return False, f"Unexpected error: {str(e)}"

    def process_video(self, input_file, output_filename, start_time, end_time, top_text, bottom_text):
        """
        Trim the video and overlay text using ffmpeg
        """
        try:
            output_path = os.path.join(self.video_dir, output_filename)

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
                top_text_filter = f"drawtext=text='{top_text}':fontcolor=white:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=10"
                filter_complex.append(top_text_filter)

            if bottom_text:
                bottom_text_filter = f"drawtext=text='{bottom_text}':fontcolor=white:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=h-th-10"
                filter_complex.append(bottom_text_filter)

            if filter_complex:
                command += ['-vf', ','.join(filter_complex)]

            command += ['-y', output_path]

            logger.debug(f"Running ffmpeg command: {' '.join(command)}")
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            logger.debug(f"ffmpeg output: {result.stdout}")

            if os.path.exists(output_path):
                logger.info(f"Processed video saved to {output_path}")
                return True, output_path
            else:
                logger.error(f"Output not found: {output_path}")
                return False, "Output not found after processing"

        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg error: {e.stderr}")
            return False, f"FFmpeg error: {e.stderr}"

        except Exception as e:
            logger.error(f"Unexpected error in process_video: {str(e)}")
            return False, f"Unexpected error: {str(e)}"
