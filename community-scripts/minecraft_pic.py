# Draw some minecraft

# Predefined colors

B = black
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
    [r,r,r,w,w,w,G,r],
    [r,r,r,w,w,w,r,r],
    [B,B,r,w,w,r,B,B],
    [B,B,r,G,r,r,B,B],
    [r,r,r,r,r,r,r,r],
    [r,r,w,w,w,w,r,r],
    [r,w,B,G,G,B,w,r],
    [r,w,G,B,B,G,w,r],
]

# Display images

display.set_panel("left", alex)
display.set_panel("right", creeper)
display.set_panel("top", mushroomcow)

