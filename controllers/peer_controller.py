from flask import Flask, request
from models import peer
from bson import ObjectId

def get_peer_info():
    """
    Hàm lấy thông tin IP và Port của client kết nối.
    """
    peer_ip = request.remote_addr  # Địa chỉ IP của client
    peer_port = request.environ.get('REMOTE_PORT')  # Cổng của client
    return peer_ip, peer_port

def check_name_exists(name):
    collection = peer.peer_collection()
    
    # Tìm kiếm tên trong collection
    peer_data = collection.find_one({"name": name})
    
    # Trả về True nếu tên đã tồn tại, ngược lại trả về False
    return peer_data is not None

def sign_up(name, password):
    if check_name_exists(name):
        return None, None  # Hoặc có thể trả về một thông điệp lỗi
    
    collection = peer.peer_collection()
    ip, port = get_peer_info()
    
    data = {
        "_id": ObjectId(),  # Tạo ObjectId mới
        "name": name,
        "password": password,
        "ip_address": ip,
        "port": port,
        "piece_info": [],
    }

     # Thêm người dùng vào collection
    result = collection.insert_one(data)

    return data['ip_address'], data['port']

def login(name, password):
    collection = peer.peer_collection()
    ip, port = get_peer_info()
    # tim user
    user = collection.find_one(
        {
            "name": name,
            "password": password
        }
    )

    if user:
        # Cập nhật thông tin ip và port cho người dùng
        data = collection.update_one(
            {"_id": user["_id"]},
            {
                "$set": {
                    "ip_address": ip, # ip, port khi đăng nhập là mới 
                    "port": port
                }
            })
        if data.modified_count > 0:
            return True, str(user["_id"]), ip, port
    
    return False, "", "", ""
    
