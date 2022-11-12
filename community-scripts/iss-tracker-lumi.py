"""
iss-tracker-lumi.py

Track the International Space Station.

Additional Installation Packages

You will need to pip install the following packages:
    pip install requests==2.25.1
    pip install geopy==2.2.0

Display 8-bit ISS, it's current location (latitude / longitude) and distance from a given location.

This project was inspired by my son.  He has a large interest in space and wanted a light system to track the ISS.
The original version of this will light up a strip of 20 leds.  This version was built when a co-worker sent me a
link the the LumiCube.

You will need to set the latitude, longitude, sound_file, and sound_file_length in the current_properties dictionary.

You can get  your Latitude and Longitude from: https://www.latlong.net

latitude and longitude are float values
sound_file is a string and the file will need to be in the Desktop/ directory of the user you created when setting up
           your LumiCube.
sound_length is an integer specifying the length of the sound file in seconds

Properties you can set:
    latitude          : Float of latitude of location you are at.  i.e. 51.507351
    longitude         : Float of longitude of location you are at.  i.e. -0.127758
    radius            : If the ISS is withing this float value it will either be Overhead or Visible
                            The default is 1300 (miles).  If you change from mi to km, you need to change this to 2092 (kilometers)
    distance_measure  : mi for miles, km for kilometers
    do_not_disturb    :
        start         : Hour you want the do not disturb to start in 24 hour format.  i.e. 22
        end           : Hour you want the do not disturb to end in 24 hour format. i.e. 9
    sound_file        : The name of the file in Desktop/ directory that will be played when Overhead or Visible
    sound_file_length : The length in seconds of the sound file.
"""
__author__ = "Rick Feldmann"
__email__ = "wrfeldmann@icloud.com"
__status__ = "Production"
__version__ = "1.0"

import logging.handlers
import os
import requests
import time

from datetime import datetime
from geopy import distance

properties = dict()
properties["latitude"] = 39.2383
properties["longitude"] = -77.4511
properties["radius"] = 1300.0
properties["distance_measure"] = "mi"
properties["do_not_disturb"] = dict()
properties["do_not_disturb"]["start"] = 22
properties["do_not_disturb"]["end"] = 9
properties["sound_file"] = "2001_Space_Odyssey.mp3"
properties["sound_file_length"] = 78


class BuildPanel(object):
    def __init__(self):
        return

    def create_iss_panel(self, color, rotate):
        """
        Creates an 8-bit representation of the ISS.

        @param: LumiCube Color
        @param: Boolean True or False to build the ISS rotated 90 degrees

        @return: 8x8 list with the appropriate colors to represent the ISS
                No rotation     Rotated 90 degrees

                 X X  X X            XXXXXXXX
                 X X  X X               XX
                 X X  X X            XXXXXXXX
                 XXXXXXXX               XX
                 XXXXXXXX               XX
                 X X  X X            XXXXXXXX
                 X X  X X               XX
                 X X  X X            XXXXXXXX
        """
        panel = list()
        if rotate is True:
            for row_index in range(0, 8, 1):
                row = list()
                for cell_index in range(0, 8, 1):
                    if row_index in [0, 2, 5, 7] and cell_index in [0, 1, 2, 5, 6, 7]:
                        row.append(color)
                    if row_index in [1, 3, 4, 6] and cell_index in [0, 1, 2, 5, 6, 7]:
                        row.append(black)
                    if row_index in [0, 1, 2, 3, 4, 5, 6, 7] and cell_index in [3, 4]:
                        row.append(color)
                panel.append(row)
        else:
            for row_index in range(0, 8, 1):
                row = list()
                for cell_index in range(0, 8, 1):
                    if row_index in [0, 1, 2, 5, 6, 7] and cell_index in [0, 2, 5, 7]:
                        row.append(color)
                    if row_index in [0, 1, 2, 5, 6, 7] and cell_index in [1, 3, 4, 6]:
                        row.append(black)
                    if row_index in [3, 4] and cell_index in [0, 1, 2, 3, 4, 5, 6, 7]:
                        row.append(color)
                panel.append(row)
        return panel


class CheckDoNotDisturb(object):
    def __init__(self):
        return

    def check_do_not_disturb(self, current_datetime):
        """Check to see if it the run is during the do not disturb time."""
        return_value = False
        current_hour = current_datetime.hour
        if current_hour > properties["do_not_disturb"]["start"]:
            return_value = True
        elif current_hour < properties["do_not_disturb"]["end"]:
            return_value = True
        return return_value


class ISSUtils(object):
    def __init__(self):
        return

    def current_ISS_location(self):
        """Get the current ISS Location."""
        try:
            response = requests.get(url="http://api.open-notify.org/iss-now.json")
            data = response.json()
            current_iss_latitude = float(data["iss_position"]["latitude"])
            current_iss_longitude = float(data["iss_position"]["longitude"])
        except:
            current_iss_latitude = 0.0
            current_iss_longitude = 0.0
        return current_iss_latitude, current_iss_longitude

    def iss_distance(self, current_iss_latitude, current_iss_longitude):
        """Get the distance you are from the ISS."""
        my_location = (properties["latitude"], properties["longitude"])
        iss_location = (current_iss_latitude, current_iss_longitude)
        if properties["distance_measure"] == "mi":
            return_distance = distance.distance(my_location, iss_location).miles
        else:
            return_distance = distance.distance(my_location, iss_location).km
        return return_distance

    def near_ISS(self, distance):
        """Calculate if we are near enough that it is Overhead."""
        message = "Far Away"
        true_false = False
        if distance <= properties["radius"]:
            message = "Overhead"
            true_false = True
        return true_false, message


class LoggingUtils(object):
    def __init__(self):
        """
        Initialize logging.

        File is Desktop/loggs/iss-tracker.log

        I use this file for homebridge integration with Apple HomeKit so I can trigger additional Apple Home devices
        to perform various things.
        """
        self.log_dir = "logs/"
        self.log_file = "{0}/{1}{2}".format(os.getcwd(), self.log_dir, "iss-tracker.log")
        self.logger = logging.getLogger("issLogger")
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def configureLogging(self, level="INFO"):
        """Configure and return the logger."""
        self.logger.setLevel(logging.INFO)
        rotating_log_file_handler = logging.handlers.RotatingFileHandler(self.log_file,
                                                                         maxBytes=1048576,
                                                                         backupCount=5)
        rotating_log_file_formatter = logging.Formatter("%(message)s")
        rotating_log_file_handler.setFormatter(rotating_log_file_formatter)
        self.logger.addHandler(rotating_log_file_handler)
        return self.logger


class SoundUtils(object):
    def __init__(self):
        return

    def check_playing_sound(self, play_sound, message):
        """
        Say the message passed in and, if not playing, play the sound.

        :param play_sound:
        :param message:
        :return:
        """
        speaker.say("The International Space Station is {0}".format(message))
        if not play_sound and os.path.exists(properties["sound_file"]):
            self.visible_sound_start_time = datetime.now()
            speaker.play(properties["sound_file"])
            play_sound = True
            time.sleep(1.0)
        elif play_sound:
            current_time = datetime.now()
            time_difference = abs(current_time - self.visible_sound_start_time)
            if time_difference.seconds > properties["sound_file_length"]:
                play_sound = False
        return play_sound


class SunriseSunsetUtils(object):
    def __init__(self):
        return

    def getTimestamp(self, dt):
        return datetime.timestamp(datetime.fromisoformat(dt))

    def is_twilight(self, current_time):
        """
        Determines if the ISS is visible.

        :param current_time:
        :param args:
        :return:
        """
        sunrise_sunset_base_url = "https://api.sunrise-sunset.org/json"
        sunrise_sunset_url = "{0}?lat={1}&lng={2}&formatted=0".format(sunrise_sunset_base_url,
                                                                      properties["latitude"],
                                                                      properties["longitude"])
        try:
            response = requests.get(sunrise_sunset_url)
            data = response.json()
            astronomical_twilight_begin_timestamp = self.getTimestamp(
                data["results"]["astronomical_twilight_begin"])
            sunrise_timestamp = self.getTimestamp(data["results"]["sunrise"])
            sunset_timestamp = self.getTimestamp(data["results"]["sunset"])
            astronomical_twilight_end_timestamp = self.getTimestamp(data["results"]["astronomical_twilight_end"])
        except:
            astronomical_twilight_begin_timestamp = 0
            sunrise_timestamp = 0
            sunset_timestamp = 0
            astronomical_twilight_end_timestamp = 0
        timezone_offset = float(current_time.isoformat().split("T")[1][-6:].replace(":", "."))
        time_now = self.getTimestamp(current_time.isoformat())
        astronomical_twilight_begin_timestamp = astronomical_twilight_begin_timestamp + (timezone_offset * 3600)
        sunrise_timestamp = sunrise_timestamp + (timezone_offset * 3600)
        sunset_timestamp = sunset_timestamp + (timezone_offset * 3600)
        astronomical_twilight_end_timestamp = astronomical_twilight_end_timestamp + (timezone_offset * 3600)
        true_false = False
        if (time_now >= astronomical_twilight_begin_timestamp and time_now <= sunrise_timestamp) or \
                (time_now >= sunset_timestamp and time_now <= astronomical_twilight_end_timestamp):
            true_false = True
        return true_false


build_panel = BuildPanel()
check_do_not_disturb = CheckDoNotDisturb()
iss_utils = ISSUtils()
logging_utils = LoggingUtils()
sound_utils = SoundUtils()
sunrise_sunset_utils = SunriseSunsetUtils()

# Configure and return a logger from logging_utils
logger = logging_utils.configureLogging()

# Create the panels necessary
blue_panel_1 = build_panel.create_iss_panel(blue, False)
blue_panel_2 = build_panel.create_iss_panel(blue, True)
green_panel_1 = build_panel.create_iss_panel(green, False)
green_panel_2 = build_panel.create_iss_panel(green, True)
grey_panel_1 = build_panel.create_iss_panel(grey, False)
grey_panel_2 = build_panel.create_iss_panel(grey, True)
black_panel = build_panel.create_iss_panel(black, False)

# Initialize other variables
panel_cycle = False
heading_printed = False
playing_sound = False

display.set_all(black)

"""Fun little startup to show the ISS."""
for i in range(1, 5, 1):
    display.set_panel("top", grey_panel_1)
    display.set_panel("left", green_panel_1)
    display.set_panel("right", blue_panel_1)
    time.sleep(.5)
    display.set_panel("top", grey_panel_2)
    display.set_panel("left", green_panel_2)
    display.set_panel("right", blue_panel_2)
    time.sleep(.5)

display.set_all(black)

"""Infinite loop to keep tracking the ISS."""
while True:
    now = datetime.now().astimezone()
    display_now = now.strftime("%Y-%m-%d %H:%M:%S %Z")
    iss_latitude, iss_longitude = iss_utils.current_ISS_location()
    distance_iss = iss_utils.iss_distance(iss_latitude, iss_longitude)
    is_near, message = iss_utils.near_ISS(distance_iss)
    is_visible = sunrise_sunset_utils.is_twilight(now)
    if is_visible and is_near:
        message = "Visible"
    str_iss_latitude = "{0:.2f}N".format(iss_latitude)
    if iss_latitude < 0:
        str_iss_latitude = "{0:.2f}S".format(abs(iss_latitude))
    str_iss_longitude = "{0:.2f}E".format(iss_longitude)
    if iss_longitude < 0:
        str_iss_longitude = "{0:.2f}W".format(abs(iss_longitude))
    str_distance_iss = "{0:.0f}".format(distance_iss)
    do_not_disturb = check_do_not_disturb.check_do_not_disturb(now)
    speaker.volume = 25
    if not heading_printed:
        heading_line = "| {0} | {1} | {2} | {3} | {4} |".format("Current Time".ljust(23, " "),
                                                                "ISS Latitude".rjust(12, " "),
                                                                "ISS Longitude".rjust(13, " "),
                                                                "Distance".rjust(8, " "),
                                                                "Message".ljust(8, " "))
        print(heading_line)
        logger.info(heading_line)
    data_line = "| {0} | {1} | {2} | {3} | {4} |".format(display_now.ljust(23, " "),
                                                         str_iss_latitude.rjust(12, " "),
                                                         str_iss_longitude.rjust(13, " "),
                                                         str_distance_iss.rjust(8, " "),
                                                         message.ljust(8, " "))
    print(data_line)
    logger.info(data_line)
    heading_printed = True
    lumi_message = "{0} - {1} - {2}{3} - {4}".format(str_iss_latitude,
                                                     str_iss_longitude,
                                                     str_distance_iss,
                                                     properties["distance_measure"],
                                                     message)
    if is_visible and is_near:
        display.set_panel("top", green_panel_1)
        if not do_not_disturb:
            playing_sound = sound_utils.check_playing_sound(playing_sound, message)
        display.scroll_text(lumi_message, green, black, .5)
        display.set_panel("left", green_panel_1)
        display.set_panel("right", green_panel_1)
    elif is_near:
        display.set_panel("top", blue_panel_1)
        if not do_not_disturb:
            playing_sound = sound_utils.check_playing_sound(playing_sound, message)
        display.scroll_text(lumi_message, blue, black, .5)
        display.set_panel("left", blue_panel_1)
        display.set_panel("right", blue_panel_1)
    else:
        display.set_panel("top", black_panel)
        if panel_cycle:
            display.set_panel("top", grey_panel_1)
            panel_cycle = False
        else:
            display.set_panel("top", grey_panel_2)
            panel_cycle = True
        lumi_message = "{0} - {1} - {2}{3}".format(str_iss_latitude,
                                                         str_iss_longitude,
                                                         str_distance_iss,
                                                         properties["distance_measure"])
        display.scroll_text(lumi_message, grey, black, .5)
        display.set_panel("left", grey_panel_1)
        display.set_panel("right", grey_panel_1)
    time.sleep(4)
