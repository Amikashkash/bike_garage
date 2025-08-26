from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/workshop/(?P<user_type>\w+)/$', consumers.WorkshopConsumer.as_asgi()),
]