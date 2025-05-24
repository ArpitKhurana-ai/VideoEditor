import os
import subprocess
import logging
from config import Config

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class VideoProcessor:
    def __init__(self):
        self.video_dir = Config.VIDEO_DIR

    def download_video(self, url, output_filename):
        """
        Download a YouTube video using yt-dlp
        
        Args:
            url (str): YouTube video URL
            output_filename (str): Filename to save the downloaded video
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Construct the full output path
            output_path = os.path.join(self.video_dir, output_filename)
            
            # Run yt-dlp to download the video
            command = [
                'yt-dlp',
                '--format', 'mp4',
                '--output', output_path,
                url
            ]
            
            logger.debug(f"Running download command: {' '.join(command)}")
            
            # Execute the command
            result = subprocess.run(
                command, 
                check=True,
                capture_output=True,
                text=True
            )
            
            logger.debug(f"Download output: {result.stdout}")
            
            # Check if the file exists after download
            if os.path.exists(output_path):
                logger.info(f"Successfully downloaded video to {output_path}")
                return True, output_path
            else:
                logger.error(f"File not found after download: {output_path}")
                return False, "File not found after download"
                
        except subprocess.CalledProcessError as e:
            logger.error(f"Error downloading video: {e}")
            logger.error(f"Command output: {e.stderr}")
            return False, f"Error downloading video: {e.stderr}"
            
        except Exception as e:
            logger.error(f"Unexpected error in download_video: {str(e)}")
            return False, f"Unexpected error: {str(e)}"

    def process_video(self, input_file, output_file, start_time, end_time, top_text, bottom_text):
        """
        Process the video with ffmpeg to trim and add text overlays
        
        Args:
            input_file (str): Path to the input video file
            output_file (str): Path to save the processed video
            start_time (str): Start time in format HH:MM:SS
            end_time (str): End time in format HH:MM:SS
            top_text (str): Text to overlay at the top of the video
            bottom_text (str): Text to overlay at the bottom of the video
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Build the ffmpeg command for trimming and adding text
            command = [
                'ffmpeg',
                '-i', input_file,
                '-ss', start_time,
                '-to', end_time,
                '-c:v', 'libx264',
                '-c:a', 'aac'
            ]
            
            # Add drawtext filters for overlays if provided
            filter_complex = []
            
            # Add top text if provided
            if top_text:
                top_text_filter = f"drawtext=text='{top_text}':fontcolor=white:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=10"
                filter_complex.append(top_text_filter)
            
            # Add bottom text if provided
            if bottom_text:
                bottom_text_filter = f"drawtext=text='{bottom_text}':fontcolor=white:fontsize=24:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=h-th-10"
                filter_complex.append(bottom_text_filter)
            
            # Add filter complex if we have text overlays
            if filter_complex:
                command.extend(['-vf', ','.join(filter_complex)])
            
            # Output file and overwrite if exists
            command.extend([
                '-y',
                output_file
            ])
            
            logger.debug(f"Running ffmpeg command: {' '.join(command)}")
            
            # Execute the command
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True
            )
            
            logger.debug(f"ffmpeg output: {result.stdout}")
            
            # Check if the output file exists
            if os.path.exists(output_file):
                logger.info(f"Successfully processed video to {output_file}")
                return True, output_file
            else:
                logger.error(f"Output file not found after processing: {output_file}")
                return False, "Output file not found after processing"
                
        except subprocess.CalledProcessError as e:
            logger.error(f"Error processing video: {e}")
            logger.error(f"Command output: {e.stderr}")
            return False, f"Error processing video: {e.stderr}"
            
        except Exception as e:
            logger.error(f"Unexpected error in process_video: {str(e)}")
            return False, f"Unexpected error: {str(e)}"
