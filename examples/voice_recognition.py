# Say "Hey Mycroft" to wake up the voice recognition,
# and then say a sentence. Your sentence will then be
# repeated back to you.

microphone.start_voice_recognition()
while (True):
    # Wait up to 1000 seconds for some speech
    sentence = microphone.wait_for_sentence(1000.0)
    if sentence:
        # Convert text back to speech
        speaker.say('You said ' + sentence)
