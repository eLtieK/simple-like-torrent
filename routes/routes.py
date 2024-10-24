# routes/routes.py
from routes import peer_route as peer , tracker_route as tracker

def get_all_peers_routes():
    routes = [peer.peer_route]
    return routes 

def get_all_tracker_routes():
    routes = [tracker.tracker_route]
    return routes 


