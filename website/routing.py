from channels.routing import route_class
from website import consumers

channel_routing = [
    route_class(consumers.websockets),
    ]