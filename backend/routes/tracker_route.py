from flask import Blueprint, request, jsonify
from urllib.parse import unquote
from controllers import tracker_controller as tracker, torrent_controller as torrent
from flask_cors import CORS
tracker_route = Blueprint('tracker_route', __name__)
CORS(tracker_route, supports_credentials=True, origins=["http://localhost:3000"])
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
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Nhận peer_id từ formData
    peer_id = request.form.get("peer_id")
    if peer_id is None:
        return jsonify({"error": "Bạn cần phải đăng nhập trước khi Upload"}), 401

    # Gọi hàm từ tracker_controller để xử lý dữ liệu tải lên
    result = tracker.upload_file(file, peer_id)

    if result:
        return jsonify({"message": "File uploaded successfully"}), 201
    else:
        return jsonify({"error": "Failed to upload file"}), 500


'''    
window.addEventListener("beforeunload", () => {
    fetch("/api/peer/set_inactive", {
        method: "POST",
        body: JSON.stringify({ peer_id: "ID_CUA_PEER" }),
        headers: {
            "Content-Type": "application/json"
        }
    });
});
'''    
@tracker_route.route("/tracker/peer/set_inactive", methods=["POST"])
def set_peer_inactive():
    peer_id = request.cookies.get("peer_id")  # Lấy peer_id từ cookie
    if not peer_id:
        return jsonify({"error": "Missing peer_id"}), 400

    result = tracker.set_peer_inactive(peer_id)

    if result.modified_count == 1:
        return jsonify({"message": "Peer status updated to inactive"}), 200
    else:
        return jsonify({"error": "Peer not found or status unchanged"}), 404
      
@tracker_route.route('/tracker/downloading/<encoded_magnet>', methods=['POST'])
def download_data(encoded_magnet):
    magnet_link = unquote(encoded_magnet)
    peer_id = request.cookies.get('peer_id')
    if not peer_id:
        return jsonify({"error": "Bạn cần phải đăng nhập trước khi kết nối tới peer"}), 401

    pieces, output_file = tracker.get_new_piece(magnet_link, peer_id)
    
    # Check the result of the download
    if pieces is None:
        return jsonify({"error": "File does not exist"}), 404
    # If pieces is an empty list, it may mean no data was downloaded
    if not pieces:
        return jsonify({"error": "No data was downloaded"}), 404
    else:
        torrent.combine_pieces(pieces, output_file)
        return jsonify({"message": "File downloaded succesfull"}), 200
    
    