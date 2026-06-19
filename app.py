from flask import Flask
from flask_jwt_extended import JWTManager

from config import Config
from models import db
from routes import api_bp , task_bp  
import logging
from waitress import serve
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
JWTManager(app)
app.register_blueprint(api_bp)
app.register_blueprint(task_bp)   

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

if __name__ == "__main__":
   print("Starting production server on port 5000...")
   serve(app, host="0.0.0.0", port=5000, threads=6)