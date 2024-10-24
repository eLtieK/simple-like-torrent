from flask import Blueprint, request, jsonify
from controllers import tracker_controller as tracker

tracker_route = Blueprint('tracker_route', __name__)

@tracker_route.route('/tracker/all_peer', methods=['GET'])
def get_all_peers():
    peer_list = tracker.get_all_peer_info()
    return jsonify(peer_list), 200 