import RPi.GPIO as GPIO
import time

class ButtonCounter:
  'Encapsulates the attributes and methods to use Kitts button'

  inputPin = 26
  ticks = 0

  def __init__(self, inputPin):
    self.inputPin = inputPin

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.IN,, pull_up_down=GPIO.PUD_DOWN)  #HARDCODED INPUTPIN (BUTTON)
    GPIO.add_event_detect(26, GPIO.RISING, callback=self.event_callback)

  def getTicks(self):
    return self.ticks

  def resetTicks(self):
    self.ticks = 0

  def event_callback(self,channel):
    self.ticks += 1
