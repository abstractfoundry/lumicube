# Identify panels: left, red; right, green; top blue; and shared corners

display.set_panel("left", [[grey, red, red, red, red, red, red, white],
                                   [red, red, cyan, red, red, red, red, red],
                                   [red, red, cyan, red, red, red, red, red],
                                   [red, red, cyan, red, red, red, red, red],
                                   [red, red, cyan, red, red, red, red, red],
                                   [red, red, cyan, red, red, red, red, red],
                                   [red, red, cyan, cyan, cyan, cyan, red, red],
                                   [red, red, red, red, red, red, red, orange]])
display.set_panel("right", [[white, green, green, green, green, green, green, pink],
                                   [green, green, magenta, magenta, magenta, green, green, green],
                                   [green, green, magenta, green, green, magenta, green, green],
                                   [green, green, magenta, green, green, magenta, green, green],
                                   [green, green, magenta, magenta, magenta, green, green, green],
                                   [green, green, magenta, green, green, magenta, green, green],
                                   [green, green, magenta, green, green, magenta, green, green],
                                   [orange, green, green, green, green, green, green, green]])
display.set_panel("top", [[blue, blue, blue, blue, blue, blue, blue, pink],
                                   [blue, blue, yellow, yellow, yellow, blue, blue, blue],
                                   [blue, blue, blue, yellow, blue, blue, blue, blue],
                                   [blue, blue, blue, yellow, blue, blue, blue, blue],
                                   [blue, blue, blue, yellow, blue, blue, blue, blue],
                                   [blue, blue, blue, yellow, blue, blue, blue, blue],
                                   [blue, blue, blue, yellow, blue, blue, blue, blue],
                                   [grey, blue, blue, blue, blue, blue, blue, white]])
# Display status on screen

def to_text(value):
    return str("{:.1f}".format(value))

screen.draw_rectangle(0, 0, 320, 240, black)
height = 36
while True:
    text = ("IP address: " + pi.ip_address() + "\n"
        + "CPU temp  : " + to_text(pi.cpu_temp()) + "\n"
        + "CPU usage : " + to_text(pi.cpu_percent()) + "\n"
        + "RAM usage : " + to_text(pi.ram_percent_used()) +"\n"
        + "Disk usage: " + to_text(pi.disk_percent()) + "\n")
    screen.write_text(10, 18, text, 1, white, black)
    time.sleep(5)
