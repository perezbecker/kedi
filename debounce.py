import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(26,GPIO.IN)
input = GPIO.input(26)

import time
#initialise a previous input variable to 0 (assume button not pressed last)
prev_input = 0
counter = 0
while True:
  #take a reading
  input = GPIO.input(26)
  #if the last reading was low and this one high, print
  if ((not prev_input) and input):
    print("Button pressed")
    counter = counter+1
  #update previous input
  prev_input = input
  #slight pause to debounce
  time.sleep(0.05)
