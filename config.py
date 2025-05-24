import os

# Configuration settings for the application
class Config:
    # Directory to store processed videos
    VIDEO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "videos")
    
    # Create the videos directory if it doesn't exist
    os.makedirs(VIDEO_DIR, exist_ok=True)
    
    # Flask settings
    PORT = 8188
    HOST = "0.0.0.0"
    DEBUG = True
    
    # Secret key for Flask sessions (from environment variable or default)
    SECRET_KEY = os.environ.get("SESSION_SECRET", "youtube-trim-api-secret-key")
