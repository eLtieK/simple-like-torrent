from pymongo import MongoClient

def connect_database(url):
    # Tạo kết nối tới MongoDB
    client = MongoClient(url)
    return client

def close_connection(client):
    # Đóng kết nối MongoDB
    client.close()