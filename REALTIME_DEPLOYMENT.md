# Real-time System Deployment Guide

## Overview
Your Django Bike Garage project now has complete real-time functionality using Django Channels and WebSockets.

## Features Implemented

### ✅ Real-time Notifications
- **Customer Progress Updates**: Customers see live progress as mechanics complete repair items
- **Mechanic Assignment Alerts**: Mechanics get instant notifications when assigned new repairs
- **Quality Check Notifications**: Managers receive alerts when repairs are ready for quality checks
- **Stuck Repair Alerts**: Managers get immediate notifications when mechanics report stuck repairs
- **Ready for Pickup**: Customers get celebration notifications when repairs are ready

### ✅ User Role Integration
- **Customer Real-time**: Progress tracking, pickup notifications, repair updates
- **Mechanic Real-time**: Task assignments, completion tracking, stuck repair reporting
- **Manager Real-time**: Live dashboard, quality checks, stuck repair management

### ✅ Technical Implementation
- **Django Channels 4.0**: WebSocket support with automatic reconnection
- **In-Memory Channel Layer**: Development-ready (switch to Redis for production)
- **Model Signals**: Automatic real-time notifications on data changes
- **API Endpoints**: RESTful APIs for JavaScript client integration
- **Role-based WebSocket Groups**: Targeted notifications by user type

## Files Added/Modified

### New Files
```
workshop/consumers.py          # WebSocket consumer for real-time connections
workshop/routing.py            # WebSocket URL routing
workshop/realtime_service.py   # Real-time notification service
workshop/signals.py            # Django model signals for auto-notifications
workshop/api_views.py          # API endpoints for real-time data
workshop/static/js/realtime.js # Base WebSocket client
workshop/static/js/customer-realtime.js # Customer-specific client
workshop/static/js/mechanic-realtime.js # Mechanic-specific client  
workshop/static/js/manager-realtime.js  # Manager-specific client
```

### Modified Files
```
garage/settings.py             # Added Channels configuration
garage/asgi.py                 # ASGI application setup
requirements.txt               # Added channels dependencies
workshop/views.py              # Integrated real-time notifications
workshop/urls.py               # Added API endpoints
workshop/templates/workshop/base.html # Real-time JS integration
workshop/templates/workshop/mechanic_task_completion.html # Real-time features
workshop/templates/workshop/manager_dashboard.html # Real-time dashboard
workshop/templates/workshop/customer_dashboard.html # Real-time panel
```

## Current Configuration (Development)

### Channel Layer: In-Memory
```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}
```

**Limitations**: 
- Single server only
- Data lost on restart
- Perfect for development/testing

## Production Deployment

### 1. Install Redis
```bash
# Ubuntu/Debian
sudo apt install redis-server

# macOS
brew install redis

# Windows
# Download from https://redis.io/download
```

### 2. Update Settings for Production
```python
# garage/settings.py
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}

# Or with Redis URL
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
    },
}
```

### 3. Run with Daphne (ASGI Server)
```bash
# Install Daphne
pip install daphne

# Run ASGI application
daphne -b 0.0.0.0 -p 8000 garage.asgi:application

# With workers (production)
daphne -b 0.0.0.0 -p 8000 --workers 4 garage.asgi:application
```

### 4. Process Manager (Production)
```bash
# Using supervisord
[program:daphne]
command=/path/to/venv/bin/daphne -b 0.0.0.0 -p 8000 garage.asgi:application
directory=/path/to/bike_garage
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
```

### 5. Nginx Configuration
```nginx
upstream bike_garage {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://bike_garage;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /ws/ {
        proxy_pass http://bike_garage;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## Testing Real-time Features

### 1. Customer Flow
1. Login as customer
2. Check dashboard for real-time panel
3. Have manager/mechanic update repair status
4. See instant notifications and progress updates

### 2. Mechanic Flow  
1. Login as mechanic
2. Get assigned repair by manager
3. See instant assignment notification
4. Complete repair items and see real-time progress
5. Report stuck repair if needed

### 3. Manager Flow
1. Login as manager
2. Assign repair to mechanic
3. See mechanic complete tasks in real-time
4. Get quality check alerts
5. Handle stuck repair notifications

## WebSocket URLs

```
ws://localhost:8000/ws/workshop/customer/  # Customer notifications
ws://localhost:8000/ws/workshop/mechanic/  # Mechanic assignments  
ws://localhost:8000/ws/workshop/manager/   # Manager alerts
```

## API Endpoints

```
GET  /api/manager/stats/                    # Manager dashboard stats
GET  /api/customer/active-repairs/          # Customer's active repairs
GET  /api/customer/notifications/           # Customer notification count
GET  /api/customer/notifications/list/      # Customer notification list
POST /api/customer/notifications/mark-read/ # Mark notification read
GET  /api/mechanic/stats/                   # Mechanic statistics
POST /api/mechanic/repair/<id>/stuck/       # Report stuck repair
POST /api/manager/resolve-stuck/<id>/       # Resolve stuck repair
```

## Troubleshooting

### WebSocket Connection Issues
1. Check if Daphne is running
2. Verify WebSocket URL in JavaScript
3. Check browser console for connection errors
4. Ensure user is authenticated

### Redis Connection Issues
1. Verify Redis is running: `redis-cli ping`
2. Check Redis URL in settings
3. Test connection: `python -c "import redis; r=redis.Redis(); print(r.ping())"`

### Signal Issues  
1. Check if signals are imported in apps.py
2. Verify model changes are triggering signals
3. Test realtime_service manually

### Performance Issues
1. Monitor Redis memory usage
2. Check WebSocket connection count
3. Use Redis cluster for high traffic
4. Consider using separate Redis for channels

## Security Considerations

### Authentication
- WebSocket connections require authentication
- Role-based access control enforced
- User type validation in consumers

### Data Validation
- All WebSocket messages validated
- CSRF protection on API endpoints
- SQL injection protection via ORM

### Rate Limiting (Recommended)
```python
# Add to settings.py for production
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
            'capacity': 1500,  # Maximum messages per channel
            'expiry': 60,      # Message expiry time
        },
    },
}
```

## Monitoring

### Recommended Tools
- **Redis monitoring**: RedisInsight, redis-cli
- **WebSocket connections**: Browser DevTools Network tab
- **Django logs**: Standard Django logging
- **Performance**: Django Debug Toolbar, APM tools

### Key Metrics
- Active WebSocket connections
- Message throughput  
- Redis memory usage
- Signal processing time

## Support

For issues or questions about the real-time system:
1. Check browser console for JavaScript errors
2. Verify WebSocket connection status
3. Test API endpoints directly
4. Check Django logs for signal processing
5. Monitor Redis connection and memory

---

🎉 **Congratulations!** Your bike garage now has a complete real-time notification system that will dramatically improve the user experience for customers, mechanics, and managers.