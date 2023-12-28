from flask import Blueprint, current_app, render_template,request, Response
from flask import current_app as app
from .mqtt import mqtt_client_connect, mqtt_client_disconnect, messages
import importlib
import config



import json

main = Blueprint('main', __name__)
user = Blueprint('user', __name__)
regsiter = Blueprint('regsiter', __name__)
mqtt_start = Blueprint('mqtt_start', __name__)
mqtt_stop = Blueprint('mqtt_stop', __name__)





@main.route('/')
def index():
    return render_template('index.html')

@regsiter.route('/register')
def register_page():
    return render_template('register.html')


@user.route('/user', methods=['POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        broker = request.form['broker']
        port = int(request.form['port'])
        topic = request.form['topic']
        client_id = request.form['client_id']

    MQTT_CONNECTION_DATA={
        'username': username,
        'password': password,
        'broker': broker,
        'port': port,
        'topic': topic,
        'client_id': client_id
    }

    with open('config.py', 'w') as file:
        file.write(f'MQTT_CONNECTION_DATA={json.dumps(MQTT_CONNECTION_DATA, indent=4)}\n')
        file.close()
    message = "Allt Klart!."
    return render_template('register.html', message=message)


@mqtt_start.route('/start', methods=['GET','POST'])
def start_mqtt():
    importlib.reload(config)
    app.config.from_object('config')

    with app.app_context():
        try:
            mqtt_client = mqtt_client_connect(app.config['MQTT_CONNECTION_DATA'])
            if mqtt_client is not None:
                message = "Api:et är nu igång"
                return render_template('index.html', message=message), 400
            else:
                raise Exception("Något gick fel1")
        except Exception as e:
            message = str(e)
            return render_template('index.html', message=message), 400



@mqtt_stop.route('/stop', methods=['GET','POST'])
def stop_mqtt():
    try:
        mqtt_client_instance=current_app.MQTTClient
        if mqtt_client_instance is not None and hasattr(mqtt_client_instance, 'disconnect'):
            mqtt_client_disconnect(mqtt_client_instance)
            message = "Api:et är nu avstängt"
        else:
            raise Exception("Något gick fel")
    except Exception as e:
        message = str(e)

    return render_template('index.html', message=message), 400


