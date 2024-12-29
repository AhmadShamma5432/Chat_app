import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack
from chat_app.middleware import JwtAuthMiddleware
from django.apps import apps
from django.core.management import call_command
from django.urls import re_path
from chat_app.consumers import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_project.settings')

try:
    call_command('clear_participants')
except Exception as e:
    print(f"Error running startup command: {e}")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": SessionMiddlewareStack(  # Include session middleware
        JwtAuthMiddleware(  # Add JWT middleware
            URLRouter(
                [
                    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
                ]
            )
        )
    ),
})


