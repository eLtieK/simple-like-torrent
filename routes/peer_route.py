from flask import Blueprint, request, jsonify
from controllers import peer_controller as peer

peer_route = Blueprint('peer_route', __name__)

@peer_route.route('/peer/my_info', methods=['GET'])
def get_my_peer_info():
    ip, port = peer.get_peer_info()
    return f"Đã nhận yêu cầu từ IP: {ip}, Port: {port}"

@peer_route.route('/peer/sign_up', methods=['POST'])
def peer_sign_up():
    # Lấy dữ liệu từ request JSON
    data = request.json

    if not data or 'name' not in data or 'password' not in data:
        return jsonify({"error": "Invalid input, name and password are required"}), 400
    
    name = data['name']
    password = data['password']

    id = peer.sign_up(name, password)

    return jsonify({"message": "Peer signed up successfully", "peer_id": id}), 201

@peer_route.route('/peer/login', methods=['POST'])
def peer_login():
    # Lấy dữ liệu từ request JSON
    data = request.json

    if not data or 'name' not in data or 'password' not in data:
        return jsonify({"error": "Invalid input, name and password are required"}), 400
    
    name = data['name']
    password = data['password']

    valid, id = peer.login(name, password)

    if valid:
         # Nếu peer tồn tại, trả về thông tin
        return jsonify({"message": "Peer found!", "peer": {"id": id}}), 200
    else:
        # Nếu không tìm thấy peer
        return jsonify({"message": "Peer not found!"}), 404
