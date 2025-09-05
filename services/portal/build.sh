#!/bin/bash
set -e
# Render build script for Portal service
pip install -r requirements.txt || { echo "Failed to install dependencies"; exit 1; }