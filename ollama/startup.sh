#!/bin/bash
set -e

# Pull the model you want at startup
ollama pull zephyr:latest
ollama pull mxbai-embed-large

# Start the Ollama server
exec ollama serve
