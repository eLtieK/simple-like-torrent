from config import database

def init_collection(collection):
    return database.get_db()[collection]