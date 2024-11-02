import base64
from models import torrents, file, peer
from bson import ObjectId
import hashlib
import os

def decode_magnet_link(magnet_link):
    # Kiểm tra xem magnet link có bắt đầu bằng 'magnet:?xt=urn:btih:' không
    if not magnet_link.startswith("magnet:?xt=urn:btih:"):
        return None

    # Tách phần info_hash ngay sau 'magnet:?xt=urn:btih:'
    info_hash = magnet_link[20:]  # Bỏ qua 'magnet:?xt=urn:btih:'
    
    # Đảm bảo info_hash có độ dài hợp lệ (thường là 40 ký tự hex cho SHA-1 hash)
    if len(info_hash) != 40:
        return None
    
    return info_hash

def get_torrent(magnet_link):
    info_hash = decode_magnet_link(magnet_link)
    collection = torrents.torrent_collection()

    torrent_data = collection.find_one({
        "info_hash": info_hash
    })

    return torrent_data

def get_pieces_idx(torrent):
    length = torrent["info"]["length"]
    piece_length = torrent["info"]["piece length"]
    # Tính số lượng piece
    num_pieces = length // piece_length
    
    # Nếu còn dữ liệu dư sau khi chia, tăng số lượng piece lên 1
    if length % piece_length > 0:
        num_pieces += 1
    # Tạo mảng các index
    return list(range(num_pieces))

def get_available_pieces(peer_id, torrent):
    collection = peer.peer_collection()
    metainfo_id = str(torrent["_id"])
    
    # Tìm kiếm thông tin peer theo peer_id
    peer_info = collection.find_one({
        "_id": ObjectId(peer_id)
    })
    
    # Nếu không tìm thấy peer, trả về danh sách rỗng
    if peer_info is None:
        return []

    # Mảng để lưu trữ các index của các piece đã có
    available_indices = []
    piece_info = peer_info["piece_info"]
    # Kiểm tra xem peer có piece_info không
    for piece in piece_info:
        for p in piece:
            # So sánh metainfo_id và lưu index nếu nó khớp
            if str(p["metainfo_id"]) == metainfo_id:
                available_indices.append(p["index"])

    return available_indices

def get_peer_list(torrent):
    file_collection = file.file_collection()
    peer_collection = peer.peer_collection()

    torrent_id = str(torrent["_id"])
    
     # Truy vấn collection để lấy danh sách peer cho torrent_id
    file_data = file_collection.find_one({
        "metainfo_id": ObjectId(torrent_id)
    })
    peer_data = file_data["peers_info"]
    # Duyệt qua các peer_data và thêm vào danh sách peer_list
    peer_list = []
    for p in peer_data:
        peer_info = peer_collection.find_one({
            "_id": ObjectId(str(p["peer_id"])),
            "status": "active"
        })

        if peer_info is None:
            continue

        peer_new_info = {
            "peer_id": str(peer_info["_id"]),
            "ip_address": peer_info["ip_address"],
            "port": peer_info["port"]
        }
        peer_list.append(peer_new_info)

    return peer_list

# Mã hóa danh sách các mảng byte thành Base64
def encode_list_to_base64(byte_list):
    return [base64.b64encode(piece).decode('utf-8') for piece in byte_list]

# Giải mã danh sách Base64 về các mảng byte
def decode_list_from_base64(base64_list):
    return [base64.b64decode(b64_str) for b64_str in base64_list]

def combine_pieces(pieces, output_file_name):
    pieces = decode_list_from_base64(pieces)
    if not os.path.exists("C:\\Downloads"):
        os.makedirs("C:\\Downloads")
    output_file_path = os.path.join("C:\\Downloads", output_file_name)
    with open(output_file_path, 'wb') as outfile:
        for piece in pieces:
            outfile.write(piece)

    print(f"File downloaded successfully to {output_file_path}")
