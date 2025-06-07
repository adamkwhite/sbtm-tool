#!/bin/bash

# SBTM Tool Start Script for EC2
# Usage: ./start.sh

set -e

APP_DIR="/home/ec2-user/sbtm-tool"
PID_FILE="$APP_DIR/sbtm.pid"
LOG_FILE="$APP_DIR/sbtm.log"

echo "🚀 Starting SBTM Tool..."

# Check if already running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null 2>&1; then
        echo "❌ SBTM Tool is already running (PID: $PID)"
        exit 1
    else
        echo "🧹 Removing stale PID file"
        rm -f "$PID_FILE"
    fi
fi

# Change to application directory
cd "$APP_DIR"

# Start the application in background
echo "📁 Starting from: $APP_DIR"
echo "📝 Logging to: $LOG_FILE"

HOST=0.0.0.0 PORT=8080 nohup python3 main.py > "$LOG_FILE" 2>&1 &

# Save PID
echo $! > "$PID_FILE"

# Wait a moment to check if it started successfully
sleep 3

PID=$(cat "$PID_FILE")
if ps -p $PID > /dev/null 2>&1; then
    echo "✅ SBTM Tool started successfully!"
    echo "🆔 PID: $PID"
    echo "🌐 URL: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8080"
    echo "📊 Health: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8080/health"
    echo "📝 Logs: tail -f $LOG_FILE"
else
    echo "❌ Failed to start SBTM Tool"
    echo "📝 Check logs: cat $LOG_FILE"
    rm -f "$PID_FILE"
    exit 1
fi