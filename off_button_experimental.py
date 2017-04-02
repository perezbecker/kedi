#!/bin/python
#This script was authored by AndrewH7 and belongs to him (www.instructables.com/member/AndrewH7)
#You have permission to modify and use this script only for your own personal usage
#You do not have permission to redistribute this script as your own work
#Use this script at your own risk

import RPi.GPIO as GPIO
import os
import time

gpio_pin_number=26
#Replace YOUR_CHOSEN_GPIO_NUMBER_HERE with the GPIO pin number you wish to use
#Make sure you know which rapsberry pi revision you are using first
#The line should look something lsike this e.g. "gpio_pin_number=7"

GPIO.setmode(GPIO.BCM)
#Use BCM pin numbering (i.e. the GPIO number, not pin number)
#WARNING: this will change between Pi versions
#Check yours first and adjust accordingly

GPIO.setup(gpio_pin_number, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#It's very important the pin is an input to avoid short-circuits
#The pull-up resistor means the pin is high by default

while True:
    input_state = GPIO.input(gpio_pin_number)
    time.sleep(0.5)
    print "input state", input_state
    #GPIO.setup(gpio_pin_number, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # if input_state == True:
    #     print('Careful!')
    #     time.sleep(2)
    #     input_state = GPIO.input(gpio_pin_number)
    #     if input_state == True:
    #         print('Bye!')
    #     else:
    #         print('Reseting Counter')
