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
    STOP = 2


direction = Direction.NONE
last_time = time.time()


def set_direction(d):
    global direction
    global last_time

    direction = d
    last_time = time.time()


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
    global last_time

    if no_led:
        return

    indicator_step = 0
    sleep = 0.06

    while running:
        LED.SetAll(0, 0, 0)

        # set main lights
        # for i in range(10, 34):
        #    LED.Set(i, 50, 50, 50)

        # tesla like headlights 
        for i in range(0, 14):
            LED.Set(i, 50, 50, 50)

        for i in range(30, 44):
            LED.Set(i, 50, 50, 50)

        if direction == Direction.LEFT:
            if indicator_step == 11:
                time.sleep(0.12)
                indicator_step = 0
                sleep = 0.06
                for i in range(10):
                    LED.Set(i, 50, 50, 50)
            else:
                for i in range(9, 9 - indicator_step, -1):
                    LED.Set(i, 50, 20, 0)
                indicator_step += 1
                sleep *= 0.9

        if direction == Direction.RIGHT:
            if indicator_step == 11:
                time.sleep(0.12)
                indicator_step = 0
                sleep = 0.06
                for i in range(34, 44):
                    LED.Set(i, 50, 50, 50)
            else:
                for i in range(34, 34 + indicator_step):
                    LED.Set(i, 50, 20, 0)
                indicator_step += 1
                sleep *= 0.9

        if direction == Direction.STOP:
            if indicator_step == 11:
                time.sleep(0.12)
                indicator_step = 0
                sleep = 0.06
                for i in range(34, 44):
                    LED.Set(i, 0, 0, 0)
                for i in range(10):
                    LED.Set(i, 0, 0, 0)
            else:
                for i in range(34, 34 + indicator_step):
                    LED.Set(i, 50, 20, 0)
                for i in range(9, 9 - indicator_step, -1):
                    LED.Set(i, 50, 20, 0)

                indicator_step += 1
                sleep *= 0.9

        LED.Update()
        time.sleep(sleep)

        if direction != Direction.NONE and time.time() - last_time > 5:
            global direction
            direction = Direction.NONE

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
