# Draw some minecraft

# Predefined colors

0 = black
G = grey
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

# Image definitions

alex = [
    [o,o,o,o,o,o,o,o],
    [o,o,o,o,o,o,o,o],
    [o,o,o,o,y,y,o,o],
    [o,o,o,y,y,y,y,o],
    [y,w,g,y,y,g,w,y],
    [y,y,y,y,y,y,y,y],
    [y,y,y,m,m,y,y,y],
    [y,y,y,y,y,y,y,y],
]

creeper = [
    [g,g,g,g,g,g,g,g],
    [g,g,g,g,g,g,g,g],
    [g,0,0,g,g,0,0,g],
    [g,0,0,g,g,0,0,g],
    [g,g,g,0,0,g,g,g],
    [g,g,0,0,0,0,g,g],
    [g,g,0,g,g,0,g,g],
    [g,g,0,g,g,0,g,g],
]

mushroomcow = [
    [r,r,r,w,w,w,G,r],
    [r,r,r,w,w,w,r,r],
    [0,0,r,w,w,r,0,0],
    [0,0,r,G,r,r,0,0],
    [r,r,r,r,r,r,r,r],
    [r,r,w,w,w,w,r,r],
    [r,w,b,G,G,0,w,r],
    [r,w,G,0,0,G,w,r],
]

# Display images

display.set_panel("left", alex)
display.set_panel("right", creeper)
display.set_panel("top", mushroomcow)

