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
        self.max_voltage = 1.2

    def read(self):
        return 3.2
    
    def atten(self, arg):
        self.max_voltage = arg
