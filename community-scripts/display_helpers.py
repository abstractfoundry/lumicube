# Display helper code
# Author : Kevin Haney
# Date : 11/23/2922
# Version : 1.0
#
from string import whitespace

# digits are defined as bits on in a 3x5 grid, 0,0 =bottomleft
digitAll = [ (0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2), (3,0), (3,1), (3,2), (4,0), (4,1), (4,2)]
digit =   [[ (0,0), (0,1), (0,2), (1,0),        (1,2), (2,0),        (2,2), (3,0),        (3,2), (4,0), (4,1), (4,2)],
           [        (0,1),               (1,1),               (2,1),               (3,1),               (4,1)       ],
           [ (0,0), (0,1), (0,2), (1,0),               (2,0), (2,1), (2,2),               (3,2), (4,0), (4,1), (4,2)],
           [ (0,0), (0,1), (0,2),               (1,2), (2,0), (2,1), (2,2),               (3,2), (4,0), (4,1), (4,2)],
           [               (0,2),               (1,2), (2,0), (2,1), (2,2), (3,0),        (3,2), (4,0),        (4,2)],
           [ (0,0), (0,1), (0,2),               (1,2), (2,0), (2,1), (2,2), (3,0),               (4,0), (4,1), (4,2)],
           [ (0,0), (0,1), (0,2), (1,0),        (1,2), (2,0), (2,1), (2,2), (3,0),               (4,0)              ],
           [               (0,2),               (1,2),               (2,2),               (3,2), (4,0), (4,1), (4,2)],
           [ (0,0), (0,1), (0,2), (1,0),        (1,2), (2,0), (2,1), (2,2), (3,0),        (3,2), (4,0), (4,1), (4,2)],
           [               (0,2),               (1,2), (2,0), (2,1), (2,2), (3,0),        (3,2), (4,0), (4,1), (4,2)]]
# x and y from bottom left
leftOnesLeds = [[(5,2),(6,2),(7,2)],[(5,3),(6,3),(7,3)],[(5,4),(6,4),(7,4)],[(5,5),(6,5),(7,5)],[(5,6),(6,6),(7,6)]]
leftTensLeds = [[(1,2),(2,2),(3,2)],[(1,3),(2,3),(3,3)],[(1,4),(2,4),(3,4)],[(1,5),(2,5),(3,5)],[(1,6),(2,6),(3,6)]]
# z and y from bottom left
rightOnesLeds = [[(2,2),(1,2),(0,2)],[(2,3),(1,3),(0,3)],[(2,4),(1,4),(0,4)],[(2,5),(1,5),(0,5)],[(2,6),(1,6),(0,6)]]
rightTensLeds = [[(6,2),(5,2),(4,2)],[(6,3),(5,3),(4,3)],[(6,4),(5,4),(4,4)],[(6,5),(5,5),(4,5)],[(6,6),(5,6),(4,6)]]

def clear_left(all_leds, background_color):
    for x in range(9):
        for y in range(9):
            all_leds[(x,y,8)] = background_color

def clear_right(all_leds, background_color):
    for y in range(9):
        for z in range(9):
            all_leds[(8,y,z)] = background_color

def set_left(all_leds, value_leds, value_color, background_color, clear=False):
    if clear:
        clear_left(all_leds, background_color)
    for v in value_leds:
        all_leds[(v[0],v[1],v[2])] = value_color
    
def set_right(all_leds, value_leds, value_color, background_color, clear=False):
    if clear:
        clear_right(all_leds, background_color)
    for v in value_leds:
        all_leds[(v[0],v[1],v[2])] = value_color
    
def clear_digits(all_leds, side, background):
    if side == 'right':
        clear_right(all_leds, background)
    else:
        clear_left(all_leds, background)

def set_digits(all_leds, side, total, color, background):
    clear_digits(all_leds, side, background)
    if total == None:
        return
        
    ones = total % 10
    tens = total // 10
    shift = 0
    if tens == 0:
        shift = 1
    
    if side == 'right':
        onesLeds = rightOnesLeds
        tensLeds = rightTensLeds
    else:
        onesLeds = leftOnesLeds
        tensLeds = leftTensLeds
    
    for point in range(len(digit[ones])):
        pair = onesLeds[digit[ones][point][0]][digit[ones][point][1]]
        h = pair[0]
        v = pair[1]
        if side == 'right':
            all_leds[(8,v,h+shift)] = color
        else:
            all_leds[(h-shift,v,8)] = color
        
    if tens > 0:
        for point in range(len(digit[tens])):
            pair = tensLeds[digit[tens][point][0]][digit[tens][point][1]]
            h = pair[0]
            v = pair[1]
            if side == 'right':
                all_leds[(8,v,h+shift)] = color
            else:
                all_leds[(h-shift,v,8)] = color

if __name__ == "__main__":
    display.set_all(black)

    # initialize our led dictionary
    leds = {}
    for x in range(9):
        for y in range(9):
            for z in range(9):
                leds[(x,y,z)] = black

    display.set_3d(leds)

    for t in range(100):
        set_digits(leds,'right',t,white,orange)
        set_digits(leds,'left',99-t,white,blue)
        display.set_3d(leds)
        time.sleep(.1)
