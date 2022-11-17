from requests import Session
from typing import List

"""
A Python Module for the Lumicube HTTP Interface.
So you can interact with the Lumicube from a different Python Script
"""


class LumicubeInterface:
    """
    A Class to interface with the Lumicube API
    For more information:
    https://github.com/abstractfoundry/lumicube
    """
    def __init__(self, api_version: str = 'v1', url: str = 'localhost') -> None:
        """

        :param api_version: Api Version (default v1)
        :param url: url of the Lumicube (default localhost)
        """
        self._baseUrl = 'http://' + url + '/api/' + api_version
        self.session = Session()
        self.modules = Modules(self._baseUrl, self.session)


# region Modules


class Modules:
    def __init__(self, baseurl, session):
        self.__url = baseurl + '/modules'
        self.buttons = Buttons(self.__url, session)
        self.display = Display(self.__url, session)
        self.light_sensor = LightSensor(self.__url, session)
        self.imu = IMU(self.__url, session)
        self.microphone = Microphone(self.__url, session)
        self.screen = Screen(self.__url, session)
        self.speaker = Speaker(self.__url, session)
        # self.pi = Pi(self.__url) WIP


class Buttons:
    def __init__(self, url, session):
        self.__fullUrl = url + '/buttons'
        self.session = session

    def get_next_action(self, timeout: int):
        """
        Returns the next button pressed by the user, either "top", "middle", or "bottom".
        If more than "timeout" seconds elapse before a button is pressed, None is returned.

        :param timeout: maximum time to wait in seconds
        """
        args = {"arguments": [timeout]}
        ret = self.session.post(url=self.__fullUrl + '/methods/get_next_action', json=args)
        ret.raise_for_status()

    @property
    def top_pressed(self):
        """
        Returns the current top button state

        :return: current top button state
        """
        ret = self.session.post(url=self.__fullUrl + '/fields/top_pressed')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    @property
    def top_pressed_count(self):
        """
        Returns amount of times the top button was pressed

        :return: amount of times the top button was pressed
        """
        ret = self.session.get(url=self.__fullUrl + '/fields/top_pressed_count')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    @top_pressed_count.setter
    def top_pressed_count(self, value: int):
        """
        Sets the amount of times the top button was pressed

        :param value: amount of times the top button was pressed
        """
        args = {"value": value}
        ret = self.session.post(url=self.__fullUrl + '/fields/top_pressed_count', json=args)
        ret.raise_for_status()

    @property
    def middle_pressed(self) -> int:
        """
        Returns the current middle button state

        :return: current middle button state
        """
        ret = self.session.post(url=self.__fullUrl + '/fields/middle_pressed')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    @property
    def middle_pressed_count(self):
        """
        Returns amount of times the middle button was pressed

        :return: amount of times the middle button was pressed
        """
        ret = self.session.get(url=self.__fullUrl + '/fields/middle_pressed_count')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    @middle_pressed_count.setter
    def middle_pressed_count(self, value: int):
        """
        Sets the amount of times the middle button was pressed

        :param value: amount of times the middle button was pressed
        """
        args = {"value": value}
        ret = self.session.post(url=self.__fullUrl + '/fields/middle_pressed_count', json=args)
        ret.raise_for_status()

    @property
    def bottom_pressed(self):
        ret = self.session.post(url=self.__fullUrl + '/fields/bottom_pressed')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    @property
    def bottom_pressed_count(self):
        """
        Returns amount of times the bottom button was pressed

        :return: amount of times the bottom button was pressed
        """
        ret = self.session.get(url=self.__fullUrl + '/fields/bottom_pressed_count')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    @bottom_pressed_count.setter
    def bottom_pressed_count(self, value: int):
        """
        Sets the amount of times the bottom button was pressed

        :param value: amount of times the bottom button was pressed
        """
        args = {"value": value}
        ret = self.session.post(url=self.__fullUrl + '/fields/bottom_pressed_count', json=args)
        ret.raise_for_status()

class Display:
    def __init__(self, url, session):
        self.__fullUrl = url + '/display'
        self.session = session

    def set_all(self, color: int):
        """
        Set the colour of all the LEDs.

        :param color: 24-bit colour, e.g. black, red, hsv_colour(0.5, 1, 1), 0xFF0000
        """
        args = {"arguments": [color]}
        ret = self.session.post(url=self.__fullUrl + '/methods/set_all', json=args, timeout=5)
        ret.raise_for_status()

    def set_led(self, x: int, y: int, color: int):
        """
        Set a single LED to a colour using x and y coordinates.
        The bottom left panel is described by:        x in range 0 to 7,  y in range 0 to 7
        The bottom right panel is described by:       x in range 8 to 15, y in range 0 to 7
        The top panel is described by:                x in range 0 to 7,  y in range 8 to 15
        Coordinates outside this range will be ignored.
        e.g.
        display.set_led(0, 0, red)     would change the bottom left pixel to red
        display.set_led(15, 15, pink)  would do nothing as it is out of range

        :param x: x coordinate, range 0 to 15
        :param y: y coordinate, range 0 to 15
        :param color: 24-bit colour, e.g. black, red, hsv_colour(0.5, 1, 1), 0xFF0000
        """
        args = {"arguments": [x, y, color]}
        ret = self.session.post(url=self.__fullUrl + '/methods/set_led', json=args)
        ret.raise_for_status()

    def set_leds(self, x_y_to_colour_dict: dict):
        """
        Set multiple LEDs all at once using x and y coordinates.
        For more information see display.set_led.

        :param x_y_to_colour_dict: dictionary with (x, y) coordinates as keys and colours as values
        """

        def __2d_dic_to_css(dictionary: dict):
            """
            JSON doesn't support tuples, so instead coordinates are represented as a comma-separated string.
            This function converts the tuples to a comma-separated string.

            :param dictionary: dictionary with 2 tuples as key value
            :return: dictionary with comma-separated string as key value
            """
            comma_separate_string = []
            temp_dict = {}
            for item in dictionary:
                temp_dict[f"{item[0]}, {item[1]}"] = dictionary[item[0], item[1]]
            comma_separate_string.append(temp_dict)
            return comma_separate_string

        param = __2d_dic_to_css(x_y_to_colour_dict)
        args = {"arguments": param}
        ret = self.session.post(url=self.__fullUrl + '/methods/set_leds', json=args)
        ret.raise_for_status()

    def set_3d(self, x_y_to_colour_dict: dict):
        """
        Description: Set multiple LEDs to a colour using x, y and z coordinates.

        The left panel is described by:  x, y when z = 8
        The right panel is described by: y, z when x = 8
        The top panel is described by:   x, z when y = 8
        Coordinates outside this range will be ignored.

        :param x_y_to_colour_dict: dictionary with (x, y, z) as keys and colours as values
        """

        def __3d_dic_to_css(dictionary: dict) -> object:
            """
            JSON doesn't support tuples, so instead coordinates are represented as a comma-separated string.
            This function converts the tuples to a comma-separated string.

            :param dictionary: dictionary with 3 tuples as key value
            :return: dictionary with comma-separated string as key value
            """
            comma_separate_string = []
            temp_dict = {}
            for item in dictionary:
                temp_dict[f"{item[0]}, {item[1]}, {item[2]}"] = dictionary[item[0], item[1], item[2]]
            comma_separate_string.append(temp_dict)
            return comma_separate_string

        param = __3d_dic_to_css(x_y_to_colour_dict)
        args2 = {"arguments": param}
        ret = self.session.post(url=self.__fullUrl + '/methods/set_3d', json=args2)
        ret.raise_for_status()

    def set_panel(self, panel: str, color_List: List[List[int]]):
        """
        Set all the LEDs on one panel.
        Takes 8 lists each containing 8 colours.
        The first list is the top row of LEDs.
        The first colour in that list is the top left LED colour.

        :param panel: panel name, either "top", "left" or "right"
        :param color_list: 8 by 8 list of colours
        """
        args = {"arguments": [panel, color_list]}
        ret = self.session.post(url=self.__fullUrl + '/methods/set_panel', json=args)
        ret.raise_for_status()

    def clear_panel(self, panel: str):
        """
        Clears a complete LED panel (sets LEDs to black)

        :param panel: panel name, either "top", "left" or "right"
        """
        sub_list = [0, 0, 0, 0, 0, 0, 0, 0]
        main_list = []
        for x in range(8):
            main_list.append(sub_list)
        args = {"arguments": [panel, main_list]}
        ret = self.session.post(url=self.__fullUrl + '/methods/set_panel', json=args)
        ret.raise_for_status()

    def scroll_text(self, text: str, color: int = 0xFFFFFF, background_color: int = 0x0, speed: float = 1):
        """
        Display text on the LEDs scrolling from right to left.

        :param text: text to display
        :param color: 24-bit colour, e.g. black, red, hsv_colour(0.5, 1, 1), 0xFF0000
        :param background_color: 24-bit colour, e.g. black, red, hsv_colour(0.5, 1, 1), 0xFF0000
        :param speed: floating-point value
        """
        args = {"arguments": [text, color, background_color, speed]}
        ret = self.session.post(url=self.__fullUrl + '/methods/scroll_text', json=args)
        ret.raise_for_status()

    @property
    def brightness(self) -> int:
        """
        Return the current LED brightness

        :return: brightness of the LEDs
        """
        ret = self.session.get(url=self.__fullUrl + '/fields/brightness')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    @brightness.setter
    def brightness(self, brightness: int):
        """
        Sets the LED brightness

        :param brightness: brightness of the LEDs
        """
        args = {"value": brightness}
        ret = self.session.post(url=self.__fullUrl + '/fields/brightness', json=args)
        ret.raise_for_status()

    @property
    def refresh_period(self) -> int:
        """
        Returns the refresh period of the LEDs

        :return: refresh Period
        """
        ret = self.session.get(url=self.__fullUrl + '/fields/refresh_period')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    @refresh_period.setter
    def refresh_period(self, refresh: int):
        """
        Sets the refresh Period of the LEDs

        :param refresh: refresh Period
        """
        args = {"value": refresh}
        ret = self.session.post(url=self.__fullUrl + '/fields/refresh_period', json=args)
        ret.raise_for_status()

    @property
    def get_estimated_current(self):
        """
        Return the estimated current drawn by the LEDs

        :return: estimated current drawn
        """
        ret = self.session.get(url=self.__fullUrl + '/fields/estimated_current')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    @property
    def max_current(self) -> int:
        """
        Returns the maximum current drawn by the LEDs

        :return: maximum current drawn
        """
        ret = self.session.get(url=self.__fullUrl + '/fields/max_current')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    @max_current.setter
    def max_current(self, max_current: int):
        """
        Sets the maximum current drawn by the LEDs
        :param max_current: maximum current drawn
        """
        args = {"value": max_current}
        ret = self.session.post(url=self.__fullUrl + '/fields/max_current', json=args)
        ret.raise_for_status()


class LightSensor:
    def __init__(self, url, session):
        self.__fullUrl = url + '/light_sensor'
        self.session = session

    def next_gesture(self, timeout: int):
        """
        Returns the next gesture performed by the user, either "up", "down", "left" or "right".
        If more than "timeout" seconds elapse before a gesture is performed, None is returned.

        :param timeout: maximum time to wait in seconds
        """
        args = {"arguments": [timeout]}
        ret = self.session.post(url=self.__fullUrl + '/methods/get_next_gesture', json=args)
        ret.raise_for_status()

    @property
    def ambient_light(self):
        """
        Returns the ambient light intensity

        :return: ambient light intensity
        """
        ret = self.session.get(url=self.__fullUrl + '/fields/ambient_light')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    @property
    def red(self):
        """
        Returns red value of the RGB sensor

        :return: red value
        """
        ret = self.session.get(url=self.__fullUrl + '/fields/red')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    @property
    def green(self):
        """
        Returns green value of the RGB sensor

        :return: green value
        """
        ret = self.session.get(url=self.__fullUrl + '/fields/green')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    @property
    def blue(self):
        """
        Returns blue value of the RGB sensor

        :return: blue value
        """
        ret = self.session.get(url=self.__fullUrl + '/fields/blue')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    @property
    def last_gesture(self):
        """
        Returns last gesture direction

        :return: last gesture
        """
        ret = self.session.get(url=self.__fullUrl + '/fields/last_gesture')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    @property
    def num_gesture(self):
        """
        Returns amount of gestures

        :return: amount of gestures
        """
        ret = self.session.get(url=self.__fullUrl + '/fields/num_gestures')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    @num_gesture.setter
    def num_gesture(self, value: int):
        """
        Sets the amount of gestures

        :param value: amount of gestures
        """
        args = {"value": value}
        ret = self.session.post(url=self.__fullUrl + '/fields/num_gestures', json=args)
        ret.raise_for_status()

    @property
    def within_proximity(self):
        """
        Returns current state of the proximity Sensor

        :return: True = in proximity || False = not in proximity
        """
        ret = self.session.get(url=self.__fullUrl + '/fields/within_proximity')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    @property
    def num_times_within_proximity(self):
        """
        Returns the amount of times within the proximity sensor

        :return: amount of times within proximity
        """
        ret = self.session.get(url=self.__fullUrl + '/fields/num_times_within_proximity')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    @num_times_within_proximity.setter
    def num_times_within_proximity(self, value: int):
        """
        Sets the amount of times within the proximity sensor

        :return: amount of times within proximity
        """
        args = {"value": value}
        ret = self.session.post(url=self.__fullUrl + '/fields/num_times_within_proximity', json=args)
        ret.raise_for_status()


class Microphone:
    def __init__(self, url, session):
        self.__fullUrl = url + '/microphone'
        self.session = session

    def start_recording(self, path: str):
        """
        Start recording microphone audio to the specified file. The file name must end in either ".wav"
        or ".mp3". If a file already exists at the given path, it is replaced.

        :param path: path to the output file (must end in ".wav" or ".mp3")
        """
        args = {"arguments": [path]}
        ret = self.session.post(url=self.__fullUrl + '/methods/start_recording', json=args)
        ret.raise_for_status()

    def stop_recording(self):
        """
        Stop a previously started recording.
        """
        args = {"arguments": []}
        ret = self.session.post(url=self.__fullUrl + '/methods/stop_recording', json=args)
        ret.raise_for_status()

    def start_voice_recognition(self):
        """
        Start the voice recognition service.
        """
        args = {"arguments": []}
        ret = self.session.post(url=self.__fullUrl + '/methods/start_voice_recognition', json=args)
        ret.raise_for_status()

    def wait_for_sentence(self, timeout: float):
        """
        Wait some number of seconds for a sentence to be spoken and translated into text.
        The sentence must be preceded by the wake word "Hey Mycroft".

        :param timeout: floating-point value specifying how many seconds to wait
        """
        args = {"arguments": [timeout]}
        ret = self.session.post(url=self.__fullUrl + '/methods/wait_for_sentence', json=args)
        ret.raise_for_status()

    def stop_voice_recognition(self):
        """
        Stop the voice recognition service.
        """
        args = {"arguments": []}
        ret = self.session.post(url=self.__fullUrl + '/methods/stop_voice_recognition', json=args)
        ret.raise_for_status()

    def start_recording_for_frequency_analysis(self):
        """
        Start recording audio for frequency analysis.
        """
        args = {"arguments": []}
        ret = self.session.post(url=self.__fullUrl + '/methods/start_recording_for_frequency_analysis', json=args)
        ret.raise_for_status()

    def get_frequency_buckets(self, num_buckets: int = 8, min_hz: int = 0, max_hz: int = 4000):
        """
        Process the audio data collected since the last call to get_frequency_buckets.
        Returns a dictionary of frequencies mapped to magnitudes.

        :param num_buckets: the number of buckets to divide the frequencies amongst
        :param min_hz: the minimum frequency to process
        :param max_hz: the maximum frequency to process
        """
        args = {"arguments": [num_buckets, min_hz, max_hz]}
        ret = self.session.post(url=self.__fullUrl + '/methods/get_frequency_buckets', json=args)
        ret.raise_for_status()

    def enable(self, enable: bool = True):
        """
        Enables the microphone

        :param enable: True = enable || False = disable
        """
        args = {"arguments": [enable]}
        ret = self.session.post(url=self.__fullUrl + '/methods/get_frequency_buckets', json=args)
        ret.raise_for_status()


class IMU:
    def __init__(self, url, session):
        self.__fullUrl = url + '/imu'
        self.session = session

    @property
    def get_pitch(self):
        """
        WIP

        :return:
        """
        ret = self.session.get(url=self.__fullUrl + '/fields/pitch')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    @property
    def get_roll(self):
        """
        WIP

        :return:
        """
        ret = self.session.get(url=self.__fullUrl + '/fields/roll')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    @property
    def get_yaw(self):
        """
        WIP

        :return:
        """
        ret = self.session.get(url=self.__fullUrl + '/fields/yaw')
        if not ret.status_code == 200:
            log(ret)
            return
        data = ret.json()
        return data['value']

    @property
    def get_acc_x(self):
        """
        WIP

        :return:
        """
        ret = self.session.get(url=self.__fullUrl + '/fields/acceleration_x')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    @property
    def get_acc_y(self):
        """
        WIP

        :return:
        """
        ret = self.session.get(url=self.__fullUrl + '/fields/acceleration_y')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    @property
    def get_acc_z(self):
        """
        WIP

        :return:
        """
        ret = self.session.get(url=self.__fullUrl + '/fields/acceleration_z')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    @property
    def get_ang_vel_x(self):
        """
                WIP

        :return:
        """
        ret = self.session.get(url=self.__fullUrl + '/fields/angular_velocity_x')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    @property
    def get_ang_vel_y(self):
        """
                WIP

        :return:
        """
        ret = self.session.get(url=self.__fullUrl + '/fields/angular_velocity_y')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    @property
    def get_ang_vel_z(self):
        """
                WIP

        :return:
        """
        ret = self.session.get(url=self.__fullUrl + '/fields/angular_velocity_z')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    @property
    def get_gravity_x(self):
        """
                WIP

        :return:
        """
        ret = self.session.get(url=self.__fullUrl + '/fields/gravity_x')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    @property
    def get_gravity_y(self):
        """
                WIP

        :return:
        """
        ret = self.session.get(url=self.__fullUrl + '/fields/gravity_y')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    @property
    def get_gravity_z(self):
        """
        WIP

        :return:
        """
        ret = self.session.get(url=self.__fullUrl + '/fields/gravity_z')
        ret.raise_for_status()
        data = ret.json()
        return data['value']


class Screen:
    def __init__(self, url, session):
        self.__fullUrl = url + '/screen'
        self.session = session

    def set_pixel(self, x: int, y: int, color: int):
        """
        Set the colour of a pixel given an x and y coordinate.

        :param x: integer between 0 and 319
        :param y: integer between 0 and 239
        :param color: 24-bit colour, e.g. black, red, hsv_colour(0.5, 1, 1), 0xFF0000
        """
        args = {"arguments": [x, y, color]}
        ret = self.session.post(url=self.__fullUrl + '/methods/set_pixel', json=args)
        ret.raise_for_status()

    def set_pixels(self, x: int, y: int, width: int, height: int, pixels: List[int]):
        """
        Set the colours of a rectangular region of pixels, from (x, y) to (x+width, y+height).
        The length of the "pixels" list must be exactly width*height, and is read left to right,
        top down.

        :param x: integer between 0 and 319
        :param y: integer between 0 and 239
        :param width: integer between 0 and 320
        :param height: integer between 0 and 240
        :param pixels: list of 24-bit colours (length width*height)
        """
        args = {"arguments": [x, y, width, height, pixels]}
        ret = self.session.post(url=self.__fullUrl + '/methods/set_pixels', json=args)
        ret.raise_for_status()

    def draw_rectangle(self, x: int, y: int, width: int, height: int, color: int):
        """
        Draw a coloured rectangle starting at x and y coordinates.

        :param x: integer between 0 and 319
        :param y: integer between 0 and 239
        :param width: integer between 0 and 320
        :param height: integer between 0 and 240
        :param color: 24-bit colour, e.g. black, red, hsv_colour(0.5, 1, 1), 0xFF0000
        """
        args = {"arguments": [x, y, width, height, color]}
        ret = self.session.post(url=self.__fullUrl + '/methods/draw_rectangle', json=args)
        ret.raise_for_status()

    def write_text(self, x: int, y: int, text: str, size: int, color: int, background_color: int):
        """
        Write some text to the screen starting at x and y coordinates.

        :param x: integer between 0 and 319
        :param y: integer between 0 and 239
        :param text: text to be displayed
        :param size: integer representing the font size, must be greater than 0
        :param color: 24-bit colour, e.g. black, red, hsv_colour(0.5, 1, 1), 0xFF0000
        :param background_color: 24-bit colour, e.g. black, red, hsv_colour(0.5, 1, 1), 0xFF0000
        """
        args = {"arguments": [x, y, text, size, color, background_color]}
        ret = self.session.post(url=self.__fullUrl + '/methods/write_text', json=args)
        ret.raise_for_status()

    def draw_image(self, path: str, x: int = 0, y: int = 0, width: int = 320, height: int = 240):
        """
        Draw an image to the screen, scaled to fit the rectangular region from (x, y) to (x+width, y+height).
        Paths are taken relative to the desktop (or can be specified absolutely).

        :param path: path to the image file
        :param x: integer between 0 and 319
        :param y: integer between 0 and 239
        :param width: integer between 0 and 320
        :param height: integer between 0 and 240
        """
        args = {"arguments": [path, x, y, width, height]}
        ret = self.session.post(url=self.__fullUrl + '/methods/draw_image', json=args)
        ret.raise_for_status()

    def resolution_scaling(self, scaling: int):
        """
        Scale the resolution

        :param scaling: N/A
        """
        args = {"value": scaling}
        ret = self.session.post(url=self.__fullUrl + '/fields/resolution_scaling', json=args)
        ret.raise_for_status()

    def invert_colours(self, state: int):
        """
        Invert colors of the screen

        :param state: True = inverted || False = normal
        """
        args = {"value": state}
        ret = self.session.post(url=self.__fullUrl + '/fields/invert_colours', json=args)
        ret.raise_for_status()


class Speaker:
    def __init__(self, url, session):
        self.__fullUrl = url + '/speaker'
        self.session = session

    def play(self, path: str):
        """
        Play an audio file (non-absolute paths are taken relative to the Desktop directory).

        :param path: string specifying the path to the audio file
        """
        args = {"arguments": [path]}
        ret = self.session.post(url=self.__fullUrl + '/methods/play', json=args)
        ret.raise_for_status()

    def stop(self):
        """
        Stops all currently playing audio files.
        """
        args = {"arguments": []}
        ret = self.session.post(url=self.__fullUrl + '/methods/stop', json=args)
        ret.raise_for_status()

    def say(self, text: str):
        """
        Convert text to speech.

        :param text: Text to speach
        """
        args = {"arguments": [text]}
        ret = self.session.post(url=self.__fullUrl + '/methods/say', json=args)
        ret.raise_for_status()

    def tone(self, freq: float, duration: float, volume: float, function: str):
        """
        Play a tone of a certain frequency.

        :param freq: frequency in Hz
        :param duration: time in seconds
        :param volume: number between 0.0 and 1.0 specifying the volume
        :param function: sine_wave, square_wave, white_noise
        """
        args = {"arguments": [freq, duration, volume, function]}
        ret = self.session.post(url=self.__fullUrl + '/methods/tone', json=args)
        ret.raise_for_status()

    def set_volume(self, volume: float):
        """
        Set the speaker volume

        :param volume: volume of the speaker
        """
        args = {"value": volume}
        ret = self.session.post(url=self.__fullUrl + '/fields/volume', json=args)
        ret.raise_for_status()


""" WIP
class Pi:
    def __init__(self, url, session):
        self.__fullUrl = url + '/pi'
        self.session = session

    def get_ip_address(self):
        ret = self.session.get(url=self.__fullUrl + '/fields/ip_address')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    def get_cpu_temp(self):
        ret = self.session.get(url=self.__fullUrl + '/fields/cpu_temp')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    def get_cpu_percentage(self):
        ret = self.session.get(url=self.__fullUrl + '/fields/cpu_percent')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    def get_ram_percent_used(self):
        ret = self.session.get(url=self.__fullUrl + '/fields/ram_percent_used')
        ret.raise_for_status()
        data = ret.json()
        return data['value']

    def get_disk_percent(self):
        ret = self.session.get(url=self.__fullUrl + '/fields/disk_percent')
        ret.raise_for_status()
        data = ret.json()
        return data['value']
"""
# endregion
