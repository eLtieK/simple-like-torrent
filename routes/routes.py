# routes/routes.py
from flask import Blueprint, request, jsonify
from routes import peer_route as peer

def get_all_routes():
    routes = [peer.peer_route]
    return routes 
