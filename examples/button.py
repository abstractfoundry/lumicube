# If the top button has been pressed an even number of times set the cube red,
# otherwise set it blue.

while True:
    if buttons.top_pressed_count % 2 == 0:
        display.set_all(red)
    else:
        display.set_all(blue)
    time.sleep(1 / 20)
