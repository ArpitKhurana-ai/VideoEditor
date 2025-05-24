import os

class Config:
    VIDEO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "outputs")
    COOKIE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cookies", "cookies.txt")
    PORT = 8188
    HOST = "0.0.0.0"
    DEBUG = True
    SECRET_KEY = os.environ.get("SESSION_SECRET", "youtube-trim-api-secret-key")
