#!/usr/bin/python

from lib.PoKeys import *


class rumbaLED:
    def __init__(self):
        # Load the library and connect to the device
        self.mydevice = PoKeysDevice("libPoKeys.so")

        # Connect to the PoKeys device
        print("Connecting to the LED controller...")
        if self.mydevice.PK_ConnectToDevice(1) != 0:
            print("Device not found, quitting!")
            sys.exit(0)

        self.Enable()
        self.maxLEDlvl = 50

        self.LEDdata = []
        for i in range(50):
            self.LEDdata.append(0)

        self.Update()

    def Enable(self):
        # Enable support for WS2812 LEDs (50 LEDs in total)
        self.mydevice.PK_WS2812_Config(50, 0)

    def Update(self):
        for i in range(50):
            r, g, b = self.LEDdata[i] & 0xFF, (self.LEDdata[i] >> 8) & 0xff, (self.LEDdata[i] >> 16) & 0xFF
            if r > self.maxLEDlvl:
                r = self.maxLEDlvl
            if g > self.maxLEDlvl:
                g = self.maxLEDlvl
            if b > self.maxLEDlvl:
                b = self.maxLEDlvl

            self.LEDdata[i] = (r) + (g << 8) + (b << 16)

        self.mydevice.PK_WS2812_SendData(self.LEDdata, 0)
        self.mydevice.PK_WS2812_Config(50, 1)  # Send this command to update the LEDs

    def Set(self, LEDindex, r, g, b):
        self.LEDdata[LEDindex] = r + (g << 8) + (b << 16)

    def SetAll(self, r, g, b):
        for i in range(50):
            self.LEDdata[i] = r + (g << 8) + (b << 16)


if __name__ == "__main__":
    # Test the LED interface
    LED = rumbaLED()

    # Turn on all LEDs in white with power 10
    LED.SetAll(10, 10, 10)
    LED.Update()

    # Wait 0.1 s then turn them all off
    time.sleep(0.1)

    LED.SetAll(0, 0, 0)
    LED.Update()

    # Knight rider effect...
    W = 20
    start = 25 - W / 2
    ind = 0

    PWR = [0] * W

    try:
        while True:
            for i in range(W):
                if PWR[i] > 0:
                    PWR[i] *= 0.4

            if ind < W:
                PWR[ind] = 255
            elif ind < 2 * W:
                PWR[2 * W - 1 - ind] = 255

            ind += 1
            if ind >= 2 * W:
                ind = 0

            for i in range(W):
                LED.Set(int(start + i), int(PWR[i]), 0, 0)

            # Update LEDs
            LED.Update()

            time.sleep(0.03)
    except (KeyboardInterrupt, SystemExit):
        for i in range(50):
            LED.Set(i, 0, 0, 0)
        LED.Update()
