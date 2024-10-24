from flask import Blueprint, request, jsonify, make_response
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
        # Tạo response và đặt cookie
        response = make_response(jsonify({"message": "Peer found!", "peer_id": id}), 200)
        response.set_cookie('peer_id', id, httponly=True)
        return response
    else:
        # Nếu không tìm thấy peer
        return jsonify({"message": "Peer not found!"}), 404

@peer_route.route('/peer/protected', methods=['GET'])
def protected():
    peer_id = request.cookies.get('peer_id')

    if not peer_id:
        return jsonify({"error": "Peer ID is missing!"}), 403

    return jsonify({"message": "Protected route accessed!", "peer_id": peer_id}), 200