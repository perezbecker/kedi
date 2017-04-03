#!/usr/bin/env python

import math
import time
import datetime

from microdotphat import clear, set_brightness, set_decimal, show, write_string, WIDTH, HEIGHT



speed = 5


string = 0
shown = True

show()

# Start time. Phase offset by math.pi/2
start = time.time()

while True:
    # Fade the brightness in/out using a sine wave
    b = (math.sin((time.time() - start) * speed) + 1) / 2
    set_brightness(b)

    # At minimum brightness, swap out the string for the next one
    if b < 0.002 and shown:
        clear()

        t = datetime.datetime.now()
        if t.second % 2 == 0:
            set_decimal(2, 1)
            set_decimal(4, 1)
        else:
            set_decimal(2, 0)
            set_decimal(4, 0)
        write_string(t.strftime('%H%M%S'), kerning=False)

        show()
        shown = False

    # At maximum brightness, confirm the string has been shown
    if b > 0.998:
        shown = True

    # Sleep a bit to save resources, this wont affect the fading speed
    time.sleep(0.01)
