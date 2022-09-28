# Definition of time = https://docs.python.org/3/library/time.html
# Definition of random = https://docs.python.org/3/library/random.html

import time
import random

# Define some hex colors

black   = 0x000000
brown   = 0xA38000
grey    = 0x808080
lightgrey = 0xEFEDED
mediumgrey = 0xBBBBCC
white   = 0xFFFFFF
red     = 0xFF0000
orange  = 0xFF8C00
yellow  = 0xFFFF00
green   = 0x00FF00
cyan    = 0x00FFFF
blue    = 0x0000FF
magenta = 0xFF00FF
pink    = 0xFF007F
skin    = 0xF4CCCC
purple  = 0x800080

# Define shorts for the colors for easier handling

B = black
Br = brown
G = grey
lG = lightgrey
mG = mediumgrey
w = white
r = red
o = orange
y = yellow
g = green
c = cyan
b = blue
m = magenta
p = pink
P = purple
s = skin

# define the pixel/led images
#
#            top
#                        r
#   l                    i
#   e                    g
#   f                    h
#   t                    t
#           bottom

sheep = [
    [w,w,w,w,w,w,w,w],
    [w,lG,lG,mG,mG,mG,mG,w],
    [w,Br,Br,Br,Br,Br,Br,w],
    [w,B,w,Br,Br,w,B,w],
    [w,Br,Br,w,w,Br,Br,w],
    [w,lG,Br,s,s,Br,lG,w],
    [w,lG,Br,s,s,Br,lG,w],
    [w,w,w,w,w,w,w,w],
]

enderman = [
    [B,B,B,B,B,B,B,B],
    [B,B,B,B,B,B,B,B],
    [B,B,B,B,B,B,B,B],
    [B,B,B,B,B,B,B,B],
    [m,P,m,B,B,m,P,m],
    [B,B,B,B,B,B,B,B],
    [B,B,B,B,B,B,B,B],
    [B,B,B,B,B,B,B,B],
]

alex = [
    [o,o,o,o,o,o,o,o],
    [o,o,o,o,o,o,o,o],
    [o,o,o,o,s,s,o,o],
    [o,o,o,s,s,s,s,o],
    [s,B,w,s,s,B,w,s],
    [s,s,s,s,s,s,s,s],
    [s,s,s,m,m,s,s,s],
    [s,s,s,s,s,s,s,s],
]

creeper = [
    [g,g,g,g,g,g,g,g],
    [g,g,g,g,g,g,g,g],
    [g,B,B,g,g,B,B,g],
    [g,B,B,g,g,B,B,g],
    [g,g,g,B,B,g,g,g],
    [g,g,B,B,B,B,g,g],
    [g,g,B,g,g,B,g,g],
    [g,g,B,g,g,B,g,g],
]

mushroomcow = [
    [r,r,r,w,w,w,mG,r],
    [r,r,r,w,w,lG,r,r],
    [B,B,r,w,lG,r,B,B],
    [B,B,r,mG,r,r,B,B],
    [r,r,r,r,r,r,r,r],
    [r,r,w,w,w,w,r,r],
    [r,w,B,G,G,B,w,r],
    [r,w,G,B,B,G,w,r],
]

cow = [
    [Br,Br,Br,w,w,G,G,Br],
    [Br,Br,Br,Br,Br,Br,Br,Br],
    [lG,lG,Br,Br,Br,Br,Br,Br],
    [B,w,Br,Br,Br,Br,w,B],
    [Br,Br,Br,Br,Br,Br,Br,Br],
    [Br,Br,Br,Br,Br,Br,Br,Br],
    [Br,Br,Br,Br,Br,Br,Br,Br],
    [Br,Br,Br,Br,Br,Br,Br,Br],
]

cow = [
    [Br,Br,Br,Br,B,lG,Br,Br],
    [w,w,Br,Br,w,lG,Br,Br],
    [lG,B,w,Br,Br,Br,Br,Br],
    [lG,G,w,Br,Br,Br,w,w],
    [lG,G,w,Br,Br,Br,w,w],
    [lG,B,w,Br,Br,Br,lG,G],
    [w,w,Br,Br,w,lG,Br,G],
    [Br,Br,Br,Br,B,lG,Br,Br],
]

# Make a list named "items" of the images
# https://docs.python.org/3/tutorial/datastructures.html

items = [sheep, enderman, alex, creeper, cow, mushroomcow]

# Use "while" to create a loop
# https://docs.python.org/3/reference/compound_stmts.html?#while

# Take a random item out of the list
# https://docs.python.org/3/library/random.html?#random.choice

while True:
    random_item = random.choice(items)
    display.set_panel("left", random_item)
    random_item = random.choice(items)
    display.set_panel("right", random_item)
    random_item = random.choice(items)
    display.set_panel("top", random_item)
    time.sleep(10)

# Sleep for 10 seconds before returning to the beginning of the loop again



