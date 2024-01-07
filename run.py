from app import create_app, socketio
from application import app

app=create_app()


if __name__=="__main__":

    socketio.run(app, debug=True, threaded=True, port=5000)