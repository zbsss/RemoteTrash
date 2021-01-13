from device import Device
from multiprocessing import Process
from paho.mqtt.client import Client


DEVICE_NUM = 4
BROKER = ("34.70.234.204", 1883, 60)  # host, port, keepalive
REAL_BATTERY_TIME = 25 # in day x2, because battery time is updated when measurement is being done
REAL_MESSAGE_TIME = 3600*24 # 24h in s
BATTERY_TIME = 60  # seconds
MESSAGE_TIME = 4  # seconds
MAIN_TOPIC = '/devices/'


def create_device_and_loop(dev, num):
    device = Device(dev, BATTERY_TIME, MESSAGE_TIME, num)
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
    for dev in range(1, DEVICE_NUM):
        proc = Process(target=create_device_and_loop, args=("smart-bin-{}".format(dev), dev))
        proc.start()
    connect()


if __name__ == '__main__':
    simulate()
