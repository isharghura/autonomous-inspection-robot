#!/bin/bash
# downloads LLaVA 7B onto the Pi via Ollama
# run this once before starting the robot
# takes a few minutes depending on your connection (~4GB download)

echo "pulling LLaVA 7B model..."
ollama pull llava:7b
echo "done, run: python3 app.py"