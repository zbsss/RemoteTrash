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
from machineMock import analogRead, A0


class Device:
    def __init__(self, dev, battery_time, message_time, num):
        """
        :param dev_id: id of the device
        :param broker: address of the broker
        :param battery_time: number of seconds that the battery can run
        :param message_time: a message will be send every certain period of time (in seconds)
        :param main_topic: main topic of the broker
        """
        self.conf = mqttHelper.CONFIGURATION
        self.conf['device_id'] = dev
        self.conf['private_key_file'] = self.conf['private_key_file'] + str(num) + ".pem"
        # seconds to milliseconds 1 second = 1000 ms
        self.send_message_time = message_time * 1000
        
        # the ustrasonic sensor
        self.sensor = HCSR04(trigger_pin = 13, echo_pin = 12, echo_timeout_us = 1000000)

        # capacity of the bin (in centimetres)
        self.capacity = 100 
        self.free_space = self.capacity

        self.battery_runtime = battery_time
        self.mqtt_init()
        self.battery = battery_time
        self.get_battery()

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
            "fulfillment":  self.capacity,
            "battery" : self.battery_percent(),
            "timestamp" : datetime.datetime.now().isoformat()
        }
        print("sending {}".format(self.conf['device_id']))
        print(json.dumps(payload))
        print(self.topic)
        print("")
        self.client.publish(self.topic, json.dumps(payload), qos=1)

    def battery_percent(self):
        #TODO calc from voltage to percent
        return 50
        return 27.02*self.battery

    def update_free_space(self):
        self.free_space = self.sensor.distance_cm()

    def get_battery(self):
        pot = machine.ADC(machine.Pin(34))
        pot.atten(machine.ADC.ATTN_11DB)

        nVoltageRaw = pot.read()
        fVoltage = nVoltageRaw * 0.00486
        self.battery = fVoltage


if __name__ == "__main__":
    dev = Device(100, 2)
    dev.start()