from channels.routing import route
from my_messages import old_consumers as consumers

channel_routing = [
    route('websocket.connect', consumers.ws_add),
    route('websocket.receive', consumers.ws_receive),
    route('websocket.disconnect', consumers.ws_disconnect),
    ]
