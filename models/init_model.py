from config import database

def init_collection(collection):
    return database.db[collection]