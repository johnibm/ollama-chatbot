#!/bin/bash
set -e

echo "📦 Pulling required models..."

ollama pull zephyr:latest || echo "⚠️ Failed to pull zephyr model"
ollama pull mxbai-embed-large || echo "⚠️ Failed to pull embedding model"

# Wait for Ollama to actually be ready to serve models
echo "⏳ Waiting for Ollama server to be ready..."
ollama serve &
OLLAMA_PID=$!

# Poll until the model is available
until curl -s http://localhost:11434/api/tags | grep -q "mxbai-embed-large"; do
  echo "⌛ Waiting for model to register..."
  sleep 2
done

echo "✅ Model is ready."

# Keep the Ollama server running in the foreground
wait $OLLAMA_PID
