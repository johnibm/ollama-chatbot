#!/bin/bash
set -e

# Start Ollama in the background
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to be ready
echo "Waiting for Ollama server to be ready..."
until curl -s http://localhost:11434/api/tags > /dev/null; do
  sleep 1
done

# Pull required models
echo "Pulling models..."
ollama pull zephyr:latest || echo "Failed to pull zephyr model"
ollama pull mxbai-embed-large || echo "Failed to pull embedding model"

# Wait until all models appear in the tags
echo "Waiting for models to be ready..."
until curl -s http://localhost:11434/api/tags | grep -q zephyr:latest && curl -s http://localhost:11434/api/tags | grep -q mxbai-embed-large; do
  sleep 1
done

echo "All models are ready. Ollama is now serving."

# Keep foreground process running
wait $OLLAMA_PID
