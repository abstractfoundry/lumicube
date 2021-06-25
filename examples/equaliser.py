# LED equaliser
# It records the microphone audio, processes it into frequency buckets
# and then displays the level of each bucket on the LEDs

num_buckets = 8

display.set_all(black)
pixels_per_bucket = max(1, 16/num_buckets)
buckets = [0 for i in range(num_buckets)]
last_time = time.time()
max_magnitude = 1 # dynamically adjust the max as we go along

# Start recording audio samples
capture = microphone.start_recording_for_frequency_analysis()

while 1:
    # Get new bucket levels
    # Converting the audio samples into 8 frequency buckets between 0Hz and 1000Hz
    new_buckets = list(microphone.get_frequency_buckets(capture, num_buckets, 0, 800).values())
    
    # Process data - keeping track of max level
    for bi, magnitude in enumerate(new_buckets):
        buckets[bi] = max(buckets[bi], magnitude)
        max_magnitude = max(max_magnitude, magnitude)
        
    # Every 10th of a second update the leds
    # We do this separately from the processing of the data because we don't want the leds to change too fast
    if time.time() - last_time > 1/10:
        last_time = time.time()
        colours = {}
        for y in range(0,8):
            for x in range(0,16):
                bi = int(x/pixels_per_bucket)
                if y/8.0 <= buckets[bi] / max_magnitude or y == 0:
                    colours[(x,y)] = hsv_colour(1 - bi/num_buckets, 1, 1)
                else:
                    colours[(x,y)] = 0
        display.set_leds(colours)
        # Reset bucket levels
        buckets = [0 for i in range(num_buckets)]
        # With time reduce the max
        max_magnitude *= 0.99