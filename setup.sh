#!/usr/bin/env bash

echo "Installing Node.js dependancies..."
npm install

if [ ! -d "my-venv" ]; then
    echo "Creating python virtual environment..."
    python3 -m venv my-venv
fi

echo "Activating environment..."
source my-venv/bin/activate

echo "Installing python dependancies..."
pip install -r requirements.txt

echo "Setup complete!"
