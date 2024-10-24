from flask import Flask, request
app = Flask(__name__)

def start_server(routes, my_host, my_port):
    for route in routes:
        app.register_blueprint(route)

    app.run(host=my_host, port=my_port, debug=True)

    