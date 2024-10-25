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
    
@tracker_route.route('/tracker/uploading', methods=['POST'])
def upload_data():
    # Lấy dữ liệu từ request JSON
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']

    # Kiểm tra xem file có được chọn không
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Kiểm tra xem peer_id có tồn tại trong session hay không
    peer_id = request.cookies.get('peer_id')
    if not peer_id:
        return jsonify({"error": "Bạn cần phải đăng nhập trước khi Upload"}), 401

    # Gọi hàm từ tracker_controller để xử lý dữ liệu tải lên
    result = tracker.upload_file(file, peer_id)

    if result:
        return jsonify({"message": "File uploaded successfully"}), 201
    else:
        return jsonify({"error": "Failed to upload file"}), 500