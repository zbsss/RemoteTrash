from device import Device
from multiprocessing import Process
from paho.mqtt.client import Client
import json

CONFIGURATION = {
    "project_id" : "tirprojekt",
    "cloud_region" : "europe-west1",
    "registry_id" : "smartbins",
    "private_key_file" : "rsa_private_",
    "algorithm" : "RS256",
    "ca_certs" : "roots.pem",
    "mqtt_bridge_hostname" : "mqtt.googleapis.com",
    "mqtt_bridge_port" : 8883,
}

DEVICE_NUM = 11
BROKER = ("34.70.234.204", 1883, 60)  # host, port, keepalive
REAL_BATTERY_TIME = 38 # in days x2, because battery time is updated when measurement is being done
REAL_MESSAGE_TIME = 3600*24 # 24h in s
BATTERY_TIME = 38  # seconds
MESSAGE_TIME = 3  # seconds
BIN_CAPACITY =  100 # centimetres
MAIN_TOPIC = '/devices/'


def create_device_and_loop(dev, num):
    create_config(dev, num, BATTERY_TIME, MESSAGE_TIME, BIN_CAPACITY)
    device = Device(CONFIGURATION)
    device.start()


def create_config(dev,num,BATTERY_TIME, MESSAGE_TIME, BIN_CAPACITY):
    CONFIGURATION["device_id"] = dev
    CONFIGURATION["num"] = num
    CONFIGURATION["message_time"] = MESSAGE_TIME
    CONFIGURATION["battery_time"] = BATTERY_TIME
    CONFIGURATION["bin_capacity"] = BIN_CAPACITY


def on_connect(client, userdata, flags, rc):
    client.subscribe(MAIN_TOPIC + '/#')


def on_message(client, userdata, msg):
    print(f"[SIM] {msg.topic} {msg.payload}")


def connect():
    client = Client('simulation')
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(*BROKER)
    client.loop_forever()  # runs in same thread


def simulate():
    for dev in range(1, DEVICE_NUM):
        proc = Process(target=create_device_and_loop, args=("smart-bin-{}".format(dev), dev))
        proc.start()
    connect()


if __name__ == '__main__':
    simulate()
