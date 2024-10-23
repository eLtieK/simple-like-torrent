from config import database
import os
from dotenv import load_dotenv
from config import system
from routes import routes

if __name__ == "__main__":
    # Load các biến môi trường từ file .env
    load_dotenv()
    my_host = os.getenv('HOST')
    my_port = os.getenv('')

    system.start_tracker(routes.get_all_routes(), my_host, my_port)
