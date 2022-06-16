# Every 20 seconds scroll the time across the cube.

import datetime
display.set_all(black)
while True:
    time_text = datetime.datetime.now().strftime("%H:%M")
    display.scroll_text(time_text, orange)
    time.sleep(20)
