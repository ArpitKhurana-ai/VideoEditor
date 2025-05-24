#!/bin/bash
set -xe

# Optional: Print working dir
echo "📂 Current Directory: $(pwd)"

# Install OS dependencies (if needed)
apt-get update && \
apt-get install -y ffmpeg git curl unzip

# (Optional) Install yt-dlp
pip install --upgrade pip
pip install yt-dlp flask

# Ensure output folder exists
mkdir -p static/outputs

# Start Flask app
echo "🚀 Launching Flask app..."
python3 app.py > /workspace/app.log 2>&1 &
sleep 3

# Tail logs to keep container alive
tail -f /workspace/app.log
