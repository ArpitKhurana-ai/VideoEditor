#!/bin/bash
set -xe

echo "🟡 Starting YouTube Video Trimmer Setup..."

# Create log folder and file
mkdir -p /workspace/logs
touch /workspace/logs/app.log
exec > >(tee /workspace/logs/app.log) 2>&1

# Install system dependencies
apt-get update
apt-get install -y tzdata git ffmpeg wget python3-pip

# Set timezone
ln -fs /usr/share/zoneinfo/Asia/Kolkata /etc/localtime && \
dpkg-reconfigure -f noninteractive tzdata

# Create workspace folders
mkdir -p /workspace/app
mkdir -p /workspace/static/outputs
mkdir -p /workspace/cookies

# Clone GitHub repo into a clean folder
if [ -d "/workspace/app/.git" ]; then
    echo "✅ Git repo already exists. Pulling latest changes..."
    cd /workspace/app && git pull
else
    echo "⬇️ Cloning repo..."
    git clone https://github.com/ArpitKhurana-ai/video-trimmer.git /workspace/app
fi

# Go into app folder
cd /workspace/app

# Install Python dependencies
pip install --upgrade pip
pip install flask yt-dlp

# Create placeholder cookies file if not present
touch /workspace/cookies/cookies.txt

# Ensure all paths exist
mkdir -p static/outputs

# Launch Flask app in background
echo "🚀 Launching Flask app..."
python3 app.py > /workspace/logs/flask.log 2>&1 &
sleep 5

# Print open ports
ss -tulpn | grep LISTEN || true

# Tail logs
tail -f /workspace/logs/app.log /workspace/logs/flask.log
