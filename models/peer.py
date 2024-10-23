from models import init_model as model

def peer_collection():
    return model.init_collection("peers")