import requests
from bson.objectid import ObjectId
from config.database import get_db, close_connection
from models import peer
from controllers.torrent_controller import create_info_hash, create_magnet_link, create_torrent_file
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

def upload_file(file_name, file_content, peer_id):
    try:
        db = get_db()
        collection = db['files']
        file_data = {
            "file_name": file_name,
            "file_content": file_content,
            "peer_id": peer_id
        }
        
        print(f"Attempting to insert document: {file_data}")
        result = collection.insert_one(file_data)
        print(f"Inserted document with id: {result.inserted_id}")
        
        update_peer_shared_files(peer_id, file_name)
        
        file_length = len(file_content)
        info_hash = create_info_hash(file_name, file_length, 512000,b"abcd1234efgh5678abcd1234efgh5678")
        magnet_link = create_magnet_link(info_hash, file_name)
        print(f"Magnet link: {magnet_link}")
        
        output_file = f"{file_name}.torrent"
        create_torrent_file(info_hash, file_name, file_length, output_file)
                
        return True
    except Exception as e:
        print(f"Error uploading file: {e}")
        return False
    finally:
        close_connection()

def update_peer_shared_files(peer_id, file_name):
    collection = peer.peer_collection()
    collection.update_one(
        {"_id": ObjectId(peer_id)},
        {"$addToSet": {"shared_files": file_name}}
    )
