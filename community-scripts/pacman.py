c = cyan
y = yellow
pacman_and_ghost = [
    [0,c,c,c,c,c,0,0, 0,0,y,y,y,y,0,0,],
    [c,c,c,c,c,c,c,0, 0,y,y,y,y,y,y,0,],
    [c,0,c,c,0,c,c,0, y,y,0,y,y,y,y,0,],
    [c,0,0,c,0,0,c,0, y,y,y,y,y,y,0,0,],
    [c,c,c,c,c,c,c,0, y,y,y,y,y,0,0,0,],
    [c,c,c,c,c,c,c,0, y,y,y,y,y,y,0,0,],
    [c,c,c,c,c,c,c,0, 0,y,y,y,y,y,y,0,],
    [c,0,c,0,c,0,c,0, 0,0,y,y,y,y,0,0,],
]

while True:
    display.set_all(black)
    leds = {}
    for frame in range(0,32):
        for y in range(0, 8):
            for x in range(0, 16):
                x1 = x - frame + 15
                if x1 >= 0 and x1 < 16:
                    leds[x, y] = pacman_and_ghost[7 - y][x1]
                else:
                    leds[x, y] = black
        display.set_leds(leds)
        time.sleep(1/10)
    
