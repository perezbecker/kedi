import time
from microdotphat import write_string, scroll, clear, show

clear()
write_string('Forecast, SNOWCATS!   ')

while True:
    scroll()
    show()
    time.sleep(0.01)
