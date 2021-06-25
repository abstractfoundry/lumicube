# Several computer players do a random walk on the led grid
# colouring where they go until the are stuck
# Can you make the players more intelligent?

def adjacent_positions(x, y, include_diagonal=False):
	positions = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
	if include_diagonal:
		positions = positions + [(x-1, y-1), (x-1, y+1), (x+1, y-1), (x+1, y+1)]
	mapped_positions = []
	for (x,y) in positions:
		# Account for 3D nature of panels
		if x > 7 and y > 7:
			if x > 7 and y == 8:
				mapped_positions.append((7, x))
			elif x == 8 and y > 7:
				mapped_positions.append((y, 7))
		# Make sure x and y are valid positions
		elif (x < 16 and x >= 0) and (y < 16 and y >= 0):
			mapped_positions.append((x,y))
	return mapped_positions

class Player:
	def __init__(self, pos, colour):
		self.pos = pos
		self.colour = colour
	
	def move(self, leds):
		(x,y) = self.pos
		# Get a list of all valid positions to move to
		valid_positions = []
		for neighbour in adjacent_positions(x, y):
			if neighbour not in leds:
				valid_positions.append(neighbour)
		# If no valid positions the player is finished, return False
		if len(valid_positions) == 0:
			return False
		# Choose a random valid position
		pos = valid_positions[random.randrange(len(valid_positions))]
		(x,y) = pos
		self.pos = pos
		leds[x, y] = self.colour
		display.set_led(x, y, self.colour)
		return True

num_players = 4
while True:
	# Start a new game
	players = []
	leds = {}
	display.set_all(black)
	# Generate all with players with random starting positions and colours
	for i in range(0, num_players):
		(x,y) = (random.randrange(16), random.randrange(16))
		if x > 8 and y > 8:
			y -= 8
		players.append(Player((x,y), random_colour()))
	# Keep calling players to move until there are none left
	while len(players) > 0:
		died = []
		# Move all players
		for player in players:
			if player.move(leds) == False:
				died.append(player)
		# Remove finished players
		for player in died:
			players.remove(player)
		time.sleep(0.1)
	# Wait before starting a new game
	time.sleep(1)
