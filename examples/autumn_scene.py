# Autumn animation

# Set the leds to Tree image with a moon
y = 0xffc000
o = 0xff9000
r = hsv_colour(0.04, 1, 1)
b = hsv_colour(0.04, 0.7, 0.3)
w = hsv_colour(0, 0, 1)
top = [
	[0,w,0,0,0,0,0,0],
	[w,0,0,0,0,0,0,0],
	[w,0,0,0,0,0,o,r],
	[0,w,0,0,o,o,o,o],
	[0,0,0,o,o,r,o,o],
	[0,0,0,o,o,o,o,o],
	[0,0,o,o,r,o,y,o],
	[0,0,o,o,o,o,o,o],
]
left = [
	[0,0,o,o,y,o,r,o],
	[0,0,0,r,o,o,o,o],
	[0,0,0,0,0,o,o,y],
	[0,0,0,0,0,0,0,b],
	[0,0,0,0,0,0,0,b],
	[0,0,0,0,0,0,0,b],
	[0,0,0,0,0,0,0,b],
	[0,0,0,0,0,0,b,b],
]
right = [
	[o,r,o,y,o,o,0,0],
	[o,o,o,o,r,0,0,0],
	[y,o,o,0,0,0,0,0],
	[b,0,0,0,0,0,0,0],
	[b,0,0,0,0,0,0,0],
	[b,0,0,0,0,0,0,0],
	[b,0,0,0,0,0,0,0],
	[b,b,0,0,0,0,0,0],
]
display.set_panel(0, left)
display.set_panel(1, right)
display.set_panel(2, top)

# Make an animation of leaves falling to the floor
leaves = {}
while True:
	# 30% chance of creating a new falling leaf
	if random.random() < 0.3:
		# Start at a random position in tree
		y = 7
		x = random.randint(2,6)
		if (random.random() < 0.5):
			x += 8
		leaves[(x,y)] = hsv_colour(0.04 + 0.12*random.random(), 1, 1)
	
	# Move all falling leaves
	leds = {}
	new_leaves = {}
	for (x,y), colour in leaves.items():
		if y > 0:
			# If leaf has moved set it's old position back to the image
			if x < 8:
				leds[(x,y)] = left[7-y][x]
			else:
				leds[(x,y)] = right[7-y][x-8]
			# Move leaf side to side as it falls
			if y % 2 == 0:
				x = x + 1
			else:
				x = x - 1
			# Move leaf down
			new_leaves[(x,y-1)] = colour
	
	leaves = new_leaves
	leds.update(leaves)
	display.set_leds(leds)
	time.sleep(0.2)
