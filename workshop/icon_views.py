from django.http import HttpResponse
from django.conf import settings
import os

def app_icon_view(request):
    """
    Serve a simple SVG icon for PWA that includes the logo centered with proper padding
    """
    svg_content = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="512" height="512" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
    <!-- Background circle with theme colors -->
    <defs>
        <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#3b82f6;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#06b6d4;stop-opacity:1" />
        </linearGradient>
    </defs>
    
    <!-- Background -->
    <rect width="512" height="512" rx="128" ry="128" fill="url(#grad1)"/>
    
    <!-- Logo area with proper padding (centered 320x320 area) -->
    <rect x="96" y="96" width="320" height="320" rx="64" ry="64" fill="rgba(255,255,255,0.1)" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
    
    <!-- Text content as fallback -->
    <text x="256" y="200" font-family="Arial, sans-serif" font-size="48" font-weight="bold" text-anchor="middle" fill="white">אופני</text>
    <text x="256" y="280" font-family="Arial, sans-serif" font-size="48" font-weight="bold" text-anchor="middle" fill="white">יקיר</text>
    <text x="256" y="350" font-family="Arial, sans-serif" font-size="24" text-anchor="middle" fill="rgba(255,255,255,0.8)">BIKES</text>
</svg>"""
    
    return HttpResponse(svg_content, content_type='image/svg+xml')
