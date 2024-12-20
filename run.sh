#!/bin/bash

# Activate virtual environment if needed (optional)
# Check if venv exists, if not, create it
if [ ! -d "venv" ]; then
    echo "Virtual environment not found, creating..."
    python3 -m venv venv
    echo "Virtual environment created"
fi

source venv/bin/activate
pip install -r requirements.txt

# Run the Flask app
python3 app.py

deactivate