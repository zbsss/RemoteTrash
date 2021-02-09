from paho.mqtt.client import Client
from time import sleep
from random import random, randint
import json
# import machine
# from HCSR04 import HC-SR04
import machineMock as machine
from HCSR04Mock import HCSR04
import mqtt_functions as mqttHelper
from mqtt_functions import *
import time
import datetime


class Device:
    def __init__(self, config_file):
        """
        :param config_file: name of json file with configuration
        """

        # read device config
        with open(config_file) as f:
            self.conf = json.load(f)

        self.conf['private_key_file'] = self.conf['private_key_file'] + str(self.conf['num']) + ".pem"
        
        # seconds to milliseconds 1 second = 1000 ms
        self.send_message_time = self.conf['message_time'] * 1000
        
        # the ustrasonic sensor
        self.sensor = HCSR04(trigger_pin = 13, echo_pin = 12, echo_timeout_us = 1000000)

        # capacity of the bin (in centimetres)
        self.capacity = self.conf['bin_capacity'] 
        self.free_space = self.capacity

        self.battery_runtime = self.conf['battery_time']
        self.mqtt_init()
        self.battery = self.battery_runtime


    def mqtt_init(self):
        conf = self.conf
        self.topic = "/devices/{}/{}".format(conf['device_id'], "events")
        client = mqttHelper.get_client(
            conf['project_id'],
            conf['cloud_region'],
            conf['registry_id'],
            conf['device_id'],
            conf['private_key_file'],
            conf['algorithm'],
            conf['ca_certs'],
            conf['mqtt_bridge_hostname'],
            conf['mqtt_bridge_port']
        )


        print("connected")
        self.client = client
    def start(self):
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
            "name" : self.conf['device_id'],
            "fulfillment":  int(self.capacity),
            "battery" : int(self.battery_percent()),
            "timestamp" : datetime.datetime.now().isoformat()
        }
        print("sending {}".format(self.conf['device_id']))
        print(json.dumps(payload))
        print(self.topic)
        print("")
        self.client.publish(self.topic, json.dumps(payload), qos=1)


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

        voltageRaw = pot.read()
        sVoltage = voltageRaw * (17021.277) / 7021.277
    
