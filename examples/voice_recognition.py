# Say "Hey Mycroft" to start voice recognition
# Then say whatever you want and once you've finished it will say it back to you

# Start voice recognition
statement_queue = microphone.start_listening()
while True:
	# Get next voice clip as text
    statement = statement_queue.get() # Blocking
    # Convert text back to speech
    speaker.say('You said ' + statement)
