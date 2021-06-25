# Rain animation

display.set_all(black)

rows = [[0 for x in range(16)] for y in range(8)]
while True:
	# Shift all rows down
	rows.pop(0)
	# Create a new row
	top_row = rows[-1]
	new_top_row = []
	for prev_pixel in top_row:
		new_pixel = 0
		# If previous pixel was start of drop
		# create droplet tail by reducing the brightness for the new pixel
		if prev_pixel > 0:
			new_pixel = prev_pixel - 0.4
			new_pixel = max(new_pixel, 0.0)
		# Generate new droplet
		elif random.random() < 0.1:
			new_pixel = 1
		new_top_row.append(new_pixel)
	rows.append(new_top_row)
	# Translate the rows of brightness values to led colours
	leds = {}
	for y in range(0,8):
		for x in range(0,16):
			leds[(x, y)] = hsv_colour(0.6, 1, rows[y][x])
	display.set_leds(leds)
	time.sleep(1/15)


