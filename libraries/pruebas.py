import time
import sys

import RPi.GPIO as GPIO

class HX711:
    def __init__(self, dout, pd_sck, gain=128):
        self.PD_SCK = pd_sck
        self.DOUT = dout
        self.GAIN = 0
        self.OFFSET = 0
        self.SCALE = 1
        self.lastVal = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PD_SCK, GPIO.OUT)
        GPIO.setup(self.DOUT, GPIO.IN)

        self.set_gain(gain)

    def set_gain(self, gain):
        if gain == 128:
            self.GAIN = 1
        elif gain == 64:
            self.GAIN = 3
        elif gain == 32:
            self.GAIN = 2

        GPIO.output(self.PD_SCK, False)
        self.read()

    def is_ready(self):
        return GPIO.input(self.DOUT) == 0

    def read(self):
        while not self.is_ready():
            pass

        data = [0]*3
        for j in range(3):
            data[j] = 0
            for i in range(8):
                GPIO.output(self.PD_SCK, True)
                data[j] <<= 1
                GPIO.output(self.PD_SCK, False)
                if GPIO.input(self.DOUT):
                    data[j] |= 1

        for i in range(self.GAIN):
            GPIO.output(self.PD_SCK, True)
            GPIO.output(self.PD_SCK, False)

        data[2] ^= 0x80
        result = data[0] << 16 | data[1] << 8 | data[2]
        self.lastVal = result
        return result

    def get_value(self):
        return self.read() - self.OFFSET

    def get_units(self):
        return self.get_value() / self.SCALE

    def tare(self, times=15):
        sum = 0
        for _ in range(times):
            sum += self.read()
        self.OFFSET = sum / times

    def set_scale(self, scale):
        self.SCALE = scale

    def set_offset(self, offset):
        self.OFFSET = offset

    def power_down(self):
        GPIO.output(self.PD_SCK, False)
        GPIO.output(self.PD_SCK, True)
        time.sleep(0.0001)

    def power_up(self):
        GPIO.output(self.PD_SCK, False)
        time.sleep(0.0001)

if __name__ == "__main__":
    hx = HX711(dout=5, pd_sck=6)
    hx.set_scale(7050)
    hx.tare()

    while True:
        try:
            val = hx.get_units()
            print("Weight: {} grams".format(val))
            time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            print("Cleaning up...")
            GPIO.cleanup()
            sys.exit()