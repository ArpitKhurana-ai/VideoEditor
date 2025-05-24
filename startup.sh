#!/bin/bash
set -xe

echo "🟡 Starting YouTube Video Trimmer Setup..."

# Logging
mkdir -p /workspace/logs
touch /workspace/logs/app.log
exec > >(tee /workspace/logs/app.log) 2>&1

# System Dependencies
apt-get update -qq
apt-get install -y -qq tzdata git ffmpeg wget unzip python3-pip

# Set Timezone
ln -fs /usr/share/zoneinfo/Asia/Kolkata /etc/localtime
dpkg-reconfigure -f noninteractive tzdata

# Clean and Prepare Workspace
cd /workspace
rm -rf /workspace/app /workspace/VideoEditor-main /workspace/repo.zip
mkdir -p /workspace/static/outputs
mkdir -p /workspace/cookies

# ✅ Download repo ZIP (case-sensitive fix)
echo "📦 Downloading repo..."
wget https://github.com/ArpitKhurana-ai/VideoEditor/archive/refs/heads/main.zip -O repo.zip

# ✅ Unzip and move to /workspace/app
echo "📦 Unzipping..."
unzip -q repo.zip
mv -v VideoEditor-main app

# ✅ Move into app folder
cd /workspace/app

# Install Python dependencies
pip install --upgrade pip
pip install flask yt-dlp

# Create cookies file if not present
touch /workspace/cookies/cookies.txt

# Ensure static output directory exists
mkdir -p static/outputs

# ✅ Launch app
echo "🚀 Launching Flask app..."
python3 app.py > /workspace/logs/flask.log 2>&1 &

sleep 5
ss -tulpn | grep LISTEN || true

# ✅ Tail logs
tail -f /workspace/logs/app.log /workspace/logs/flask.log
