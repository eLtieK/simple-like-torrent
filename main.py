from config import database
import os
from dotenv import load_dotenv
from config import system
from routes import routes
import argparse

if __name__ == "__main__":
    # Load các biến môi trường từ file .env
    load_dotenv()
    my_host = os.getenv('HOST')
    peer_port = os.getenv('PEER_PORT')
    tracker_port = os.getenv('TRACKER_PORT')

    # Thiết lập parser để nhận tham số từ dòng lệnh
    # Chạy server peer: python main.py --mode peer  
    # Chạy server tracker: python main.py --mode tracker
    parser = argparse.ArgumentParser(description='Run Peer and Tracker servers.')
    parser.add_argument('--mode', type=str, choices=['peer', 'tracker'], required=True, help='Specify which server to run')
    args = parser.parse_args()

    if(args.mode == 'tracker'):
        system.start_tracker(routes.get_all_tracker_routes(), my_host, tracker_port)
    else:
        system.start_peers(routes.get_all_peers_routes(), my_host, peer_port)
