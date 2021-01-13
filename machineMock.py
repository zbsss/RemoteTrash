from time import sleep

# time in milliseconds
def deepsleep(sleep_time_ms):
    sleep(sleep_time_ms/1000)

class Pin:
    def __init__(self, pin):
        self.pin = pin


class ADC:
    ATTN_11DB = 3.3

    def __init__(self, pin):
        self.pin = pin
        self.max_voltage = 3.3
        self.step = 0.145394727 / 2
        self.actual_voltage = self.max_voltage

    def read(self):
        self.actual_voltage = self.actual_voltage - self.step
        return self.actual_voltage
    
    def atten(self, arg):
        self.max_voltage = arg