# Write some statistics about the Pi to the the screen.

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
