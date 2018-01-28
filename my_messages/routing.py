from channels.routing import route_class
from my_messages import consumers

channel_routing = [
    route_class(consumers.websockets),
    # route('websocket.connect', consumers.ws_add),
    # route('websocket.receive', consumers.ws_receive),
    # route('websocket.disconnect', consumers.ws_disconnect),
    ]
