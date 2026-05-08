#!/bin/bash
# downloads model onto the Pi via Ollama
# run this once before starting the robot
# takes a few minutes depending on your connection (~4GB download)

echo "pulling model..."
ollama pull moondream
echo "done, run: python3 app.py"