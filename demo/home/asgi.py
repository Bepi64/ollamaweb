"""
ASGI config for demo project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from home.routing import websocket_urlpatterns  # ton fichier routing.py pour les WebSockets
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # pour les requêtes HTTP classiques
    "websocket": AuthMiddlewareStack(  # middleware pour l'authentification WebSocket
        URLRouter(websocket_urlpatterns)  # route les WebSockets vers les consumers
    ),
})
