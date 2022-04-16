import time
import json

from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
from counterfit_shims_grove.grove_led import GroveLed
import paho.mqtt.client as mqtt


CounterFitConnection.init()

light_sensor = GroveLightSensor(0)
led = GroveLed(5)

id = 'bdc25316-c99d-44b8-b1c1-a936d7607a0f'
client_name = id + 'nightlight_client'
client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()


def handle_command(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print('Message received:', payload)

    if payload['led_on']:
        led.on()
    else:
        led.off()


mqtt_client.subscribe(server_command_topic)
mqtt_client.on_message = handle_command

print('MQTT connected')

while True:
    light = light_sensor.light
    telemetry = json.dumps({'light': light})

    print('Sending telemetry', telemetry)

    mqtt_client.publish(client_telemetry_topic, telemetry)

    time.sleep(5)
