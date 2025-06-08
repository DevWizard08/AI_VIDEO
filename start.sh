#!/bin/bash

set -e

echo "🔊 Starting OpenTTS server on port 5004..."

# Start OpenTTS in the background
python3 -m TTS.server.server --port 5004 > opentts.log 2>&1 &

TTS_PID=$!

# Wait for TTS to start (check if port 5004 is open)
echo "⏳ Waiting for OpenTTS to be ready..."
RETRY=0
until nc -z localhost 5004 || [ $RETRY -eq 30 ]; do
  echo "⏳ OpenTTS not ready yet... ($RETRY)"
  RETRY=$((RETRY + 1))
  sleep 1
done

if nc -z localhost 5004; then
  echo "✅ OpenTTS is up!"
else
  echo "❌ OpenTTS failed to start"
  exit 1
fi

# Start Flask app
echo "🚀 Starting Flask app on port 5000..."
python3 app.py
