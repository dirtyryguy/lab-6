import RPi.GPIO as gpio
import time

class Shifter:
    """

    """

    def __init__(self, data, latch, clock):
        """

        """

        self.dataPin, self.latchPin, self.clockPin = data, latch, clock
        gpio.setmode(gpio.BCM)
        gpio.setup(self.dataPin, gpio.OUT)
        gpio.setup(self.latchPin, gpio.OUT, initial=0)
        gpio.setup(self.clockPin, gpio.OUT, initial=0)

    def ping(self, pin):
        """

        """

        gpio.output(pin, 1)
        time.sleep(0)
        gpio.output(pin, 0)

    def shiftByte(self, byteVal, anode=True):
        """

        """

        for i in range(8):
            if anode:
                gpio.output(self.dataPin, ~(byteVal & (1<<i)))
            else:
                gpio.output(self.dataPin, byteVal & (1<<i))
            self.pin(self.clockPin)
        self.ping(self.latchPin)
