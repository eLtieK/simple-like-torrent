from flask import Flask, request
from models import peer
from bson import ObjectId
import socket
import threading
from queue import Queue
import base64


def get_ip_and_port():
    """
    Hàm lấy thông tin IP và Port của client kết nối.
    """
    peer_ip = request.remote_addr  # Địa chỉ IP của client
    peer_port = request.environ.get('REMOTE_PORT')  # Cổng của client
    return peer_ip, peer_port

def get_peer_info(ip, port):
    """
    Hàm lấy thông tin IP và Port của client kết nối.
    """
    collection = peer.peer_collection()
    peer_data = collection.find_one({
        "ip_address": ip,
        "port": port
    })

    return str(peer_data["_id"])

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
    ip, port = get_ip_and_port()
    
    data = {
        "_id": ObjectId(),  # Tạo ObjectId mới
        "name": name,
        "password": password,
        "ip_address": ip,
        "port": port,
        "piece_info": [],
        "status": "inactive"
    }

     # Thêm người dùng vào collection
    result = collection.insert_one(data)

    return data['ip_address'], data['port']

def login(name, password):
    collection = peer.peer_collection()
    ip, port = get_ip_and_port()
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
                    "port": port,
                    "status": "active"
                }
            })
        if data.modified_count > 0:
            return True, str(user["_id"]), ip, port
    
    return False, "", "", ""

def request_piece(peer_id, piece_index, pieces, requested_pieces, queue_lock, metainfo_id):
    peer_ip = peer_id['ip_address']
    peer_port = peer_id['port']
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((peer_ip, peer_port))

            # Gửi yêu cầu lấy piece cụ thể
            request_message = f"REQUEST_PIECE|{piece_index, metainfo_id}"
            client_socket.send(request_message.encode())
            
            # Nhận dữ liệu piece từ peer
            piece_data = client_socket.recv(1024)
            if piece_data == "PIECE_NOT_FOUND":
                print(f"Piece {piece_index} not found on peer {peer_ip}:{peer_port}")
            else:
                print(f"Received piece data from {peer_ip}:{peer_port} for piece {piece_index}")
                # Lưu piece vào danh sách, cập nhật trạng thái
                with queue_lock:
                    pieces[piece_index] = piece_data
                    requested_pieces.remove(piece_index)

    except ConnectionRefusedError:
        print(f"Không thể kết nối đến peer {peer_ip}:{peer_port}")
    except Exception as e:
        print(f"Đã xảy ra lỗi khi kết nối tới peer {peer_ip}:{peer_port}: {str(e)}")

def request_pieces_from_peers(peer_list, piece_indexes, torrent_data, available_pieces):
    # Kiểm tra nếu piece_indexes rỗng
    if not piece_indexes:
        pieces = [None] # Hoặc khởi tạo như một danh sách với các phần tử None
    else:
        pieces = [None] * (max(piece_indexes) + 1)  # Danh sách lưu các pieces đã nhận

    requested_pieces = set()  # Set để lưu các pieces đang được yêu cầu
    queue_lock = threading.Lock()
    threads = []

    # Hàng đợi để quản lý các yêu cầu tải xuống
    piece_queue = Queue()
    metainfo_id = str(torrent_data["_id"])
    # Thêm các piece cần tải (dựa vào các chỉ số piece) vào hàng đợi
    for piece_index in piece_indexes:
        if piece_index not in available_pieces:  # Kiểm tra piece có sẵn
            piece_queue.put(piece_index)
    #print(peer_id, piece_index, pieces, requested_pieces, queue_lock, metainfo_id)
    while not piece_queue.empty():
        piece_index = piece_queue.get()

        # Chọn peer có piece đó theo vòng lặp danh sách
        peer_id = peer_list[piece_index % len(peer_list)]

        with queue_lock:
            if piece_index not in requested_pieces:
                requested_pieces.add(piece_index)
                
                # Tạo thread cho từng piece và peer
                thread = threading.Thread(target=request_piece, args=(peer_id, piece_index, pieces, requested_pieces, queue_lock, metainfo_id))
                threads.append(thread)
                thread.start()

    # Chờ cho tất cả các thread hoàn thành
    for thread in threads:
        thread.join()

    return pieces

def run_peer_server(ip, port, peer_id):
    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer_socket.bind((ip, port))
    peer_socket.listen(10)
    
    while True:
        client_socket, addr = peer_socket.accept()
        request = client_socket.recv(1024).decode()
        if(request.startswith("REQUEST_PIECE")):
             # Tách lấy piece_index và metainfo_id từ request
            try:
                _, params = request.split("|")
                piece_index, metainfo_id = eval(params)  # Lấy piece_index từ params

                # Gửi dữ liệu của piece về cho client
                send_piece_data(piece_index, client_socket, peer_id, metainfo_id)
            except Exception as e:
                print(f"Error processing request: {str(e)}")
                client_socket.send(b"ERROR")
        client_socket.close()

def send_piece_data(piece_index, client_socket, peer_id, metainfo_id):
    """Hàm này gửi dữ liệu của piece được yêu cầu về cho client."""
    collection = peer.peer_collection()
    peer_data = collection.find_one({
        "_id": ObjectId(peer_id)
    })

    if peer_data and "piece_info" in peer_data:
        # Truy xuất mảng piece_info
        piece_info = peer_data["piece_info"]

        # print(piece_info, piece_index, metainfo_id)
        # Sử dụng vòng lặp for để tìm piece có index bằng piece_index
        piece_data = None
        for piece in piece_info:
            if piece["index"] == piece_index and piece["metainfo_id"] == ObjectId(metainfo_id):
                piece_data = piece["piece"]
                break
            
        if piece_data:
            client_socket.send(piece_data)
        else:
            print("Không tìm thấy piece với piece_index yêu cầu.")
    else:
        # Nếu piece không tồn tại, trả về thông báo lỗi
        client_socket.send(b"PIECE_NOT_FOUND")
        print(f"Piece {piece_index} not found.")

