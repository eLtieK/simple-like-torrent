# routes/routes.py
from routes import peer_route as peer , tracker_route as tracker

def get_all_routes():
    routes = [tracker.tracker_route, peer.peer_route]
    return routes 


