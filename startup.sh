#!/bin/bash
set -xe

# 📁 Setup folders
mkdir -p /workspace/app
cd /workspace/app

# 📄 Redirect logs
mkdir -p /workspace/logs
touch /workspace/logs/app.log
exec > >(tee /workspace/logs/app.log) 2>&1

echo "🟡 Starting YouTube Video Trimmer Setup..."

# 🌐 Basic tools
apt-get update && apt-get install -y tzdata git ffmpeg wget python3-pip

# 🕓 Timezone
ln -fs /usr/share/zoneinfo/Asia/Kolkata /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

# 📦 Install Python dependencies
pip install --upgrade pip
pip install flask yt-dlp

# 📁 Create required folders
mkdir -p static/outputs
mkdir -p cookies

# ⬇️ Download latest code from GitHub
if [ ! -d .git ]; then
  git clone https://github.com/ArpitKhurana-ai/video-trimmer.git /workspace/app
  cd /workspace/app
fi

# ✅ Check required files exist
REQUIRED_FILES=("app.py" "video_processor.py" "config.py" "validators.py")
for file in "${REQUIRED_FILES[@]}"; do
  if [ ! -f "$file" ]; then
    echo "❌ ERROR: Required file missing - $file"
    exit 1
  fi
done

# ✅ Create placeholder cookies.txt if missing
if [ ! -f "cookies/cookies.txt" ]; then
  echo "🔐 Creating empty cookies.txt (you can replace later)"
  touch cookies/cookies.txt
fi

# 🚀 Run Flask app
echo "🚀 Launching Flask App..."
python3 app.py > /workspace/logs/flask.log 2>&1 &

# ✅ Show active ports
ss -tulpn | grep LISTEN || true

# 📄 Show live logs
tail -f /workspace/logs/flask.log
