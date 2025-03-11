#!/bin/bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y \
    libsoup-3.0-0 \
    libgstgl1.0-0 \
    libgstcodecparsers-1.0-0 \
    libenchant-2-2 \
    libsecret-1-0 \
    libmanette-0.2-0 \
    libgles2 \
    libegl1

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
playwright install-deps
