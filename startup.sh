#!/bin/bash
set -xe

echo "🟡 Starting YouTube Video Trimmer Setup..."

# Create log folder and file
mkdir -p /workspace/logs
touch /workspace/logs/app.log
exec > >(tee /workspace/logs/app.log) 2>&1

# Install system dependencies
apt-get update -qq
apt-get install -y -qq tzdata git ffmpeg wget unzip python3-pip net-tools

# Set timezone
ln -fs /usr/share/zoneinfo/Asia/Kolkata /etc/localtime && \
dpkg-reconfigure -f noninteractive tzdata

# Clean previous broken attempts
rm -rf /workspace/app /workspace/VideoEditor-main /workspace/repo.zip

# Download the correct GitHub ZIP
echo "📦 Syncing project code from VideoEditor..."
cd /workspace
wget https://github.com/ArpitKhurana-ai/VideoEditor/archive/refs/heads/main.zip -O repo.zip
unzip -q repo.zip
mv VideoEditor-main app

# Go into app folder
cd /workspace/app

# Install Python packages
pip install --upgrade pip
pip install flask yt-dlp

# Ensure cookies file and output folder exist
mkdir -p /workspace/cookies
touch /workspace/cookies/cookies.txt
mkdir -p static/outputs

# Launch the app in background
echo "🚀 Launching Flask app..."
python3 app.py > /workspace/logs/flask.log 2>&1 &
sleep 5

# ✅ Install and launch FileBrowser
cd /workspace
wget https://github.com/filebrowser/filebrowser/releases/latest/download/linux-amd64-filebrowser.tar.gz -O fb.tar.gz
tar --no-same-owner -xvzf fb.tar.gz
chmod +x filebrowser
mv filebrowser /usr/local/bin/filebrowser
mkdir -p /workspace/filebrowser
chmod -R 777 /workspace/filebrowser

filebrowser \
  -r /workspace \
  --address 0.0.0.0 \
  -p 8080 \
  -d /workspace/filebrowser/filebrowser.db \
  > /workspace/filebrowser.log 2>&1 &

# Show open ports (using netstat instead of ss)
netstat -tulpn || true

# Tail logs
tail -f /workspace/logs/app.log /workspace/logs/flask.log /workspace/filebrowser.log
