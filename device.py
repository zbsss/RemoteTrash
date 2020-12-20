from paho.mqtt.client import Client
from time import sleep
from random import random, randint

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

        self.capacity = 100

        self.battery = battery_time
        self.battery_runtime = battery_time

    def start(self):
        self.client.connect(*self.broker)
        self.client.loop_start()  # runs in new thread
        print(f"[{self.dev_id}] CONNECTED TO {self.broker}")
        self.run()

    def run(self):
        while self.battery:
            self.update_battery()
            self.update_capacity()
            self.send()
            sleep(1)

    def send(self):
        self.client.publish(f"{self.topic}/battery/{self.battery_percent()}")
        self.client.publish(f"{self.topic}/capacity/{self.capacity}")

    def battery_percent(self):
        return str(round(self.battery/self.battery_runtime, 2))

    def update_capacity(self):
        if random() > 0.5:
            self.capacity -= randint(1, 5)

    def update_battery(self):
        self.battery -= 1
