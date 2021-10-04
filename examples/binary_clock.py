# Display a binary clock
# https://en.wikipedia.org/wiki/Binary_clock

def draw_binary_clock(hours, minutes, seconds):
    def draw_binary_value(value, x, colour, leds):
        # Split the time value into two separate digits
        digits = [int(value / 10), value % 10]
        for digit in digits:
            binary = list(bin(digit)[2:]) # Returns a list of 0's and 1's
            # Start at the bottom with the least significant digit
            # Loop through and set leds if the digit is 1
            binary.reverse()
            for i, value in enumerate(binary):
                y = i *2
                # Set all the leds in a 2x2 square
                positions = [
                    (x, y),
                    (x, y+1),
                    (x+1, y),
                    (x+1, y+1),
                ]
                for pos in positions:
                    if value == '1':
                        leds[pos] = colour
            # Increment x for the next digit
            x += 2
            
    leds = {}
    for y in range(0,16):
        for x in range(0,16):
            if x < 8 or y < 8:
                leds[(x,y)] = black
    draw_binary_value(hours,    0, pink,   leds)
    draw_binary_value(minutes,  6, purple, leds)
    draw_binary_value(seconds, 11, cyan,   leds)
    display.set_leds(leds)

display.set_all(black)
while True:
    import datetime
    import time
    time_now = datetime.datetime.now()
    seconds = int(time_now.strftime("%S"))
    minutes = int(time_now.strftime("%M"))
    hours   = int(time_now.strftime("%H"))
    draw_binary_clock(hours, minutes, seconds)
    time.sleep(1/10)

