from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import graphql_api.routing
import ws.routing


application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            ws.routing.websocket_urlpatterns + graphql_api.routing.websocket_urlpatterns
        )
    ),
})
