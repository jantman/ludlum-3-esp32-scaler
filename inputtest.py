"""
Input test script for jantman/ludlum-3-esp32-scaler

Uses GPIO pin 4

https://github.com/jantman/ludlum-3-esp32-scaler
"""
from machine import Pin, Timer
from micropython import const

pin = Pin(4, Pin.IN, Pin.PULL_UP)

counter = 0

timer = Timer(0)


def on_timer(x):
    global counter
    val = counter
    counter = 0
    print('%d cps / %d cpm' % (val, val * 60))


def on_pulse(x):
    global counter
    counter += 1


timer.init(period=1000, mode=Timer.PERIODIC, callback=on_timer)
# NOTE - Pin.IRQ_FALLING gives a double count
pin.irq(trigger=Pin.IRQ_RISING, handler=on_pulse)
