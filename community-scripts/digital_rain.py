# Digital Rain (matrix screen effect)
# v2.0
# builds 8 random streams which "rain" down from the top to the sides.
# supports v1 mode (rain down from the top to the left side, overflow from left onto right) or 
# v2 mode (rain down diagonally from the top, over both sides)
# set Diagonally to true or false as you prefer.
# Author: Kevin Haney
# Date: 10/10/2022
# history:
# - 1.0 - original (v1)
# - 2.0 - diagonal scrolling added (v2)
# - 2.1 - some code cleanup and fixed right scrolling

import random

# set to True to rain down diagonally from the top (v2 mode), False  to rain down to the left (v1) 
Diagonally = True

class Point:
    def __init__(self, column, row, hue, saturation, brightness):
        self.column = column
        self.row = row
        self.hue = self._check(hue)
        self.color = black
        self.saturation = self._check(saturation)
        self.brightness = self._check(brightness)
        
    def _check(self,value):
        if value > 1:
            return 1
        elif value < 0:
            return 0
        else:
            return value
            
class Stream:
    def __init__(self, column, saturation, brightness, speed, length):
        self.column = column
        self.saturation = saturation
        self.brightness = brightness
        self.position = 0
        self.speed = speed
        self.length = length
        self.pause = 0
        
        self.points = []

        # brightness tapers off after 1/2
        bdelta = brightness / (self.length / 2)

        # front pad a random number of cells so they don't all "start" at the same time
        pad = random.randrange(5,12)

        for row in reversed(range (0,self.length)):
            sat = self.saturation + random.randrange(-15,16)/100
            if row > (self.length / 2) - 2:
                adjust = (row/2)*bdelta
                bright = self.brightness - adjust
                if bright < 0:
                    bright = 0
            else:
                bright = self.brightness + random.randrange(-25,26)/100
            hue = .3 # green
            if (row == pad):
                hue = .15
            if row < pad:
                bright = 0
            
            self.points.append(Point(column,row,hue,sat,bright))
            
    # grab a window of 16/24 points to display, moving from bottom to top
    # not crazy how this abruplty ends the stream though - I'd like those to scroll off too
    def rain(self):
        update = False
        if self.pause == 0:
            self.position += 1
            self.pause = self.speed
            update = True
        else:
            self.pause -= 1
        if self.position >= self.length:
            self.position = 1
        first = self.length - self.position
        last = first + self.position - 1
        lastRow = 23
        if Diagonally:
            lastRow = 15
        if last - first > lastRow:
            last = first + lastRow
        if update:
            row = 0
            for i in range(first,last+1):
                p = self.points[i]
                p.row = row
                # random adjustment of sat and brighness? given the motion it seems like overkill
                sat = p.saturation # + random.randrange(-15,16)/100
                bright = p.brightness # + random.randrange(-25,26)/100
                p.color = hsv_colour(p.hue, sat, bright)
                row += 1
            
        return self.points[first:last+1]
            
def map(point):
    x = point.column
    y = 15-point.row
    # left screen overflow onto right screen
    if point.row > 15:
        x = x + 8
        y = y + 8
    return x, y
    
def mapV2(point,lookup):
    # left
    if (point.column < 7 or point.column == 15) and point.row > 7:
        x = point.column + 1
        if (point.column == 15):
            x = 0
        y = 15 - point.row
    # right
    elif (point.column > 6 and point.column < 15) and point.row > 7:
        x = point.column
        if x == 7:
            x += 8 # throw the center stream over to the far right
        y = 15 - point.row
    else:
        if (point.column, point.row) in lookup:
            l = lookup[(point.column,point.row)]
            #print(l)
            x = l[0]
            y = l[1]
        else:
            x = -1
            y = -1
            
    return x, y

def BuildLookup():
    lookup = { 
        (0,7) : (0,8), (1,6) : (0,9), (2,5) : (0,10), (3,4)  : (0,11), (4,3)  : (0,12), (5,2)  : (0,13), (6,1)  : (0,14), (7,0)  : (0,15), 
        (1,7) : (1,8), (2,6) : (1,9), (3,5) : (1,10), (4,4)  : (1,11), (5,3)  : (1,12), (6,2)  : (1,13), (7,1)  : (1,14), (8,1)  : (1,15), 
        (2,7) : (2,8), (3,6) : (2,9), (4,5) : (2,10), (5,4)  : (2,11), (6,3)  : (2,12), (7,2)  : (2,13), (8,2)  : (2,14), (9,2)  : (2,15), 
        (3,7) : (3,8), (4,6) : (3,9), (5,5) : (3,10), (6,4)  : (3,11), (7,3)  : (3,12), (8,3)  : (3,13), (9,3)  : (3,14), (10,3) : (3,15), 
        (4,7) : (4,8), (5,6) : (4,9), (6,5) : (4,10), (7,4)  : (4,11), (8,4)  : (4,12), (9,4)  : (4,13), (10,4) : (4,14), (11,4) : (4,15), 
        (5,7) : (5,8), (6,6) : (5,9), (7,5) : (5,10), (8,5)  : (5,11), (9,5)  : (5,12), (10,5) : (5,13), (11,5) : (5,14), (12,5) : (5,15), 
        (6,7) : (6,8), (7,6) : (6,9), (8,6) : (6,10), (9,7)  : (6,11), (10,6) : (6,12), (11,6) : (6,13), (12,6) : (6,14), (13,6) : (6,15), 
        (7,7) : (7,8), (8,7) : (7,9), (9,7) : (7,10), (10,7) : (7,11), (11,7) : (7,12), (12,7) : (7,13), (13,7) : (7,14), (14,7) : (7,15) 
    }
    return lookup


def LedDictionary():
    leds = {}
    for x in range(0,16):
        for y in range(0,16):
            if x < 8 or (x > 7 and y < 8):
                leds[x,y] = 0
    return leds
    
# main code

display.set_all(black)

lookup = BuildLookup()

maxStreams = 8
if Diagonally:
    maxStreams = 16
    
streams = []
for s in range(0,maxStreams):
    streams.append(Stream(s, random.randrange(45,66)/100, random.randrange(35,86)/100, random.randrange(0,3), random.randrange(32,43)))

while True:
    # need a pre-ordered dictionary of points because I'm not setting them in an order the cube code likes (unordered = crash!)
    leds = LedDictionary()
    for stream in streams:
        drops = stream.rain()
        for d in drops:
            if Diagonally:
                m = mapV2(d,lookup)
            else:
                m = map(d)
            if m[0] != -1:
                #print ("v2 map from",d.column,d.row,"to",m[0],m[1])
                leds[m[0], m[1]] = d.color

    display.set_leds(leds)
    time.sleep(.25)