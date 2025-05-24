#!/bin/bash
set -xe

echo "🟡 Starting YouTube Video Trimmer Setup..."

# Log folder
mkdir -p /workspace/logs
touch /workspace/logs/app.log
exec > >(tee /workspace/logs/app.log) 2>&1

# Install deps
apt-get update -qq
apt-get install -y -qq tzdata git ffmpeg wget unzip python3-pip

# Timezone
ln -fs /usr/share/zoneinfo/Asia/Kolkata /etc/localtime && \
dpkg-reconfigure -f noninteractive tzdata

# Clean old folders
rm -rf /workspace/app /workspace/logs/flask.log

# ✅ Clone public GitHub repo reliably
echo "📦 Cloning public repo..."
git clone https://github.com/ArpitKhurana-ai/VideoEditor.git /workspace/app

# Navigate into app
cd /workspace/app

# Python dependencies
pip install --upgrade pip
pip install flask yt-dlp

# Ensure runtime dirs
mkdir -p /workspace/cookies
touch /workspace/cookies/cookies.txt
mkdir -p static/outputs

# ✅ Launch the Flask app
echo "🚀 Launching Flask app..."
python3 app.py > /workspace/logs/flask.log 2>&1 &
sleep 5

# Show open ports
ss -tulpn | grep LISTEN || true

# Tail logs
tail -f /workspace/logs/app.log /workspace/logs/flask.log
