from paho.mqtt.client import Client
from time import sleep
from random import random, randint
import json
# from HCSR04 import HC-SR04
from HCSR04Mock import HCSR04

class Device:
    def __init__(self, dev_id, broker, battery_time, main_topic):
        """
        :param dev_id: id of the device
        :param broker: address of the broker
        :param battery_time: number of seconds that the battery can run
        :param main_topic: main topic of the broker
        """
        self.dev_id = dev_id
        self.topic = f"{main_topic}/{dev_id}"

        self.client = Client(dev_id)
        self.broker = broker

        
        self.sensor = HCSR04(trigger_pin=13, echo_pin=12,echo_timeout_us=1000000)
        self.capacity = 100    # in cm
        self.free_space = self.capacity
        self.update_free_space()

        self.battery = battery_time
        self.battery_runtime = battery_time

    def start(self):
        self.client.connect(*self.broker)
        self.client.loop_start()  # runs in new thread
        self.run()

    def run(self):
        while self.battery:
            self.update_battery()
            self.update_free_space()
            self.send()
            sleep(1)
        self.stop()

    def stop(self):
        self.client.disconnect()
        self.client.loop_stop()

    def send(self):
        payload = {
            "battery": self.battery_percent(),
            "capacity": self.capacity,
            "free space": self.free_space
        }
        self.client.publish(f"{self.topic}", json.dumps(payload))

    def battery_percent(self):
        return str(round(self.battery / self.battery_runtime, 2))

    def update_free_space(self):
        self.free_space = self.sensor.distance_cm()

    def update_battery(self):
        self.battery -= 1
