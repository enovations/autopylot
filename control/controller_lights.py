import threading
import time
from enum import Enum

from lib import LED as L

LED = None
max_led = 43
no_led = False
running = True

class Direction(Enum):
    NONE = 0
    LEFT = -1
    RIGHT = 1


direction = Direction.NONE


def init():
    global no_led
    global LED
    try:
        LED = L.rumbaLED()
    except:
        no_led = True
        return
    LED.SetAll(0, 0, 0)
    LED.Update()
    t = threading.Thread(target=run)
    t.start()


def run():
    global LED
    global no_led
    global running

    if no_led:
        return

    while running:
        if direction == Direction.NONE:
            LED.SetAll(0, 0, 0)
            for i in range(10, 33):
                LED.Set(i, 20, 20, 20)
            LED.Update()
        time.sleep(0.03)

    LED.SetAll(0, 0, 0)
    LED.Update()


def close():
    global LED
    global no_led
    global running

    if no_led:
        return

    print('closing led')

    running = False
