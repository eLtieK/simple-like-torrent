from pymongo import MongoClient
import os
from dotenv import load_dotenv
url = os.getenv('MONGO_URL')
client = MongoClient(url)
db = client["mmt"]

def get_db():
    return db

def close_connection():
    # Đóng kết nối MongoDB
    db.close()