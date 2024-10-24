from flask import Flask, request

tracker = Flask(__name__)
peers = Flask(__name__)

def start_server(server, routes, my_host, my_port):
    for route in routes:
        server.register_blueprint(route)

    server.run(host=my_host, port=my_port, debug=True)

def start_tracker(routes, my_host, my_port):
    start_server(tracker,routes , my_host, my_port)

def start_peers(routes, my_host, my_port):
    start_server(peers, routes, my_host, my_port)


    