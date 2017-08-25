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


direction = Direction.RIGHT


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

    indicator_step = 0
    sleep = 0.06

    while running:
        LED.SetAll(0, 0, 0)
        for i in range(10, 33):
            LED.Set(i, 20, 20, 20)

        if direction == Direction.LEFT:
            if indicator_step == 11:
                time.sleep(0.09)
                indicator_step = 0
                sleep = 0.06
                for i in range(10):
                    LED.Set(i, 0, 0, 0)
            else:
                for i in range(10, 10 - indicator_step, -1):
                    LED.Set(i, 20, 10, 0)
                indicator_step += 1
                sleep *= 0.9

        if direction == Direction.RIGHT:
            if indicator_step == 11:
                time.sleep(0.09)
                indicator_step = 0
                sleep = 0.06
                for i in range(33, 43):
                    LED.Set(i, 0, 0, 0)
            else:
                for i in range(33, 33 + indicator_step):
                    LED.Set(i, 20, 10, 0)
                indicator_step += 1
                sleep *= 0.9

        LED.Update()
        time.sleep(sleep)

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
    LED.SetAll(0, 0, 0)
    LED.Update()
