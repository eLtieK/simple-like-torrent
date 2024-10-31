import base64
from models import torrents, file, peer
from bson import ObjectId
import hashlib

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
        # So sánh metainfo_id và lưu index nếu nó khớp
        if str(piece["metainfo_id"]) == metainfo_id:
            available_indices.append(piece["index"])

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
            "_id": ObjectId(str(p["peer_id"]))
        })
        peer_new_info = {
            "peer_id": str(peer_info["_id"]),
            "ip_address": peer_info["ip_address"],
            "port": peer_info["port"]
        }
        peer_list.append(peer_new_info)

    return peer_list

def get_piece_hash_from_torrent(torrent_data, piece_index):
    # Truy cập trường pieces được mã hóa base64 trong torrent data
    pieces_base64 = torrent_data['info']['pieces']['$binary']['base64']
    
    # Giải mã base64 thành dữ liệu nhị phân
    pieces_binary = base64.b64decode(pieces_base64)
    
    # Mỗi hash SHA-1 có độ dài 20 byte
    piece_length = 20  
    start = piece_index * piece_length
    end = start + piece_length
    # Trả về hash của piece tương ứng
    return pieces_binary[start:end]

def verify_piece(piece_data, pieces_base64, piece_index):
    # Tính hash SHA-1 của piece tải về từ peer
    piece_hash = hashlib.sha1(piece_data).digest()
    # Lấy hash từ file torrent cho piece tương ứng
    expected_hash = get_piece_hash_from_torrent(pieces_base64, piece_index)
    
    # So sánh hash
    if piece_hash == expected_hash:
        print(f"Piece {piece_index} hợp lệ.")
        return True
    else:
        print(f"Piece {piece_index} không hợp lệ.")
        return False
    
def combine_pieces(pieces, output_file):
    # Mở tệp đầu ra ở chế độ ghi nhị phân
    with open(output_file, 'wb') as outfile:
        for piece in pieces:
            print(len(piece))
            # Ghi từng phần dữ liệu vào tệp đầu ra
            outfile.write(piece)