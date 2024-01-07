import paho.mqtt.client as mqtt
from flask import current_app
from application import app
import json
import time


messages = []


class MQTTPayload:
    def __init__(self, transId, cmd_name, cmd_arg=None):
        self.transId = transId
        self.cmd_name = cmd_name
        self.cmd_arg = cmd_arg

    def to_dict(self):
        return self.__dict__


def mqtt_client_connect(MQTT_CONNECTION_DATA):
    client = mqtt.Client()

    client.username_pw_set(
        current_app.config['MQTT_CONNECTION_DATA']['username'],
        current_app.config['MQTT_CONNECTION_DATA']['password']
    )

    #set the MQTT on_message callback
    client.on_message = on_message

    client.connect(
        current_app.config['MQTT_CONNECTION_DATA']['broker'],
        current_app.config['MQTT_CONNECTION_DATA']['port']
    )

    client.subscribe(current_app.config['MQTT_CONNECTION_DATA']['sse_topic'])

    client.subscribe(current_app.config['MQTT_CONNECTION_DATA']['payload_topic'])


    client.loop_start()
    time.sleep(3)

    current_app.MQTTClient = client
    return client

def mqtt_client_disconnect(client):
    client.loop_stop()
    client.disconnect()


def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    power = payload.get('soc', {})
    for key, value in power.items():
        rounded_value= round(float(value), 1)
        messages.append(rounded_value)
        print(messages[-1])


def send_payload_to_mqtt(payload_data, client):
    with app.app_context():
        payload ={
            'transId': payload_data['transId'],
            'cmd': {
                'name': payload_data['cmd_name'],
                'arg': payload_data['cmd_arg']
            }
        }
        payload_jason = json.dumps(payload)
        print(f'Payload: {payload_jason}')
        client.publish(
            app.config['MQTT_CONNECTION_DATA']['payload_topic'],
            payload_jason
        )
