import paho.mqtt.client as mqtt
from flask import current_app

import json
import time


messages = []


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

    client.subscribe(
        current_app.config['MQTT_CONNECTION_DATA']['topic']
    )

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
        messages.append(value)
        print(messages[-1])
