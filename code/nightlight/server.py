import json
import time

import paho.mqtt.client as mqtt


id = 'bdc25316-c99d-44b8-b1c1-a936d7607a0f'
client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'
client_name = id + 'nightlight_server'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()


def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print('Message received:', payload)

    command = {'led_on': payload['light'] < 300}
    print('Sending message:', command)

    client.publish(server_command_topic, json.dumps(command))


mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

while True:
    time.sleep(2)
