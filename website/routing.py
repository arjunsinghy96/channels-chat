from channels.routing import route_class
from website import consumers

channel_routing = [
    route_class(consumers.websockets, path='^/chat/(?P<room>[-\w]+)/$'),
    route_class(consumers.dashboardWebsockets, path='^/dashboard/$'),
    route_class(consumers.leagueWebsockets, path='^/league/(?P<id>[0-9]+)/details/$'),
    ]