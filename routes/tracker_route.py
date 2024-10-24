from flask import Blueprint, request, jsonify
from controllers import tracker_controller as tracker

tracker_route = Blueprint('tracker_route', __name__)

@tracker_route.route('/tracker/all_peer', methods=['GET'])
def get_all_peers():
    peer_list = tracker.get_all_peer_info()
    return jsonify(peer_list), 200 

@tracker_route.route('/tracker/peer/<name>', methods=['GET'])
def get_peer(name):
    peer = tracker.get_peer(name)
    if peer:
        return jsonify(peer), 200
    else:
        return jsonify({"error": "Peer not found"}), 404