#!/bin/bash
set -xe

# 1. Update apt and install wget
apt update && apt install -y wget

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Ensure output directories and log file exist
mkdir -p static/outputs
mkdir -p /workspace
touch /workspace/app.log

# 4. Log app start
echo "🚀 Launching Flask app..." | tee -a /workspace/app.log

# 5. Start the Flask app and redirect logs
python3 app.py >> /workspace/app.log 2>&1 &

# 6. Follow logs
tail -f /workspace/app.log
