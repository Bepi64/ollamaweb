# demo/routing.py

from django.urls import path
from . import consumers

# Définir les URL WebSocket
websocket_urlpatterns = [
        path("ws/chat/<str:pseudo>/<str:model>/", consumers.OllamaChatConsumer.as_asgi()),
]
