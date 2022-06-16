# Display a binary clock (https://en.wikipedia.org/wiki/Binary_clock).

def draw_column(decimal_digit, x, colour):
    # Convert digit to four digit binary
    binary = list(format(decimal_digit, '04b'))
    # Start at the bottom with the least significant digit
    binary.reverse()
    leds = {}
    for i, value in enumerate(binary):
        # Set all the leds in a 2x2 square
        pixel = colour if value == '1' else black
        y = i * 2
        leds[x,   y  ] = pixel
        leds[x,   y+1] = pixel
        leds[x+1, y  ] = pixel
        leds[x+1, y+1] = pixel
    display.set_leds(leds)

import datetime
display.set_all(black)
while True:
    time_now = datetime.datetime.now()
    seconds = format(time_now.second, '02')
    minutes = format(time_now.minute, '02')
    hours   = format(time_now.hour,   '02')
    draw_column(int(hours[0]),    0, pink)
    draw_column(int(hours[1]),    2, pink)
    draw_column(int(minutes[0]),  4, purple)
    draw_column(int(minutes[1]),  6, purple)
    draw_column(int(seconds[0]),  8, cyan)
    draw_column(int(seconds[1]), 10, cyan)
    time.sleep(1/10)
