from flask import Flask, request
from flask_cors import CORS
from controllers import tracker_controller
import sys
import signal

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

def start_server(routes, my_host, my_port):
    for route in routes:
        app.register_blueprint(route)

    app.run(host=my_host, port=my_port, debug=True)

# Xử lý khi nhận tín hiệu tắt ứng dụng
def signal_handler(sig, frame):
    print("Shutting down...")
    tracker_controller.set_all_peer_inactive()
    sys.exit(0)

# Đăng ký tín hiệu
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)