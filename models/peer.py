from models import init_model as model
class Peer:
    def __init__(self, id, ip, port):
        self.id = id
        self.ip = ip
        self.port = port

def peer_collection():
    return model.init_collection("peers")