#!/bin/bash
set -e

# Initialize database
echo "Initializing database..."
python init_db.py

# Run application
echo "Starting Flask server..."
exec python run.py
