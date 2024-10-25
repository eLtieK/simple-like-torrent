from models import peer, file, torrents
from controllers import torrent_controller, torrent_create
from bson import ObjectId
import bencodepy

def get_all_peer_info():
    collection = peer.peer_collection()
    peer_list = []
    for p in collection.find() :
        data = {
            "name": p["name"],  
            "ip_address": p["ip_address"],
            "port": p["port"],
            "shared_files": p["shared_files"]
        }
        peer_list.append(data)

    return peer_list

def get_peer(name):
    collection = peer.peer_collection()
    peer_data = collection.find_one({"name": name})
    data = None
    if peer_data:
        # Chuyển đổi đối tượng MongoDB về định dạng JSON
        data = {
            "name": peer_data['name'],
            "ip_address": peer_data['ip_address'],
            "port": peer_data['port'],
            "shared_files": peer_data['shared_files']
        }
    
    return data

def upload_file(file_path, peer_id):
    try:
        file_collection = file.file_collection()
        file_data = {
            "file_name": file_path.filename,
            "peer_ids": []
        }

        # Thêm peer_id vào mảng peer_ids
        file_data["peer_ids"].append(peer_id)
        # Thên file vào collection file
        file_collection.insert_one(file_data)
        # Thêm file vào field shared_files của peer
        update_peer_shared_files(peer_id, file_path.filename)

        # Các bước hình thành magnetext và metainfo của files
        file_path.seek(0)
        file_path.seek(0, 2) # seeks the end of the file
        file_length = file_path.tell() # tell at which byte we are
        file_path.seek(0, 0) # go back to the beginning of the file

        pieces = torrent_create.generate_pieces(file_path, 512000)
        info_hash = torrent_create.generate_info_hash(file_path.filename, 512000, file_length, pieces)
        magnet_link = torrent_create.create_magnet_link(info_hash, file_path.filename)
        print(f"Magnet link: {magnet_link}")

        output_file = f"{file_path.filename}.torrent"
        torrent_create.create_torrent_file(file_path.filename, 512000, pieces, file_length, output_file)
        add_torrent_to_db(output_file)

        return True
    except Exception as e:
        print(f"Error uploading file: {e}")
        return False

def update_peer_shared_files(peer_id, file_name):
    collection = peer.peer_collection()
    collection.update_one(
        {"_id": ObjectId(peer_id)}, 
        {
            "$addToSet": {"shared_files": file_name}, # Thêm file_name vào mảng shared_files
            "$inc": {"uploaded_count": 1}  # Tăng giá trị upload_count thêm 
        }
    )

def add_torrent_to_db(output_file):
    collection = torrents.torrent_collection()
    # Đọc tệp torrent
    with open(output_file, 'rb') as f:
        torrent_data = bencodepy.decode(f.read())

    # Chuẩn bị dữ liệu để thêm vào DB
    torrent_info = {
        "file_name": torrent_data[b'info'][b'name'].decode('utf-8'),
        "piece_length": torrent_data[b'info'][b'piece length'],
        "length": torrent_data[b'info'][b'length'],
        "pieces": torrent_data[b'info'][b'pieces'],
        "output_file": output_file  # Tên file torrent
    }
    
    # Thêm dữ liệu vào collection torrents
    collection.insert_one(torrent_info)
    print(f"Torrent '{torrent_info['file_name']}' added to database successfully!")

    