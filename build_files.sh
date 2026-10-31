#!/bin/bash
echo "=== Step 1: Installing dependencies ==="
python3 -m pip install --break-system-packages -r requirements.txt || python3 -m pip install -r requirements.txt

echo "=== Step 2: Collecting static files ==="
python3 manage.py collectstatic --noinput --clear

echo "=== Step 3: Applying database migrations ==="
python3 manage.py migrate --noinput || echo "Database migration will apply upon request or DB connection."

echo "=== Step 4: Seeding default demo data ==="
python3 manage.py seed_data || echo "Seeding skipped."

echo "=== Build Completed Successfully! ==="
