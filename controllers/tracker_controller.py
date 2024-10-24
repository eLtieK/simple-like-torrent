from models import peer

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
    
def get_files():
    files = []
    for f in file_collection.find():
        file_data = {
            "file_name": f.get("file_name", "Unknown"),
            "file_size": f.get("file_size", 0),
            "info_hash": f.get("info_hash", "Unknown")
        }
        files.append(file_data)
    return files

    