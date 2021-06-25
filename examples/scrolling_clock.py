# Every 10 seconds scroll the time across the LEDs

display.set_all(black)
while True:
    import datetime
    time_string = datetime.datetime.now().strftime("%H:%M")
    display.scroll_text(time_string, pink)
    time.sleep(10)