from channels.routing import ProtocolTypeRouter, URLRouter

from simplechat.main.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'websocket': (
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
