from shifter import Shifter
import time

class LED8x8:
    """A class useful for controlling the 8x8 LED array.

    """

    def __init__(self, data, latch, clock):
        """

        """

        self.shift = Shifter(data, latch, clock)

    def display(self, pattern):
        """Continuously updates the array based on a given pattern.

        Arguments
        ---------
        pattern : byte array
            The byte array corresponding to the pattern displayed on
            the LED array.

        """

        while 1:
            for row, val in enumerate(pattern):
                self.shift.shiftByte(val)
                self.shift.shiftByte(1 << row)
            time.sleep(0.001)
