from flask import Blueprint, request, jsonify, make_response
from controllers import peer_controller as peer
import threading
import socket

peer_route = Blueprint('peer_route', __name__)

@peer_route.route('/peer/my_info', methods=['GET'])
def get_my_peer_info():
    ip, port = peer.get_peer_info()
    return jsonify({
        "ip_address": ip,
        "port": port
    })

@peer_route.route('/peer/sign_up', methods=['POST'])
def peer_sign_up():
    # Lấy dữ liệu từ request JSON
    data = request.json

    if not data or 'name' not in data or 'password' not in data:
        return jsonify({"error": "Invalid input, name and password are required"}), 400
    
    name = data['name']
    password = data['password']

    ip, port = peer.sign_up(name, password)

    if ip is None and port is None:
        return jsonify({"error": "Name already exists"}), 400
    
    return jsonify({
        "message": "Peer signed up successfully",
        "ip_address": ip,
        "port": port
    }), 201

@peer_route.route('/peer/login', methods=['POST'])
def peer_login():
    # Lấy dữ liệu từ request JSON
    data = request.json

    if not data or 'name' not in data or 'password' not in data:
        return jsonify({"error": "Invalid input, name and password are required"}), 400
    
    name = data['name']
    password = data['password']

    valid, id, ip, port = peer.login(name, password)

    if valid:
         # Nếu peer tồn tại, trả về thông tin
        response = make_response(
        jsonify({ 
            "message": "Peer found",
            "peer_id": id,
            "ip_address": ip,
            "port": port
        }), 201)
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

@peer_route.route('/peer/start_peer', methods=['POST'])
def start_peer():
    peer_id = request.cookies.get('peer_id')
    if not peer_id:
        return jsonify({"error": "Bạn cần phải đăng nhập trước khi Upload"}), 401
    
    ip = request.json['ip_address']
    port = request.json['port']
    thread = threading.Thread(target=run_peer_server, args=(str(ip),int(port),))
    thread.start()
    return jsonify({"status": "Peer server started on port {}".format(port)}), 200

def run_peer_server(ip, port):
    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer_socket.bind((ip, port))
    peer_socket.listen(5)
    
    while True:
        client_socket, addr = peer_socket.accept()
        request = client_socket.recv(1024).decode()
        if request.startswith("REQUEST_PIECE"):
            piece_data = "This is a piece of the file."  # Giả lập dữ liệu
            client_socket.send(piece_data.encode())
        client_socket.close()

@peer_route.route('/peer/connect', methods=['POST'])
def connect_to_peer():
    peer_id = request.cookies.get('peer_id')
    if not peer_id:
        return jsonify({"error": "Bạn cần phải đăng nhập trước khi kết nối tới peer"}), 401

    peer_ip = request.json['ip_address']
    peer_port = request.json['port']
    
    try:
        # Kết nối đến peer server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((peer_ip, peer_port))
            # Gửi yêu cầu lấy piece
            request_message = "REQUEST_PIECE"
            client_socket.send(request_message.encode())
            
            # Nhận dữ liệu piece từ peer
            piece_data = client_socket.recv(1024).decode()
            print(f"Received piece data: {piece_data}")
            
            # Xử lý hoặc lưu trữ dữ liệu nhận được ở đây
            return jsonify({"status": "Received piece data", "data": piece_data}), 200

    except ConnectionRefusedError:
        return jsonify({"error": "Không thể kết nối đến peer, vui lòng kiểm tra địa chỉ IP và port."}), 404
    except Exception as e:
        return jsonify({"error": f"Đã xảy ra lỗi: {str(e)}"}), 500