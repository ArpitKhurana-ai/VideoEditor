#!/bin/bash
set -xe

echo "🟡 Starting YouTube Video Trimmer Setup..."

# Create log folder and file
mkdir -p /workspace/logs
touch /workspace/logs/app.log
exec > >(tee /workspace/logs/app.log) 2>&1

# Install system dependencies
apt-get update -qq
apt-get install -y -qq tzdata git ffmpeg wget unzip python3-pip

# Set timezone
ln -fs /usr/share/zoneinfo/Asia/Kolkata /etc/localtime && \
dpkg-reconfigure -f noninteractive tzdata

# Clean up previous broken attempts
rm -rf /workspace/app /workspace/videoeditor-* /workspace/VideoEditor-* /workspace/repo.zip

# Download the repo ZIP
echo "📦 Downloading project from GitHub..."
cd /workspace
wget https://github.com/ArpitKhurana-ai/VideoEditor/archive/refs/heads/main.zip -O repo.zip
unzip -q repo.zip

# Dynamically detect extracted folder
EXTRACTED_DIR=$(find . -maxdepth 1 -type d -name 'VideoEditor-*' -o -name 'videoeditor-*' | head -n 1)
echo "📁 Detected extracted folder: $EXTRACTED_DIR"

# Move to /workspace/app
mv "$EXTRACTED_DIR" app

# Go into the app directory
cd /workspace/app

# Install Python dependencies
pip install --upgrade pip
pip install flask yt-dlp

# Ensure cookies and output folders exist
mkdir -p /workspace/cookies
touch /workspace/cookies/cookies.txt
mkdir -p static/outputs

# Launch Flask app
echo "🚀 Launching Flask app..."
python3 app.py > /workspace/logs/flask.log 2>&1 &
sleep 5

# Show open ports
ss -tulpn | grep LISTEN || true

# Tail logs
tail -f /workspace/logs/app.log /workspace/logs/flask.log
