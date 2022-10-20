# Volcano simulation
# Random lava flows, projectiles, rumbling...
# Author : Kevin Haney
# Date : 10/20/2022
# v1.0

import time

display.set_all(black)

b0 = hsv_colour(.0, .0, .750)
b1 = hsv_colour(.0, .0, .650)
b2 = hsv_colour(.0, .0, .550)
b3 = hsv_colour(.0, .0, .450)
b4 = hsv_colour(.0, .0, .350)
b5 = hsv_colour(.0, .0, .250)
b6 = hsv_colour(.0, .0, .150)

cone = {
    #top
                                (1,8,5) : b6, (1,8,4) : b5, (1,8,3) : b6, (2,8,2) : b6, 
                  (2,8,6) : b5, (2,8,5) : b3, (2,8,4) : b3, (2,8,3) : b4, (2,8,2) : b6, 
    (3,8,7) : b5, (3,8,6) : b5, (3,8,5) : b5,               (3,8,3) : b5, (3,8,2) : b4, (3,8,1) : b6,
    (4,8,7) : b5, (4,8,6) : b4,                                           (4,8,2) : b3, (4,8,1) : b5,
    (5,8,7) : b3, (5,8,6) : b3, (5,8,5) : b5,               (5,8,3) : b5, (5,8,2) : b3, (5,8,1) : b6,
    (6,8,7) : b2, (6,8,6) : b2, (6,8,5) : b3, (6,8,4) : b4, (6,8,3) : b3, (6,8,2) : b5,
    (7,8,7) : b3, (7,8,6) : b2, (7,8,5) : b2, (7,8,4) : b5, (7,8,3) : b6,
    #left
    (7,7,8) : b2, (7,6,8) : b1, (7,5,8) : b1, (7,4,8) : b1, (7,3,8) : b2, (7,2,8) : b3, (7,1,8) : b0, (7,0,8) : b0,
    (6,7,8) : b5, (6,6,8) : b2, (6,5,8) : b1, (6,4,8) : b1, (6,3,8) : b1, (6,2,8) : b0, (6,1,8) : b2, (6,0,8) : b3,
    (5,7,8) : b4, (5,6,8) : b5, (5,5,8) : b4, (5,4,8) : b1, (5,3,8) : b1, (5,2,8) : b1, (5,1,8) : b0, (5,0,8) : b0,
    (4,7,8) : b5, (4,6,8) : b4, (4,5,8) : b3, (4,4,8) : b4, (4,3,8) : b4, (4,2,8) : b3, (4,1,8) : b1, (4,0,8) : b0,
    (3,7,8) : b6, (3,6,8) : b5, (3,5,8) : b4, (3,4,8) : b3, (3,3,8) : b2, (3,2,8) : b1, (3,1,8) : b3, (3,0,8) : b0,
                                (2,5,8) : b6, (2,4,8) : b5, (2,3,8) : b4, (2,2,8) : b2, (2,1,8) : b1, (2,0,8) : b3,
                                              (1,4,8) : b6, (1,3,8) : b5, (1,2,8) : b3, (1,1,8) : b2, (1,0,8) : b1,
                                                            (0,3,8) : b6, (0,2,8) : b5, (0,1,8) : b3, (0,0,8) : b2,
    #right
    (8,7,7) : b2, (8,6,7) : b1, (8,5,7) : b1, (8,4,7) : b1, (8,3,7) : b2, (8,2,7) : b3, (8,1,7) : b0, (8,0,7) : b0,
    (8,7,6) : b5, (8,6,6) : b2, (8,5,6) : b1, (8,4,6) : b1, (8,3,6) : b1, (8,2,6) : b0, (8,1,6) : b2, (8,0,6) : b3,
    (8,7,5) : b4, (8,6,5) : b5, (8,5,5) : b4, (8,4,5) : b1, (8,3,5) : b1, (8,2,5) : b1, (8,1,5) : b0, (8,0,5) : b0,
    (8,7,4) : b5, (8,6,4) : b4, (8,5,4) : b3, (8,4,4) : b4, (8,3,4) : b4, (8,2,4) : b3, (8,1,4) : b1, (8,0,4) : b0,
    (8,7,3) : b6, (8,6,3) : b5, (8,5,3) : b4, (8,4,3) : b3, (8,3,3) : b2, (8,2,3) : b1, (8,1,3) : b3, (8,0,3) : b0,
                                (8,5,2) : b6, (8,4,2) : b5, (8,3,2) : b4, (8,2,2) : b2, (8,1,2) : b1, (8,0,2) : b3,
                                              (8,4,1) : b6, (8,3,1) : b5, (8,2,1) : b3, (8,1,1) : b2, (8,0,1) : b1,
                                                            (8,3,0) : b6, (8,2,0) : b5, (8,1,0) : b3, (8,0,0) : b2
}

lava0 = [
    (3,8,5), (2,8,6), (2,8,7) , (2,7,8), (2,6,8), (2,5,8), (1,5,8), (2,5,8), (1,5,8), (1,4,8), (1,4,8), (0,4,8), (0,4,8), (0,3,8)
]

lava1 = [
    (4,8,6), (5,8,6), (4,8,7) , (5,8,7), (4,7,8), (5,7,8), (4,6,8), (4,5,8), (3,4,8), (5,4,8),
    (3,3,8), (5,3,8), (3,2,8) , (5,2,8), (2,1,8), (5,1,8), (1,0,8), (5,0,8), (0,0,8), (4,0,8), (4,0,8), (4,1,8), (3,0,8), (4,0,8)
]

lava2 = [
    (5,8,5), (6,8,6), (5,8,6), (6,8,5), (6,8,6), (6,8,7), (7,8,6), (7,8,7), (7,7,8), (7,7,8), (7,6,8), (8,7,7), (7,5,8), (8,6,7),
    (7,4,8), (8,5,7), (7,3,8), (8,4,7), (7,3,8), (8,3,7), (6,3,8), (8,3,7), (6,3,8), (8,3,6), (6,2,8), (8,2,6), (5,2,8), (8,2,6),
    (5,1,8), (8,2,5), (6,1,8), (8,1,5), (5,0,8), (8,1,6), (4,0,8), (8,0,6), (4,1,8), (8,0,5), (4,0,8), (8,0,4), (3,0,8), (8,0,7)
]

lava3 = [
    (6,8,5), (6,8,4), (7,8,5) , (7,8,4), (8,7,5), (8,7,4), (8,6,5), (8,6,4), (8,5,4), (8,5,3),
    (8,4,4), (8,4,3), (8,3,3) , (8,3,2), (8,2,3), (8,2,2), (8,1,2), (8,1,1), (8,0,3), (8,0,1), (8,0,2), (8,0,0)
]

lava4 = [
    (5,8,3), (6,8,2), (7,8,8) , (8,7,2), (8,6,2), (8,5,2), (8,5,1), (8,5,2), (8,5,1), (8,4,1), (8,4,1), (8,4,0), (8,4,0), (8,3,0)
]

flows = [
    lava0,
    lava1,
    lava2,
    lava3,
    lava4
]

def LedDictionary():
    leds = {}
    for x in range(9):
        for y in range(9):
            for z in range(9):
                leds[x,y,z] = blue
    return leds

def Shift(direction, leds):
    if direction == "left":
        #left side
        for x in range(0,7):
            for y in range(8):
                leds[x,y,8] = leds[x+1,y,8]
        #right side
        for y in range(8):
            for z in reversed(range(1,8)):
                leds[8,y,z] = leds[8,y,z-1]
        #fill in on right
        leds[8,0,0] = b5
        leds[8,1,0] = b5
        leds[8,2,0] = blue
        leds[8,3,0] = blue
        #top
        for x in range(8):
            for z in reversed(range(1,7)):
                leds[x,8,z] = leds[x,8,z-1]
    else:
        #left side
        for x in reversed(range(1,8)):
            for y in range(8):
                leds[x,y,8] = leds[x-1,y,8]
        #right side
        for y in range(8):
            for z in (range(0,7)):
                leds[8,y,z] = leds[8,y,z+1]
        #fill in on the left
        leds[0,0,8] = b5
        leds[0,1,8] = b5
        leds[0,2,8] = blue
        leds[0,3,8] = blue
        #top
        for x in reversed(range(1,8)):
            for z in range(8):
                leds[x,8,z] = leds[x-1,8,z]

    return leds
    
def Shake(leds):
    left = Shift("left",leds.copy())
    right = Shift("right",leds.copy())
    
    for i in range(7):
        display.set_3d(left)
        time.sleep(random.randrange(1,3)/10)
        display.set_3d(leds)
        time.sleep(random.randrange(1,3)/10)
        display.set_3d(right)
        time.sleep(random.randrange(1,3)/10)

    display.set_3d(leds)

def RandomBubbleColor():
    return hsv_colour(random.randrange(0,5)/100, random.randrange(50,100)/100, random.randrange(60,100)/100)

def RandomFlowColor():
    return hsv_colour(random.randrange(0,5)/100, random.randrange(60,100)/100, random.randrange(80,100)/100)

def Bubble(count, leds, sleep):
    for c in range(count):
        for x in range(3,6):
            for z in range(3,6):
                leds[x,8,z] = RandomBubbleColor()
        display.set_3d(leds)
        if sleep:
            time.sleep(random.randrange(3,7)/10)
        
def Flow(leds, lava):
    copy = leds.copy()
    Bubble(1,copy,False)
    pairs = int(len(lava)/2)
    # flow them on
    for p in range(pairs+1):
        # draw 2 at a time
        for l in range(p*2):
            copy[lava[l]] = RandomFlowColor()
        Bubble(1,copy,False)
        display.set_3d(copy)
        time.sleep(.9)
    # refresh all colors a few times
    for i in range(6):
        for l in range(len(lava)):
            copy[lava[l]] = RandomFlowColor()
        Bubble(1,copy,False)
        display.set_3d(copy)
        time.sleep(.9)
    # flow them off 
    for p in range(1,pairs+1):
        copy = leds.copy()
        for l in range(p*2,pairs*2):
            copy[lava[l]] = RandomFlowColor()
        Bubble(1,copy,False)
        display.set_3d(copy)
        time.sleep(.9)


def main():
    leds = LedDictionary()
    
    for key, value in cone.items():
        leds[key] = value
    
    display.set_3d(leds)
    
    shakeEvery = 5
    shake = 0
    
    while True:
        Bubble(random.randrange(5,8), leds, True)
        shake += 1
        if shake >= shakeEvery:
            shake = 0
            Shake(leds)
            flow = 1#random.randrange(0,len(flows))
            Flow(leds, flows[flow])

if __name__ == "__main__":
    main()