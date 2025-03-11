#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Kokoro Dictate
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🗣️

# Documentation:

cd /Users/your_path_here/Kokoro-Server/Kokoro-FastAPI
/opt/homebrew/bin/uv run dictation_hotkey.py
