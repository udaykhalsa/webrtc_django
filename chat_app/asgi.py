import os
import chat.routing
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from channels.auth import AuthMiddlewareStack


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_app.settings')


application = ProtocolTypeRouter({
 'http': get_asgi_application(),

 'websocket': AllowedHostsOriginValidator(
    AuthMiddlewareStack(
      URLRouter(
       chat.routing.websocket_urlpatterns
      )
    )
  )
})
