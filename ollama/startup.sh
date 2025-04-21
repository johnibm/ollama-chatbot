#!/bin/bash
set -e

echo "Pulling models..."
ollama pull zephyr:latest || echo "Failed to pull zephyr model"
ollama pull mxbai-embed-large || echo "Failed to pull embedding model"

echo "Starting Ollama server..."
exec ollama serve
