from models import init_model as model

def torrent_collection():
    return model.init_collection("torrents")