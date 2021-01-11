from device import Device
from multiprocessing import Process
from paho.mqtt.client import Client


DEVICE_NUM = 10
BROKER = ("34.70.234.204", 1883, 60)  # host, port, keepalive
REAL_BATTERY_TIME = 38 # in days x2, because battery time is updated when measurement is being done
REAL_MESSAGE_TIME = 3600*24 # 24h in s
BATTERY_TIME = 60  # seconds
MESSAGE_TIME = 30  # seconds
MAIN_TOPIC = '2654645634673'


def create_device_and_loop(dev):
    device = Device(dev, BROKER, BATTERY_TIME, MESSAGE_TIME, MAIN_TOPIC)
    device.start()


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
    for dev in range(DEVICE_NUM):
        proc = Process(target=create_device_and_loop, args=(str(dev),))
        proc.start()
    connect()


if __name__ == '__main__':
    simulate()
