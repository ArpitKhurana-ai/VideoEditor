#!/bin/bash
set -xe

echo "🟡 Starting YouTube Video Trimmer Setup..."

# Setup logs
mkdir -p /workspace/logs
touch /workspace/logs/app.log
exec > >(tee /workspace/logs/app.log) 2>&1

# Install required packages (incl. unzip early)
apt-get update -qq
apt-get install -y -qq tzdata git ffmpeg wget unzip python3-pip

# Set timezone
ln -fs /usr/share/zoneinfo/Asia/Kolkata /etc/localtime && \
dpkg-reconfigure -f noninteractive tzdata

# Prepare workspace
mkdir -p /workspace/static/outputs /workspace/cookies
cd /workspace
rm -rf /workspace/app /workspace/VideoEditor-main repo.zip

# ✅ Download and unzip
echo "📦 Downloading GitHub repo..."
wget https://github.com/ArpitKhurana-ai/VideoEditor/archive/refs/heads/main.zip -O repo.zip

echo "📦 Extracting zip..."
unzip -q repo.zip || { echo "❌ Failed to unzip repo.zip"; exit 1; }

# ✅ Verify extraction
if [ ! -d "VideoEditor-main" ]; then
    echo "❌ ERROR: Extracted folder 'VideoEditor-main' not found."
    ls -la
    exit 1
fi

mv VideoEditor-main app
cd /workspace/app

# Python deps
pip install --upgrade pip
pip install flask yt-dlp

# Placeholder
touch /workspace/cookies/cookies.txt
mkdir -p static/outputs

# Launch app
echo "🚀 Launching Flask app..."
python3 app.py > /workspace/logs/flask.log 2>&1 &
sleep 5

# Ports info
ss -tulpn | grep LISTEN || true

# Logs
tail -f /workspace/logs/app.log /workspace/logs/flask.log
