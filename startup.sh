#!/bin/bash
set -xe

echo "🟡 Starting YouTube Video Trimmer Setup..."

# 📝 Setup logs
mkdir -p /workspace/logs
touch /workspace/logs/app.log
exec > >(tee /workspace/logs/app.log) 2>&1

# 📦 Install required packages
apt-get update -qq
apt-get install -y -qq tzdata git ffmpeg wget unzip python3-pip

# 🌍 Set timezone
ln -fs /usr/share/zoneinfo/Asia/Kolkata /etc/localtime && \
dpkg-reconfigure -f noninteractive tzdata

# 📁 Prepare workspace
mkdir -p /workspace/app
mkdir -p /workspace/static/outputs
mkdir -p /workspace/cookies

# 📥 Download and extract GitHub repo
echo "📦 Syncing project code..."
cd /workspace
rm -rf /workspace/app /workspace/VideoEditor-main repo.zip
wget https://github.com/ArpitKhurana-ai/VideoEditor/archive/refs/heads/main.zip -O repo.zip
unzip -q repo.zip
mv VideoEditor-main app

# ▶️ Go into app
cd /workspace/app

# 🔧 Install Python packages
pip install --upgrade pip
pip install flask yt-dlp

# 📄 Create empty cookies.txt if not present
touch /workspace/cookies/cookies.txt

# 🧱 Ensure all paths exist
mkdir -p static/outputs

# 🚀 Launch Flask app
echo "🚀 Launching Flask app..."
python3 app.py > /workspace/logs/flask.log 2>&1 &
sleep 5

# 🔌 Show open ports
ss -tulpn | grep LISTEN || true

# 📄 Tail logs
tail -f /workspace/logs/app.log /workspace/logs/flask.log
