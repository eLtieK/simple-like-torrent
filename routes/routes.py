# routes/routes.py
from flask import Blueprint, request, jsonify
import controllers.file_management as file_mgmt
import controllers.integrity_check as integrity_check
import controllers.tracker_management as tracker_mgmt
import controllers.peer_management as peer_mgmt
import controllers.downloading as downloading

routes = Blueprint('routes', __name__)

@routes.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    result = file_mgmt.upload_file(file)
    return jsonify(result)

@routes.route('/download', methods=['GET'])
def download():
    file_name = request.args.get('file_name')
    result = file_mgmt.download_file(file_name)
    return jsonify(result)

@routes.route('/register', methods=['POST'])
def register_peer():
    peer_info = request.get_json()
    result = tracker_mgmt.register_peer(peer_info)
    return jsonify(result)

@routes.route('/get_peers', methods=['GET'])
def get_peers():
    file_name = request.args.get('file_name')
    result = tracker_mgmt.get_peers(file_name)
    return jsonify(result)

@routes.route('/start_download', methods=['POST'])
def start_download():
    data = request.get_json()
    result = downloading.start_download(data['peers'], data['file_name'])
    return jsonify(result)