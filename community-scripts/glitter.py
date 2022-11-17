# Note: make sure to put the brightness back down after running this script
display.brightness = 250

brightness = {}
def glitter_shader(x, y, frame):
    if x %2 == 0 or y % 2 == 0:
        return 0
    if (x,y) not in brightness:
        brightness[(x,y)] = 0
    if brightness[x,y] > 0:
        brightness[x,y] = brightness[x,y] - 0.05
        if brightness[x,y] < 0.1:
            brightness[x,y] = 0
    else:
        if random.random() < 1/50:
            brightness[x,y] = 1.0
    return hsv_colour(0.10, 0.8, brightness[x,y])

frame = 0;
while True:
    led_colours = {}
    for y in range(0,16):
        for x in range(0,16):
            if (x < 8) or (y < 8):
                led_colours[x,y] = glitter_shader(x,y,frame)
    display.set_leds(led_colours)
    frame+=1
    time.sleep(1/20)
    
