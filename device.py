from paho.mqtt.client import Client
from time import sleep
from random import random, randint
import json
# import machine
# from HCSR04 import HC-SR04
import machineMock as machine
from HCSR04Mock import HCSR04

class Device:
    def __init__(self, dev_id, broker, battery_time, message_time, main_topic):
        """
        :param dev_id: id of the device
        :param broker: address of the broker
        :param battery_time: number of informations that can be sent during battery life
        :param message_time: a message will be send every certain period of time (in seconds)
        :param main_topic: main topic of the broker
        """
        self.dev_id = dev_id
        self.topic = f"{main_topic}/{dev_id}"

        self.client = Client(dev_id)
        self.broker = broker

        # seconds to milliseconds 1 second = 1000 ms
        self.send_message_time = message_time * 1000
        
        # the ustrasonic sensor
        self.sensor = HCSR04(trigger_pin = 13, echo_pin = 12, echo_timeout_us = 1000000)

        # capacity of the bin (in centimetres)
        self.capacity = 100 
        self.free_space = self.capacity

        self.battery_runtime = battery_time
        self.battery = battery_time


    def start(self):
        self.client.connect(*self.broker)
        self.client.loop_start()  # runs in new thread
        self.run()

    def run(self):
        while self.battery:
            self.update_free_space()
            print(self.free_space)
            self.get_battery()
            self.send()
            machine.deepsleep(self.send_message_time)
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


    def update_free_space(self):
        self.free_space = self.sensor.distance_cm()

    def battery_percent(self):
        return self.battery / self.battery_runtime *100


    def get_battery(self): 
        # mocked battery update
        self.battery -= 1

        # functions to use with real device
        pot = machine.ADC(machine.Pin(34))
        pot.atten(machine.ADC.ATTN_11DB)

        nVoltageRaw = pot.read()
        sVoltage = nVoltageRaw * (17021.277) / 7021.277
        

        
    
