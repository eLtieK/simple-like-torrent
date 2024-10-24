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

    