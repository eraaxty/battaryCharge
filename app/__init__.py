from flask import Flask
from flask_socketio import SocketIO
from .routes import main, regsiter, user, mqtt_start, mqtt_stop

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    app.register_blueprint(regsiter)
    app.register_blueprint(user)
    app.config.from_object('config')
    app.register_blueprint(mqtt_start)
    app.register_blueprint(mqtt_stop)
    socketio.init_app(app)
    return app

