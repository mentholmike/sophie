#!/bin/bash
# Pre-session GitHub sync - pulls latest before OpenClaw loads workspace

cd ~/.openclaw/workspace || exit 1

# Pull latest from GitHub (non-destructive, only updates local)
git fetch origin main
git checkout -f main
git pull -f origin main

# Exit cleanly
exit 0
