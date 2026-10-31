#!/bin/bash
echo "Installing requirements..."
python3 -m pip install -r requirements.txt

echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear

echo "Applying migrations..."
python3 manage.py migrate --noinput

echo "Seeding default data..."
python3 manage.py seed_data

echo "Build complete!"
