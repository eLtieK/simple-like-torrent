from flask import Blueprint, request, jsonify, session
from controllers import tracker_controller as tracker

tracker_route = Blueprint('tracker_route', __name__)

@tracker_route.route('/tracker/all_peer', methods=['GET'])
def get_all_peers():
    peer_list = tracker.get_all_peer_info()
    return jsonify(peer_list), 200 

@tracker_route.route('/tracker/uploading', methods=['POST'])
def upload_data():
    # Lấy dữ liệu từ request JSON
    data = request.json

    if not data or 'file_name' not in data or 'file_content' not in data:
        return jsonify({"error": "Invalid input, file_name and file_content are required"}), 400
    
    file_name = data['file_name']
    file_content = data['file_content']

    # Kiểm tra xem peer_id có tồn tại trong session hay không
    peer_id = request.cookies.get('peer_id')
    if not peer_id:
        return jsonify({"error": "Bạn cần phải đăng nhập trước khi Upload"}), 401

    # Gọi hàm từ tracker_controller để xử lý dữ liệu tải lên
    result = tracker.upload_file(file_name, file_content, peer_id)

    if result:
        return jsonify({"message": "File uploaded successfully"}), 201
    else:
        return jsonify({"error": "Failed to upload file"}), 500