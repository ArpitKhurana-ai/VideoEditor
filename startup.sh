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

# Clean previous app folders to avoid folder name conflicts
cd /workspace
rm -rf /workspace/app /workspace/VideoEditor-main repo.zip

# Download repo zip and extract
echo "📦 Downloading code from GitHub..."
wget https://github.com/ArpitKhurana-ai/VideoEditor/archive/refs/heads/main.zip -O repo.zip
unzip -q repo.zip
mv VideoEditor-main app

# Go into app directory
cd /workspace/app

# Install Python packages
pip install --upgrade pip
pip install flask yt-dlp

# Ensure folders exist
mkdir -p static/outputs
mkdir -p /workspace/cookies
touch /workspace/cookies/cookies.txt

# Launch Flask app in background
echo "🚀 Launching Flask app..."
python3 app.py > /workspace/logs/flask.log 2>&1 &
sleep 5

# Show open ports
ss -tulpn | grep LISTEN || true

# Tail logs
tail -f /workspace/logs/app.log /workspace/logs/flask.log
