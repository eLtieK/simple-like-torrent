from config import database
import os
from dotenv import load_dotenv
from flask import Flask
from routes import routes

if __name__ == "__main__":
    # Load các biến môi trường từ file .env
    load_dotenv()
    url = os.getenv('MONGO_URL')
    my_host = os.getenv('HOST')
    my_port = os.getenv('')

    db = database.connect_database(url)

    app = Flask(__name__)
    app.register_blueprint(routes.routes)

    app.run(host=my_host, port=my_port)
