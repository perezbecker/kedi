from threading import Thread
import datetime
import time

global localtime


class getTime:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        global localtime
        while self._running:
            time.sleep(0.05)
            t = datetime.datetime.now()
            # if t.second % 2 == 0:
            #     set_decimal(2, 1)
            #     set_decimal(4, 1)
            # else:
            #     set_decimal(2, 0)
            #     set_decimal(4, 0)

            localtime = t.strftime('%H%M%S')




TimeTrack = getTime()
TimeThread = Thread(target=TimeTrack.run)
TimeThread.start()


cycle=0

localtime='0'



Exit = False #Exit flag

while Exit==False:
 cycle = cycle + 1
 print "CurrentTime", localtime
 time.sleep(1) #One second delay
 if (cycle > 5): Exit = True #Exit Program

TimeTrack.terminate()

print "Goodbye :)"
