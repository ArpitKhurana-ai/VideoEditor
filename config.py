import os

class Config:
    VIDEO_DIR = os.path.join("static", "outputs")
    os.makedirs(VIDEO_DIR, exist_ok=True)

    PORT = 8188
    HOST = "0.0.0.0"
    DEBUG = True

    SECRET_KEY = os.environ.get("SESSION_SECRET", "youtube-trim-api")
