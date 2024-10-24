from flask import Flask, request

tracker = Flask(__name__)
peers = Flask(__name__)

def start_server(server, routes, my_host, my_port):
    for route in routes:
        server.register_blueprint(route)

    server.run(host=my_host, port=my_port, debug=True)


    