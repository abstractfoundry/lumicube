# Identify panels: left, red; right, green; top blue.

display.set_panel("left", [[red, red, red, red, red, red, red, red],
                                   [red, red, cyan, red, red, red, red, red],
                                   [red, red, cyan, red, red, red, red, red],
                                   [red, red, cyan, red, red, red, red, red],
                                   [red, red, cyan, red, red, red, red, red],
                                   [red, red, cyan, red, red, red, red, red],
                                   [red, red, cyan, cyan, cyan, cyan, red, red],
                                   [red, red, red, red, red, red, red, red]])
display.set_panel("right", [[green, green, green, green, green, green, green, green],
                                   [green, green, magenta, magenta, magenta, green, green, green],
                                   [green, green, magenta, green, green, magenta, green, green],
                                   [green, green, magenta, green, green, magenta, green, green],
                                   [green, green, magenta, magenta, magenta, green, green, green],
                                   [green, green, magenta, green, green, magenta, green, green],
                                   [green, green, magenta, green, green, magenta, green, green],
                                   [green, green, green, green, green, green, green, green]])
display.set_panel("top", [[blue, blue, blue, blue, blue, blue, blue, blue],
                                   [blue, blue, yellow, yellow, yellow, blue, blue, blue],
                                   [blue, blue, blue, yellow, blue, blue, blue, blue],
                                   [blue, blue, blue, yellow, blue, blue, blue, blue],
                                   [blue, blue, blue, yellow, blue, blue, blue, blue],
                                   [blue, blue, blue, yellow, blue, blue, blue, blue],
                                   [blue, blue, blue, yellow, blue, blue, blue, blue],
                                   [blue, blue, blue, blue, blue, blue, blue, blue]])
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

