# Display a clock in resistor colour code
# By Sean Kelly

def fill_panel(panel,n1,n2):
    display.set_panel(panel, [[b, b, b, b, b, b, b, b],
                                   [b, n1, n1, n1, n2, n2, n2, b],
                                   [b, n1, n1, n1, n2, n2, n2, b],
                                   [wires, n1, n1, n1, n2, n2, n2, wires],
                                   [wires, n1, n1, n1, n2, n2, n2, wires],
                                   [b, n1, n1, n1, n2, n2, n2, b],
                                   [b, n1, n1, n1, n2, n2, n2, b],
                                   [b, b, b, b, b, b, b, b]])

# initialise
import datetime
display.set_all(black)
lastminute = 99
lasthour = 25

# number and colour definitions
brown = 0xAB784E
violet = 0x9B26B6
border = 0xDED1A6
b = border
wires = 0x444444
dimblack = 0x101010
colourlist = [dimblack,brown,red,orange,yellow,green,blue,violet,grey,white]

# main loop
while True:
    time_now = datetime.datetime.now()
    seconds = int(format(time_now.second))
    minutes = int(format(time_now.minute))
    hours = int(format(time_now.hour))
    fill_panel("top",colourlist[int(seconds/10)],colourlist[seconds % 10])
    if lastminute != minutes:
        fill_panel("right",colourlist[int(minutes/10)],colourlist[minutes % 10])
        lastminute = minutes
    if hours != lasthour:
        fill_panel("left",colourlist[int(hours/10)],colourlist[hours % 10])
        lasthour = hours
    time.sleep(1)
