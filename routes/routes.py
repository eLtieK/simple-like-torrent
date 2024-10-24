# routes/routes.py
from routes import peer_route as peer , tracker_route as tracker

def get_all_routes():
    routes = [peer.peer_route, tracker.tracker_route]
    return routes 
