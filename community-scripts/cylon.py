# BSG Cylon with ever scanning eye
# best viewed from the front with left and right panels evently visible left and right to see the cylon "face"
# Author : Kevin Haney
# Date : 10/13/2022
# v1.0

import time

display.set_all(black)

m0 = hsv_colour(.198, .058, .46)
m1 = hsv_colour(.198, .058, .36)
m2 = hsv_colour(.198, .058, .26)
m3 = hsv_colour(.198, .058, .16)
m4 = hsv_colour(.198, .058, .06)
m5 = hsv_colour(.198, .058, .02)

bright_red = hsv_colour(0.0, .91, .86)
fade_red = hsv_colour(0.0, .91, .40)
pulse_red = hsv_colour(0.0, .30, .82)

leds = {}

delay = .07
longdelay = .25

# pre-build a dictionary in a nice order, and update it later - the cube doesn't like randomly ordered data for some reason
helmet = {}
for x in range(9):
    for y in range(9):
        helmet[(x,y,8)] = black
for x in range(9):
    for z in range(9):
        helmet[(x,8,z)] = black
for y in range(9):
    for z in range(9):
        helmet[(8,y,z)] = black

# the static helmet data
data = { 
    #left
    (0,7,8) : m3, (1,7,8) : m1, (2,7,8) : m0, (3,7,8) : m0, (4,7,8) : m0, (5,7,8) : m0, (6,7,8) : m0, (7,7,8) : m0, 
    (0,6,8) : m2,
    (0,5,8) : m3, (1,5,8) : m1, (2,5,8) : m0, (3,5,8) : m0, (4,5,8) : m0, (5,5,8) : m0, (6,5,8) : m0, (7,5,8) : m0,
    (0,4,8) : m5, (1,4,8) : m4, (2,4,8) : m2, (3,4,8) : m2, (4,4,8) : m2, (5,4,8) : m3, (6,4,8) : m4, (7,4,8) : m1, 
    (0,3,8) : m5, (1,3,8) : m4, (2,3,8) : m2, (3,3,8) : m2, (4,3,8) : m2, (5,3,8) : m3, (6,3,8) : m1, (7,3,8) : black, 
    (0,2,8) : m5, (1,2,8) : m4, (2,2,8) : m3, (3,2,8) : m2, (4,2,8) : m2, (5,2,8) : m3, (6,2,8) : m1, (7,2,8) : black, 
    (0,1,8) : black, (1,1,8) : m5, (2,1,8) : m3, (3,1,8) : m2, (4,1,8) : m3, (5,1,8) : m1, (6,1,8) : black, (7,1,8) : black, 
    (0,0,8) : black, (1,0,8) : m5, (2,0,8) : m3, (3,0,8) : m2, (4,0,8) : m3, (5,0,8) : m1, (6,0,8) : black, (7,0,8) : black, 
    #right
    (8,7,0) : m3, (8,7,1) : m1, (8,7,2) : m0, (8,7,3) : m0, (8,7,4) : m0, (8,7,5) : m0, (8,7,6) : m0, (8,7,7) : m0, 
    (8,6,0) : m2,
    (8,5,0) : m3, (8,5,1) : m1, (8,5,2) : m0, (8,5,3) : m0, (8,5,4) : m0, (8,5,5) : m0, (8,5,6) : m0, (8,5,7) : m0,
    (0,4,8) : m5, (8,4,1) : m4, (8,4,2) : m2, (8,4,3) : m2, (8,4,4) : m2, (8,4,5) : m3, (8,4,6) : m4, (8,4,7) : m1, 
    (0,3,8) : m5, (8,3,1) : m4, (8,3,2) : m2, (8,3,3) : m2, (8,3,4) : m2, (8,3,5) : m3, (8,3,6) : m1, (8,3,7) : black, 
    (0,2,8) : m5, (8,2,1) : m4, (8,2,2) : m3, (8,2,3) : m2, (8,2,4) : m2, (8,2,5) : m3, (8,2,6) : m1, (8,2,7) : black, 
    (0,1,8) : black, (8,1,1) : m5, (8,1,2) : m3, (8,1,3) : m2, (8,1,4) : m3, (8,1,5) : m1, (8,1,6) : black, (8,1,7) : black, 
    (0,0,8) : black, (8,0,1) : m5, (8,0,2) : m3, (8,0,3) : m2, (8,0,4) : m3, (8,0,5) : m1, (8,0,6) : black, (8,0,7) : black,
    #top
    (0,8,7) : m3, (0,8,6) : m4,
    (1,8,7) : m2, (1,8,6) : m2, (1,8,5) : m2, (1,8,4) : m1, (1,8,3) : m3,
    (2,8,7) : m1, (2,8,6) : m1, (2,8,5) : m1, (2,8,4) : m0, (2,8,3) : m0, (2,8,2) : m0,
    (3,8,7) : m1, (3,8,6) : m1, (3,8,5) : m0, (3,8,4) : m0, (3,8,3) : m0, (3,8,2) : m0, (3,8,1) : m2,
    (4,8,7) : m1, (4,8,6) : m0, (4,8,5) : m0, (4,8,4) : m0, (4,8,3) : m0, (4,8,2) : m0, (4,8,1) : m1,
    (5,8,7) : m1, (5,8,6) : m1, (5,8,5) : m0, (5,8,4) : m0, (5,8,3) : m0, (5,8,2) : m1, (5,8,1) : m1,
    (6,8,7) : m2, (6,8,6) : m2, (6,8,5) : m1, (6,8,4) : m0, (6,8,3) : m1, (6,8,2) : m1, (6,8,1) : m2, (6,8,0) : m4,
    (7,8,7) : m3, (7,8,6) : m2, (7,8,5) : m1, (7,8,4) : m1, (7,8,3) : m0, (7,8,2) : m1, (7,8,1) : m2, (7,8,0) : m3,
    (0,8,0) : black
}

for d in data:
    helmet[d] = data[d]
    
display.set_3d(helmet)

# scanning eye code.  I may put this into method that just handles the left and right on a flat plane, then use a map to convert o the cube
while True:
    for x in range(1,9):
        leds[(x,6,8)] = bright_red
        if x > 1:
            leds[(x-1,6,8)] = fade_red
        if x > 2:
            leds[(x-2,6,8)] = black
        display.set_3d(leds)
        time.sleep(delay)

    if x == 8:
        leds[(7,6,8)] = black
    
    for z in reversed(range(1,8)):
        leds[(8,6,z)] = bright_red
        if z < 7:
            leds[(8,6,z+1)] = fade_red
        if z < 6:
            leds[(8,6,z+2)] = black
        display.set_3d(leds)
        last = leds
        time.sleep(delay)

    leds[(8,6,2)] = black
    leds[(8,6,1)] = pulse_red
    display.set_3d(leds)

    time.sleep(longdelay)
    
    for z in range(1,9):
        leds[(8,6,z)] = bright_red
        if z > 1:
            leds[(8,6,z-1)] = fade_red
        if z > 2:
            leds[(8,6,z-2)] = black
        display.set_3d(leds)
        last = leds
        time.sleep(delay)
    if z == 7:
        leds[(8,6,6)] = black
    
    for x in reversed(range(1,9)):
        leds[(x,6,8)] = bright_red
        if x == 8:
            leds[(8,6,7)] = black
        if x < 8:
            leds[(x+1,6,8)] = fade_red
        if x < 7:
            leds[(x+2,6,8)] = black
        display.set_3d(leds)
        time.sleep(delay)

    leds[(2,6,8)] = black
    leds[(1,6,8)] = pulse_red
    display.set_3d(leds)

    time.sleep(longdelay)
