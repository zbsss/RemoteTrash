from device import Device
from multiprocessing import Process


DEVICE_NUM = 2
BROKER = ("test.mosquitto.org", 1883, 60)  # host, port, keepalive
BATTERY_TIME = 60  # seconds
MAIN_TOPIC = '2654645634673'


def create_device_and_loop(dev):
    device = Device(dev, BROKER, BATTERY_TIME, MAIN_TOPIC)
    device.start()


def simulate():
    for dev in range(DEVICE_NUM):
        proc = Process(target=create_device_and_loop, args=(str(dev),))
        proc.start()


if __name__ == '__main__':
    simulate()
