"""
Input test script for jantman/ludlum-3-esp32-scaler

Uses GPIO pin 4

https://github.com/jantman/ludlum-3-esp32-scaler
"""

from machine import Pin, Timer
from utime import sleep_ms
from micropython import const
from uarray import array
from utime import sleep_ms
import micropython

micropython.alloc_emergency_exception_buf(100)


class Scaler:

    def __init__(self):
        self._pin = Pin(4, Pin.IN, Pin.PULL_UP)
        self._decisec_pointer = 0
        self._decisec_array = array('I', [0 for _ in range(0, 10)])
        self._sec_pointer = 0
        self._sec_array = array('Q', [0 for _ in range(0, 60)])
        self._pin.irq(trigger=Pin.IRQ_RISING, handler=self.on_pulse)

    def run(self):
        while True:
            self.do_decisec()
            sleep_ms(100)

    def do_decisec(self):
        old_ptr = self._decisec_pointer
        if old_ptr == 9:
            self._decisec_pointer = 0
            self._sec_array[self._sec_pointer] = sum(self._decisec_array)
            if self._sec_pointer == 59:
                self._sec_pointer = 0
            else:
                self._sec_pointer += 1
        else:
            self._decisec_pointer += 1
        print(self._decisec_array)
        print(
            '%d CPS\t%d CPM' % (
                sum(self._decisec_array), sum(self._sec_array)
            )
        )
        self._decisec_array[old_ptr] = 0

    def on_pulse(self, *args):
        self._decisec_array[self._decisec_pointer] += 1


if __name__ == "__main__":
    Scaler().run()
