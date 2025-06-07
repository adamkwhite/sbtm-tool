#!/bin/bash

# SBTM Tool Stop Script for EC2
# Usage: ./stop.sh

set -e

APP_DIR="/home/ec2-user/sbtm-tool"
PID_FILE="$APP_DIR/sbtm.pid"

echo "🛑 Stopping SBTM Tool..."

# Check if PID file exists
if [ ! -f "$PID_FILE" ]; then
    echo "❌ PID file not found. SBTM Tool may not be running."
    
    # Try to kill any running python processes with main.py
    PIDS=$(pgrep -f "python3 main.py" || true)
    if [ -n "$PIDS" ]; then
        echo "🔍 Found running python3 main.py processes: $PIDS"
        echo "🔪 Killing processes..."
        kill $PIDS
        echo "✅ Processes killed"
    else
        echo "ℹ️  No running SBTM Tool processes found"
    fi
    exit 0
fi

# Read PID from file
PID=$(cat "$PID_FILE")

# Check if process is actually running
if ! ps -p $PID > /dev/null 2>&1; then
    echo "❌ Process $PID is not running. Removing stale PID file."
    rm -f "$PID_FILE"
    exit 0
fi

# Kill the process
echo "🔪 Killing process $PID..."
kill $PID

# Wait for process to stop
echo "⏳ Waiting for process to stop..."
TIMEOUT=10
COUNT=0

while ps -p $PID > /dev/null 2>&1; do
    sleep 1
    COUNT=$((COUNT + 1))
    
    if [ $COUNT -ge $TIMEOUT ]; then
        echo "⚠️  Process didn't stop gracefully. Force killing..."
        kill -9 $PID
        break
    fi
done

# Remove PID file
rm -f "$PID_FILE"

echo "✅ SBTM Tool stopped successfully!"

# Show any remaining python processes (for debugging)
REMAINING=$(pgrep -f "python3 main.py" || true)
if [ -n "$REMAINING" ]; then
    echo "⚠️  Warning: Other python3 main.py processes still running: $REMAINING"
fi