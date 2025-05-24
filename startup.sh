#!/bin/bash
set -xe

echo "🟡 Starting YouTube Video Trimmer Setup..."

# Create log folder and file
mkdir -p /workspace/logs
touch /workspace/logs/app.log
exec > >(tee /workspace/logs/app.log) 2>&1

# Install system dependencies
apt-get update
apt-get install -y tzdata git ffmpeg wget unzip python3-pip

# Set timezone
ln -fs /usr/share/zoneinfo/Asia/Kolkata /etc/localtime && \
dpkg-reconfigure -f noninteractive tzdata

# Create workspace folders
mkdir -p /workspace/app
mkdir -p /workspace/static/outputs
mkdir -p /workspace/cookies

# Download and extract GitHub repo (avoiding GitHub auth issues)
echo "📦 Syncing project code..."
cd /workspace
rm -rf /workspace/app /workspace/video-trimmer-main repo.zip
wget https://github.com/ArpitKhurana-ai/video-trimmer/archive/refs/heads/main.zip -O repo.zip
unzip repo.zip
mv video-trimmer-main app

# Go into app folder
cd /workspace/app

# Install Python dependencies
pip install --upgrade pip
pip install flask yt-dlp

# Ensure cookies.txt exists
touch /workspace/cookies/cookies.txt

# Ensure all paths exist
mkdir -p static/outputs

# Launch Flask app in background
echo "🚀 Launching Flask app..."
python3 app.py > /workspace/logs/flask.log 2>&1 &
sleep 5

# Show open ports
ss -tulpn | grep LISTEN || true

# Tail logs
tail -f /workspace/logs/app.log /workspace/logs/flask.log
