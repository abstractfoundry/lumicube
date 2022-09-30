<p align="left">
    <a href="https://discord.gg/Vw4GP74jyR" alt="Join us on Discord">
        <img src="https://img.shields.io/discord/1019982647608496129?label=Discord&logo=discord&style=social" />
    </a>&nbsp;&nbsp;
    <a href="https://www.youtube.com/channel/UCqcvg09IKlXt0q0qyGb5hGw/featured" alt="Our YouTube Channel">
        <img src="https://img.shields.io/youtube/channel/views/UCqcvg09IKlXt0q0qyGb5hGw?label=YouTubeChannelViews&style=social" />
    </a>
</p>

# LumiCube

This repository contains some example code and documentation for the LumiCube:
* https://www.kickstarter.com/projects/1202256831/lumicube-an-led-cube-kit-for-the-raspberry-pi
* https://www.indiegogo.com/projects/lumicube-an-led-cube-kit-for-the-raspberry-pi

More detailed information can be found in our project booklet:
* https://abstractfoundry.com/lumicube/manual.pdf

For getting started head to our resources page:
* https://abstractfoundry.com/lumicube/resources

(Note: the only supported operating system at the moment is the full 32bit Raspberry Pi OS.)

The source code for the software running on the Raspberry Pi, including our web-based IDE, is available in a separate project:
* https://github.com/abstractfoundry/lumicube-daemon

## Community Contributions

Documentation:
* https://github.com/abstractfoundry/lumicube/tree/main/community-documentation

Scripts:
* https://github.com/abstractfoundry/lumicube/tree/main/community-scripts

## Simulator

It is also possible to run _some_ of these examples projects using our online simulator:
* https://abstractfoundry.com/lumicube/simulator

## Example projects

The “examples” folder contains a number of example projects, some of which we used in our Kickstarter and Indiegogo video:

### Level 1 (easiest)

#### button.py
Use the button to switch the cube’s colour between red and blue.

#### chiptune.py
Play a randomly generated tune.

#### pi_status_screen.py
Display some Raspberry Pi stats on the screen: CPU temperature, disk usage, etc.

#### rainbow.py
Continually change the cube's colour.

#### scrolling_clock.py
Every 10 seconds scroll the time across the LEDs.

#### voice_recognition.py
Basic voice recognition and text-to-speech.

### Level 2 (after you’ve learnt the basics)

#### autumn_scene.py
Autumn animation (leaves falling from a pixel-art tree).

#### binary_clock.py
A simple binary clock (see https://en.wikipedia.org/wiki/Binary_clock).

#### conways_game_of_life.py
Run Conway’s Game of Life on the LEDs (see https://en.wikipedia.org/wiki/Conway's_Game_of_Life).

#### equaliser.py
Colourful equaliser using the microphone.

#### land_grab.py
Several computer players randomly walk the LED grid, colouring squares until they get stuck.

#### lava_lamp.py
Use OpenSimplex noise to generate a lava lamp like effect (see https://en.wikipedia.org/wiki/Simplex_noise).

#### rain.py
Rain animation.

#### ripples.py
Random circular ripple animation.

#### tapping_ripples.py
Ripple animation which responds to tapping or moving the cube.

#### water_level.py
Virtual water-level effect which responds to the cube's orientation.

#### windmill.py
Blow at the back of the cube to make the windmill animation turn.

## Documentation

### Python API

See the LumiCube manual for a detailed explanation of the modules, methods and fields:
* https://abstractfoundry.com/lumicube/manual.pdf

A brief summary of the API is also given here:
* https://github.com/abstractfoundry/lumicube/blob/main/documentation/api.txt

### REST API

The API is broken down into:
- modules (e.g. speaker, microphone, screen)
- methods (e.g. play_tone(), draw_rectangle())
- fields  (e.g. volume, brightness)

All of the modules, methods, and fields in the Python API (see the product manual, linked above) also exist in the REST API.

#### Getting or setting a field

```
[GET/POST] http://<IP_ADDRESS>/api/v1/modules/<MODULE_NAME>/fields/<FIELD_NAME> { "value": <VALUE> }
```

For example, to set the brightness of the display to 50%:

```
curl -X POST -H "Content-Type: application/json" -d '{"value": 50}' http://<IP_ADDRESS>/api/v1/modules/display/fields/brightness
```

#### Calling a method

```
[POST] http://<IP_ADDRESS>/api/v1/modules/<MODULE_NAME>/methods/<METHOD_NAME> { "arguments": <ARGUMENTS_LIST> }
```

For example, to set one LED at x=1, y=0 to colour=255 (blue, #0000ff in hex):

```
curl -X POST -H "Content-Type: application/json" -d '{"arguments": [1, 0, 255]}' http://<IP_ADDRESS>/api/v1/modules/display/methods/set_led
```

#### Executing a Python script

```
[POST] http://<IP_ADDRESS>/api/v1/scripts/main/methods/start { "body": "<YOUR_CODE>" }
```

For example, to set all the LEDs to red using a Python script:

```
curl -X POST -H "Content-Type: application/json" -d '{"body": "display.set_all(red)"}' http://<IP_ADDRESS>/api/v1/scripts/main/methods/start
```

#### Exceptional cases

`set_leds(), set_3d()`

In Python these methods take a dictionary mapping coordinates to colours, where the coordinates are a tuple of (x, y) or (x, y, z) values. JSON doesn't support tuples, so instead coordinates are represented as a comma-separated string.

For example, to set the LED at (0,0) to 0x000080 and the LED at (1,1) to 0x0000FF:

```
curl -X POST -H "Content-Type: application/json" -d '{"arguments": [{"0,0": 128, "1,1": 255}]}' http://<IP_ADDRESS>/api/v1/modules/display/methods/set_leds
```
