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

def sign_up(name, password):
    collection = peer.peer_collection()
    ip, port = get_peer_info()
    
    data = {
        "_id": ObjectId(),  # Tạo ObjectId mới
        "name": name,
        "password": password,
        "ip_address": ip,
        "port": port,
        "shared_files": [],
        "downloaded_count": 0,
        "uploaded_count": 0
    }

     # Thêm người dùng vào collection
    result = collection.insert_one(data)

    return str(data['_id'])

def login(name, password):
    collection = peer.peer_collection()
    data = collection.find_one({
        "name": name,
        "password": password
    })

    if data:
        return True, str(data['_id'])
    else:   
        return False, ""
    
