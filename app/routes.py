from flask import Blueprint, current_app, render_template,request, Response
from flask import current_app as app
from .mqtt import mqtt_client_connect, mqtt_client_disconnect, messages, send_payload_to_mqtt
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
        sse_topic = request.form['sse_topic']
        payload_topic= request.form['payload_topic']
        client_id = request.form['client_id']

    MQTT_CONNECTION_DATA={
        'username': username,
        'password': password,
        'broker': broker,
        'port': port,
        'sse_topic': sse_topic,
        'payload_topic': payload_topic,
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
                message = "Api:et är igång"
                return render_template('index.html', message=message), 400
            else:
                raise Exception("Något gick fel")
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


@main.route('/sse')
def sse():
    def generate():

        while True:
            if messages:
                # Send the latest message as an SSE event
                message = messages.pop(0)
                yield f"data: {message}\n\n"

    return Response(generate(), content_type='text/event-stream')


@main.route('/automode', methods=['POST'])
def automode():
    payload_data = {'transId': '989C6E5C-2CC1-11CA-A044-08002B1BB4F5',
                    'cmd_name': 'auto',
                    'cmd_arg': None
                    }

    send_payload_to_mqtt(payload_data, current_app.MQTTClient)

    response_massage = 'Autoläge'

    return render_template('index.html', responsmassages=response_massage)


@main.route('/charge', methods=['GET','POST'])
def charge():
    cmd_arg= request.form['charge']
    payload_data = {'transId': '1',
                    'cmd_name': 'charge',
                    'cmd_arg': cmd_arg
                    }

    send_payload_to_mqtt(payload_data, current_app.MQTTClient)
    massage = 'Laddar'
    return render_template('index.html', responsmassages=massage)


@main.route('/discharge', methods=['GET','POST'])
def discharge():
    cmd_arg= request.form['discharge']
    payload_data = {'transId': '1508459760',
                    'cmd_name': 'discharge',
                    'cmd_arg': cmd_arg
                    }
    send_payload_to_mqtt(payload_data, current_app.MQTTClient)
    response_massage = 'Urladdning'
    return render_template('index.html', responsmassages=response_massage)