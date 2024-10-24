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
    client.close()

    # Kiểm tra kết nối đến MongoDB
try:
    client.admin.command('ping')
    print("Kết nối đến MongoDB thành công!")
except Exception as e:
    print(f"Không thể kết nối đến MongoDB: {e}")