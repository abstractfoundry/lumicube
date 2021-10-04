# Continually change the cube's colour
import time

hue = 0
while True:
    hue += 0.01
    if hue > 1:
    	hue = 0
    display.set_all(hsv_colour(hue,1,1))
    time.sleep(1/20)
