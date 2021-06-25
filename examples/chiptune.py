# Play a randomly generated tune
# speaker.tone(frequency, duration, amplitude)

while True:
    # Play a rising piece
    for frequency in range(500, 2000, 100):
        speaker.tone(frequency, 0.01)
    # Play a beat and then another beat
    time.sleep(0.02)
    speaker.tone(500, 0.1, 0.1, function=white_noise)
    time.sleep(0.05)
    speaker.tone(500, 0.1, 0.1, function=white_noise)
    # Play 3 different tones 
    speaker.tone(500 + 500 * random.random(), 0.1)
    speaker.tone(500 + 500 * random.random(), 0.1)
    speaker.tone(500 + 500 * random.random(), 0.1)
    # Play another rising piece
    for frequency in range(200, 1000, 10):
        speaker.tone(frequency, 0.003)
