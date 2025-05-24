#!/bin/bash
set -xe

# 1. Update and install wget if missing
apt update && apt install -y wget

# 2. Install Python requirements
pip install -r VideoEditor/requirements.txt

# 3. Create required folders and log file
mkdir -p /workspace
touch /workspace/app.log
mkdir -p VideoEditor/static/outputs

# 4. Log message
echo "🚀 Launching Flask app..." | tee -a /workspace/app.log

# 5. Change to repo directory
cd VideoEditor

# 6. Start app with logging
python3 app.py >> /workspace/app.log 2>&1 &

# 7. Tail logs
tail -f /workspace/app.log
