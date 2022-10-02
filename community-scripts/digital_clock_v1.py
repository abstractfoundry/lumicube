# credit to @arustleund#0019 (Discord) for the original script
# modified by @darkalexwang 10-01-2022

# ToDo: have the second dots come to life in a spiral as an optional mode
# ToDo: develop a menu for the rear screen so the config below can be changed on the fly (up/down/enter buttons)
# ToDo: load and save config to file

import datetime
import traceback
from pathlib import Path
import pyttsx3

import requests

# Digital Clock

# config
enable_check_temperature_button = True
chime_on_hour = True
chime_on_half_hour = True
chime_disabled_hours = range(8)  # iterable containing hours by which clock shouldn't chime
chime_file_path = "Cuckoo.mp3"  # http://sfxcontent.s3.amazonaws.com/soundfx/Cartoon-Cuckoo1.mp3
#chime_file_path = "CharlieSheen-001.mp3"
dictate_on_hour = True
dictate_on_half_hour = True
hour_color_hue = 0.8
hour_color_saturation = 1
min_ambient_light_for_max_brightness = 3000 # the minimum ambient light level to display pixels at full brightness
min_brightness = 0.4 # range 0-1
minute_color_hue = 0
minute_color_saturation = 0
prefer_double_digits = True
use_random_second_colors = True
use_random_minute_colors = True
use_random_hour_colors = True
refresh_rate = 1/20
second_color_hue = 0.6
second_color_saturation = 0.8
speaker.volume = 10
use_random_dots_for_seconds = True # fill in the top with dots in a random pattern else display numbers for seconds
use_24_hour_clock = True

# weather config
openweathermap_api_key = ""
params = {
    "appid": openweathermap_api_key,
    "id": "",  # city id as per openweathermap.org; search your city and take ID from URL
    "units": "metric"
}
current_weather_url = "https://api.openweathermap.org/data/2.5/weather?"
# disable weather functionality if no api key
# ToDo: Add functionality for the env_sensor when it is delivered as an alternative to the API
if not openweathermap_api_key:
    enable_check_temperature_button = False

# engine initiate for text to speach
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', 'english_rp+f3')

def ampm_hour(hour: int) -> int:
    if hour > 11:
        hour -= 12
    return 12 if hour == 0 else hour


def chime(hour):
    if hour not in chime_disabled_hours:
        if Path(chime_file_path).exists():
            speaker.play(chime_file_path)


def draw_number(leds: dict, number: int, x_offset: int, y_offset: int, color: int) -> None:
    mask = pow(2, 9 - number)
    for y in range(8):
        for x in range(3):
            tf_index = (21 - (y * 3)) + (x % 3)
            tf_value = tall_font[tf_index]
            bit_on = bool(mask & tf_value)
            leds[x + x_offset, y + y_offset] = color if bit_on else 0


def draw_double_digit_number(leds: dict, number: int, x_offset: int, y_offset: int, color: int) -> None:
    draw_number(leds, number // 10, x_offset, y_offset, color)
    draw_number(leds, number % 10, x_offset + 4, y_offset, color)


def get_seconds_colors() -> list[tuple[float, float]]:
    if use_random_second_colors:
        return [random_color() for _ in range(64)]
    return [(second_color_hue, second_color_saturation) for _ in range(64)]


def get_temperature() -> None:
    global displaying_weather, temperature
    if displaying_weather == 0:
        display.set_panel("top", [(black,)*8]*8)
        try:
            # note: doesn't handle negative or > 100
            # really need a scrolling text function for a single panel!
            temperature = int(requests.get(current_weather_url, params).json()['main']['temp'])
        except:
            temperature = 0

    displaying_weather += refresh_rate
    if displaying_weather >= 5:  # slight pause before clearing screen
        temperature = 0
        displaying_weather = 0
        display.set_panel("top", [(black,)*8]*8)


def random_color() -> tuple[float, float]:
    return (random.randint(0, 100)/100, random.randint(0, 100)/100)



tall_font = [
    0b1011111111, 0b1111011111, 0b1011111111,
    0b1100111011, 0b0100000000, 0b1011100111,
    0b1000111011, 0b0100000000, 0b1011100111,
    0b1011111011, 0b0111111011, 0b1011111111,
    0b1010001010, 0b0100000000, 0b1001111111,
    0b1010001010, 0b0100000000, 0b1001111111,
    0b1010001010, 0b0100000000, 0b1001111111,
    0b1111011011, 0b1111011011, 0b1111111111
]
big_font = [
    [
        [0,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1],
        [1,1,1,0,0,1,1,1],
        [1,1,1,0,0,1,1,1],
        [1,1,1,0,0,1,1,1],
        [1,1,1,0,0,1,1,1],
        [1,1,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,0],
    ],
    [
        [0,0,0,1,1,1,0,0],
        [0,0,1,1,1,1,0,0],
        [0,1,1,1,1,1,0,0],
        [0,0,0,1,1,1,0,0],
        [0,0,0,1,1,1,0,0],
        [0,0,0,1,1,1,0,0],
        [0,0,0,1,1,1,0,0],
        [0,0,0,1,1,1,0,0],
    ],
    [
        [0,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1],
        [1,1,1,0,0,1,1,1],
        [0,0,0,0,1,1,1,0],
        [0,0,1,1,1,0,0,0],
        [1,1,1,0,0,0,0,0],
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1],
    ],
    [
        [1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1],
        [0,0,0,0,0,1,1,1],
        [1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,0],
        [0,0,0,0,0,1,1,1],
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,0],
    ],
    [
        [1,1,1,0,1,1,1,0],
        [1,1,1,0,1,1,1,0],
        [1,1,1,0,1,1,1,0],
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1],
        [0,0,0,0,1,1,1,0],
        [0,0,0,0,1,1,1,0],
        [0,0,0,0,1,1,1,0],
    ],
    [
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1],
        [1,1,1,0,0,0,0,0],
        [1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1],
        [0,0,0,0,0,1,1,1],
        [1,1,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,0],
    ],
    [
        [0,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1],
        [1,1,1,0,0,0,0,0],
        [1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1],
        [1,1,1,0,0,1,1,1],
        [1,1,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,0],
    ],
    [
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1],
        [0,0,0,0,0,1,1,1],
        [0,0,0,0,1,1,1,0],
        [0,0,0,1,1,1,0,0],
        [0,0,1,1,1,0,0,0],
        [0,0,1,1,1,0,0,0],
        [0,0,1,1,1,0,0,0],
    ],
    [
        [0,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1],
        [1,1,1,0,0,1,1,1],
        [0,1,1,1,1,1,1,0],
        [0,1,1,1,1,1,1,0],
        [1,1,1,0,0,1,1,1],
        [1,1,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,0],
    ],
    [
        [0,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1],
        [1,1,1,0,0,1,1,1],
        [1,1,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,1],
        [0,0,0,0,0,1,1,1],
        [1,1,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,0],
    ]
]


display.set_all(black)
rand_indexes = [x for x in range(64)]
random.shuffle(rand_indexes)
colors = get_seconds_colors()
reset_indexes = False
displaying_weather = 0
temperature = 0
time_now = datetime.datetime.now()

recent_hour = (time_now.hour - 1, time_now.hour, time_now.hour - 12) # starting hours to not chime on
recent_minute = time_now.minute - 1
try:
    while True:
        if buttons.middle_pressed:
            use_random_dots_for_seconds = not use_random_dots_for_seconds
        if buttons.bottom_pressed:
            use_24_hour_clock = not use_24_hour_clock

        leds = {(x, y):0 for x in range(16) for y in range(16)}
        max_brightness = max(min_brightness, min(1, light_sensor.ambient_light / min_ambient_light_for_max_brightness))

        time_now = datetime.datetime.now()

        # set hour digits for left panel
        latest_hour = ampm_hour(time_now.hour) if not use_24_hour_clock else time_now.hour
        # change colours of hour if optioned and hour has changed
        if latest_hour not in recent_hour:
            if chime_on_hour:
                chime(time_now.hour)
            if dictate_on_hour:
                engine.say(f"{ampm_hour(time_now.hour)} o clock")
                engine.runAndWait()
                #speaker.say(f"{ampm_hour(time_now.hour)} o clock")

            if use_random_hour_colors:
                hour_color_hue, hour_color_saturation = random_color()
            recent_hour = (latest_hour, latest_hour - 12)  # record both, don't want it to chime when changing to/from 24hrs

        if not prefer_double_digits and latest_hour < 10:
            for y in range(8):
                for x in range(8):
                    pixel_on = big_font[latest_hour][7 - y][x] == 1
                    leds[x, y] = hsv_colour(hour_color_hue, hour_color_saturation, max_brightness) if pixel_on else 0
        else:
            draw_double_digit_number(leds, latest_hour, 1, 0, hsv_colour(hour_color_hue, hour_color_saturation, max_brightness))

        # set minutes digits for right panel
        # change colours of minute if optioned and minute has changed
        if time_now.minute != recent_minute:
            if time_now.minute == 30:
                if chime_on_half_hour:
                    chime(time_now.hour)
                if dictate_on_half_hour:
                    engine.say(f"{ampm_hour(time_now.hour)} thirty")
                    engine.runAndWait()
                    #speaker.say(f"{ampm_hour(time_now.hour)} thirty")

            if use_random_minute_colors:
                minute_color_hue, minute_color_saturation = random_color()
            recent_minute = time_now.minute
        draw_double_digit_number(leds, time_now.minute, 9, 0, hsv_colour(minute_color_hue, minute_color_saturation, max_brightness))

        # handle button press - if pressed, get weather and set the top panel digits to temperature
        if enable_check_temperature_button and (buttons.top_pressed or displaying_weather != 0):
            get_temperature()
            draw_double_digit_number(leds, temperature, 1, 8, hsv_colour(second_color_hue, second_color_saturation, max_brightness))

        # if top panel isn't currently displaying weather, set seconds for top panel
        if not displaying_weather:
            if not use_random_dots_for_seconds:
                draw_double_digit_number(leds, time_now.second, 1, 8, hsv_colour(second_color_hue, second_color_saturation, max_brightness))
            else:
                if (time_now.second == 0 and not reset_indexes):
                    random.shuffle(rand_indexes)
                    reset_indexes = True
                    colors = get_seconds_colors()
                elif time_now.second != 0:
                    reset_indexes = False

                percent_seconds = ((time_now.second * 1000000) + time_now.microsecond) / 60000000
                how_lit = (percent_seconds * 64)

                for y in range(8):
                    for x in range(8):
                        led_index = (y * 8) + x
                        hue, saturation = colors[led_index]
                        if how_lit >= led_index:
                            diff = how_lit - led_index
                            plot_x = rand_indexes[led_index] % 8
                            plot_y = rand_indexes[led_index] // 8
                            percent_lit = min(1, diff)
                            adjusted_lit = max_brightness * percent_lit
                            leds[plot_x, plot_y + 8] = hsv_colour(hue, saturation, adjusted_lit)

        display.set_leds(leds)
        time.sleep(refresh_rate)
except Exception:
    print(traceback.format_exc())
    screen.draw_rectangle(0, 0, 320, 240, black)
    screen.write_text(0, 0, traceback.format_exc(), 1, black, white)
