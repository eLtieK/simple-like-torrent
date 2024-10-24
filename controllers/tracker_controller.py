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

    