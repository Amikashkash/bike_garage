#!/bin/bash
echo "==============================================="
echo "  Django Bike Garage - Real-time ASGI Server"
echo "==============================================="
echo ""
echo "IMPORTANT: This runs the ASGI server needed for"
echo "real-time WebSocket functionality."
echo ""
echo "DO NOT use 'python manage.py runserver' for"
echo "real-time features - it has limited WebSocket support."
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "Starting ASGI server on http://localhost:8000"
echo "==============================================="
echo ""

daphne -b 0.0.0.0 -p 8000 garage.asgi:application