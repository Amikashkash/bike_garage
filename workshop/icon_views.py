from django.http import HttpResponse
from django.conf import settings
import os

def app_icon_view(request):
    """
    Serve a beautiful bike-themed SVG icon for PWA
    """
    svg_content = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="512" height="512" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
    <!-- Background with gradient -->
    <defs>
        <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#3b82f6;stop-opacity:1" />
            <stop offset="50%" style="stop-color:#1d4ed8;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#06b6d4;stop-opacity:1" />
        </linearGradient>
        <filter id="glow">
            <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
            <feMerge> 
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
    </defs>
    
    <!-- Background circle -->
    <circle cx="256" cy="256" r="256" fill="url(#grad1)"/>
    
    <!-- Bike icon -->
    <g transform="translate(256,256)" filter="url(#glow)">
        <!-- Left wheel -->
        <circle cx="-100" cy="60" r="45" stroke="#ffffff" stroke-width="6" fill="none" opacity="0.9"/>
        <circle cx="-100" cy="60" r="35" stroke="#ffffff" stroke-width="2" fill="none" opacity="0.7"/>
        <circle cx="-100" cy="60" r="25" stroke="#ffffff" stroke-width="2" fill="none" opacity="0.5"/>
        <circle cx="-100" cy="60" r="15" stroke="#ffffff" stroke-width="2" fill="none" opacity="0.3"/>
        
        <!-- Right wheel -->
        <circle cx="100" cy="60" r="45" stroke="#ffffff" stroke-width="6" fill="none" opacity="0.9"/>
        <circle cx="100" cy="60" r="35" stroke="#ffffff" stroke-width="2" fill="none" opacity="0.7"/>
        <circle cx="100" cy="60" r="25" stroke="#ffffff" stroke-width="2" fill="none" opacity="0.5"/>
        <circle cx="100" cy="60" r="15" stroke="#ffffff" stroke-width="2" fill="none" opacity="0.3"/>
        
        <!-- Frame -->
        <!-- Main triangle -->
        <path d="M -55 60 L 0 -40 L 55 60 Z" stroke="#ffffff" stroke-width="5" fill="none" opacity="0.9"/>
        
        <!-- Top tube -->
        <line x1="0" y1="-40" x2="70" y2="-20" stroke="#ffffff" stroke-width="5" opacity="0.9"/>
        
        <!-- Seat post -->
        <line x1="0" y1="-40" x2="0" y2="-70" stroke="#ffffff" stroke-width="4" opacity="0.9"/>
        
        <!-- Handlebars -->
        <line x1="70" y1="-20" x2="70" y2="-50" stroke="#ffffff" stroke-width="4" opacity="0.9"/>
        <line x1="60" y1="-50" x2="80" y2="-50" stroke="#ffffff" stroke-width="4" opacity="0.9"/>
        
        <!-- Seat -->
        <ellipse cx="0" cy="-75" rx="15" ry="5" fill="#ffffff" opacity="0.9"/>
        
        <!-- Pedals -->
        <circle cx="0" cy="10" r="8" stroke="#ffffff" stroke-width="3" fill="none" opacity="0.8"/>
        <line x1="-6" y1="10" x2="6" y2="10" stroke="#ffffff" stroke-width="2" opacity="0.8"/>
        
        <!-- Chain (simplified) -->
        <circle cx="0" cy="10" r="25" stroke="#ffffff" stroke-width="2" fill="none" opacity="0.4" stroke-dasharray="5,5"/>
    </g>
    
    <!-- Text -->
    <text x="256" y="420" font-family="Arial, sans-serif" font-size="32" font-weight="bold" text-anchor="middle" fill="white" opacity="0.9">אופני יקיר</text>
    <text x="256" y="460" font-family="Arial, sans-serif" font-size="18" text-anchor="middle" fill="rgba(255,255,255,0.7)">BIKE GARAGE</text>
</svg>"""
    
    return HttpResponse(svg_content, content_type='image/svg+xml')
