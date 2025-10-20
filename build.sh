#!/usr/bin/env bash
# Render build script for Django + Vite frontend

set -o errexit  # Exit on error

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "🎨 Installing frontend dependencies..."
cd frontend
npm ci
npm run build
cd ..

echo "🎨 Building Tailwind CSS..."
python manage.py tailwind build

echo "📂 Collecting static files..."
python manage.py collectstatic --no-input

echo "✅ Build complete!"
