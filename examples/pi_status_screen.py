# Display some pi stats on the screen

# Set the screen black
screen.draw_rectangle(0, 0, 320, 240, black)
height = 36
while True:
    # Every 20 seconds write the pi stats to the screen
    (days, hours, minutes, seconds) = pi.uptime()
    screen.write_text(0, 0.5*height, "IP Address: " + pi.ip_address(),                                   1, white, black)
    screen.write_text(0, 1.5*height, "CPU temp  : " + str("{:.1f}".format(pi.cpu_temp())) + "'C",        1, white, black)
    screen.write_text(0, 2.5*height, "CPU usage : " + str("{:.1f}".format(pi.cpu_percent())) + "%",      1, white, black)
    screen.write_text(0, 3.5*height, "RAM usage : " + str("{:.1f}".format(pi.ram_percent_used())) + "%", 1, white, black)
    screen.write_text(0, 4.5*height, "Disk usage: " + str("{:.1f}".format(pi.disk_percent())) + "%",     1, white, black)
    screen.write_text(0, 5.5*height, "Uptime    : " + str(days) + ":" + str(hours) + ":" + str(minutes), 1, white, black)
    time.sleep(20)