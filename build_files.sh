#!/bin/bash
echo "=== Step 1: Installing dependencies ==="
python3 -m pip install --break-system-packages -r requirements.txt || python3 -m pip install -r requirements.txt

echo "=== Step 2: Collecting static files ==="
python3 manage.py collectstatic --noinput --clear

echo "=== Step 3: Preparing static output directory for Vercel ==="
mkdir -p staticfiles_build
cp -r staticfiles/* staticfiles_build/ 2>/dev/null || true

echo "=== Step 4: Applying database migrations ==="
python3 manage.py migrate --noinput || echo "Database migration will apply upon request or DB connection."

echo "=== Step 5: Seeding default demo data ==="
python3 manage.py seed_data || echo "Seeding skipped."

echo "=== Build Completed Successfully! ==="
