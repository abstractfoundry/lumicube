#!/usr/bin/python3

from foundry_api.standard_library import *


# Predefined colors

D = 0x5A5A5A # dark grey
G = grey
w = white
r = red
o = orange
y = yellow
g = green
c = cyan
b = blue
m = magenta
p = pink
P = purple

icon_sun = [ [0,o,0,o,o,0,o,0], [o,0,y,y,y,y,0,o], [0,y,y,y,y,y,y,0], [o,y,y,y,y,y,y,o], [o,y,y,y,y,y,y,o], [0,y,y,y,y,y,y,0], [o,0,y,y,y,y,0,o], [0,o,0,o,o,0,o,0] ]
##icon_clear_day = [ [0,0,y,0,0,y,0,0], [0,0,0,0,0,0,0,0], [y,0,y,y,y,y,0,y], [0,0,y,y,y,y,0,0], [0,0,y,y,y,y,0,0], [y,0,y,y,y,y,0,y], [0,0,0,0,0,0,0,0], [0,0,y,0,0,y,0,0] ]
icon_moon = [ [0,0,G,w,w,w,0,0], [0,G,w,G,0,0,G,0], [G,w,w,0,0,0,0,0], [w,w,w,0,0,0,0,0], [w,w,w,0,0,0,0,0], [G,w,w,G,0,0,0,G], [0,G,w,w,w,w,G,0], [0,0,G,G,G,G,0,0] ]
##icon_clear_night = [ [0,0,b,0,0,b,0,0], [0,0,0,0,0,0,0,0], [b,0,b,b,b,b,0,b], [0,0,b,b,b,b,0,0], [0,0,b,b,b,b,0,0], [b,0,b,b,b,b,0,b], [0,0,0,0,0,0,0,0], [0,0,b,0,0,b,0,0] ]
icon_clouds = [ [0,0,o,o,o,0,0,0], [0,o,y,y,y,o,0,0], [o,y,y,y,D,D,D,0], [o,y,y,D,G,G,G,D], [o,y,y,D,G,G,G,G], [o,o,D,G,G,G,G,G], [0,D,G,G,G,G,G,G], [D,G,G,G,G,G,G,G] ]
icon_rain = [ [0,0,0,G,G,G,0,0], [0,0,G,G,G,G,G,0], [0,0,G,G,G,G,G,0], [G,G,G,G,G,G,G,G], [0,0,0,0,0,0,0,0], [b,0,0,b,0,0,b,0], [0,0,0,0,0,0,0,0], [0,b,0,0,b,0,0,b] ]
icon_raindrop = [ [0,0,0,b,0,0,0,0], [0,0,0,b,0,0,0,0], [0,0,w,b,b,0,0,0], [0,w,w,b,b,b,0,0], [b,w,b,b,b,b,b,0], [b,b,b,b,b,b,b,0], [b,w,b,b,b,b,b,0], [0,b,b,b,b,b,0,0] ]
icon_thunder = [ [0,0,o,y,y,o,0,0], [0,0,y,y,o,0,0,0], [0,o,y,o,0,0,0,0], [0,y,y,0,0,0,0,0], [o,y,y,y,y,y,o,0], [0,0,0,0,y,o,0,0], [0,0,0,y,o,0,0,0], [0,0,0,o,0,0,0,0] ]
icon_snow = [ [0,0,0,w,0,0,0,0], [0,0,w,w,w,0,0,0], [0,0,0,w,0,0,w,0], [0,w,0,w,w,w,w,w], [w,w,w,w,w,0,w,0], [0,w,0,0,w,0,0,0], [0,0,0,w,w,w,0,0], [0,0,0,0,w,0,0,0] ]
icon_question_mark = [ [0,r,r,r,r,r,r,0], [r,r,r,r,r,r,r,r], [r,r,0,0,0,0,r,r], [0,0,0,0,0,0,r,r], [0,0,0,r,r,r,r,0], [0,0,0,r,r,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,r,r,0,0,0] ]


# import required modules
import requests, json

# Enter your API key here
api_key = "" # Create an account and put the API key here

# base_url variable to store url
base_url = "http://api.openweathermap.org/data/2.5/weather?"

# Give city id
city_id =  # Look up your city on openweathermap.org

# complete_url variable to store
# complete url address
complete_url = base_url + "appid=" + api_key + "&id=" + city_id

# get method of requests module
# return response object
response = requests.get(complete_url)

# json method of response object
# convert json format data into
# python format data
x = response.json()

# Now x contains list of nested dictionaries
# Check the value of "cod" key is equal to
# "404", means city is found otherwise,
# city is not found
if x["cod"] != "404":

  # store the value of "main"
  # key in variable y
  y = x["main"]

  # store the value corresponding
  # to the "temp" key of y
  current_temperature = y["temp"]
  celsius_temperature = int(current_temperature - 273.15)

  # store the value corresponding
  # to the "pressure" key of y
  current_pressure = y["pressure"]

  # store the value corresponding
  # to the "humidity" key of y
  current_humidity = y["humidity"]

  # store the value of "weather"
  # key in variable w
  w = x["weather"]

  # store the value corresponding
  # to the "description" key at
  # the 0th index of z
  weather_description = w[0]["description"]

  # colour of the text based on temperature
  if celsius_temperature >= 40: colour = red
  elif celsius_temperature >= 30 and celsius_temperature < 40: colour = orange
  elif celsius_temperature >= 20 and celsius_temperature < 30: colour = yellow
  elif celsius_temperature >= 10 and celsius_temperature < 20: colour = green
  elif celsius_temperature >= 0 and celsius_temperature < 10: colour = cyan
  elif celsius_temperature >= -10 and celsius_temperature < 0: colour = blue
  else: colour = white

  z = colour # because i use 'z' in the number icons

  # number icons

  number_one = [ [0,0,0,0,0,0,0,0], [z,z,z,z,0,0,0,0], [0,0,0,z,0,0,0,0], [0,0,0,z,0,0,0,0], [0,0,0,z,0,0,0,0], [0,0,0,z,0,0,0,0], [0,0,0,z,0,0,0,0], [z,z,z,z,z,z,z,0] ]
  number_two = [ [0,0,0,0,0,0,0,0], [z,z,z,z,z,z,z,0], [0,0,0,0,0,0,z,0], [0,0,0,0,0,0,z,0], [z,z,z,z,z,z,z,0], [z,0,0,0,0,0,0,0], [z,0,0,0,0,0,0,0], [z,z,z,z,z,z,z,0] ]
  number_three = [ [0,0,0,0,0,0,0,0], [z,z,z,z,z,z,z,0], [0,0,0,0,0,0,z,0], [0,0,0,0,0,0,z,0], [z,z,z,z,z,z,z,0], [0,0,0,0,0,0,z,0], [0,0,0,0,0,0,z,0], [z,z,z,z,z,z,z,0] ]
  number_four = [ [0,0,0,0,0,0,0,0], [z,0,0,0,0,0,z,0], [z,0,0,0,0,0,z,0], [z,0,0,0,0,0,z,0], [z,z,z,z,z,z,z,0], [0,0,0,0,0,0,z,0], [0,0,0,0,0,0,z,0], [0,0,0,0,0,0,z,0] ]
  number_five = [ [0,0,0,0,0,0,0,0], [z,z,z,z,z,z,z,0], [z,0,0,0,0,0,0,0], [z,0,0,0,0,0,0,0], [z,z,z,z,z,z,z,0], [0,0,0,0,0,0,z,0], [0,0,0,0,0,0,z,0], [z,z,z,z,z,z,z,0] ]
  number_six = [ [0,0,0,0,0,0,0,0], [z,z,z,z,z,z,z,0], [z,0,0,0,0,0,0,0], [z,0,0,0,0,0,0,0], [z,z,z,z,z,z,z,0], [z,0,0,0,0,0,z,0], [z,0,0,0,0,0,z,0], [z,z,z,z,z,z,z,0] ]
  number_seven = [ [0,0,0,0,0,0,0,0], [z,z,z,z,z,z,z,0], [0,0,0,0,0,0,z,0], [0,0,0,0,0,0,z,0], [0,0,0,0,0,0,z,0], [0,0,0,0,0,0,z,0], [0,0,0,0,0,0,z,0], [0,0,0,0,0,0,z,0] ]
  number_eight = [ [0,0,0,0,0,0,0,0], [z,z,z,z,z,z,z,0], [z,0,0,0,0,0,z,0], [z,0,0,0,0,0,z,0], [z,z,z,z,z,z,z,0], [z,0,0,0,0,0,z,0], [z,0,0,0,0,0,z,0], [z,z,z,z,z,z,z,0] ]
  number_nine = [ [0,0,0,0,0,0,0,0], [z,z,z,z,z,z,z,0], [z,0,0,0,0,0,z,0], [z,0,0,0,0,0,z,0], [z,z,z,z,z,z,z,0], [0,0,0,0,0,0,z,0], [0,0,0,0,0,0,z,0], [z,z,z,z,z,z,z,0] ]
  number_zero = [ [0,0,0,0,0,0,0,0], [z,z,z,z,z,z,z,0], [z,0,0,0,0,0,z,0], [z,0,0,0,0,0,z,0], [z,0,0,0,0,0,z,0], [z,0,0,0,0,0,z,0], [z,0,0,0,0,0,z,0], [z,z,z,z,z,z,z,0] ]

  # text based on celsius temperature
  strtemp = str(celsius_temperature)
  firstnumber = strtemp[:1]
  secondnumber = strtemp[1:2]

  if firstnumber == "1": left_number = number_one
  elif firstnumber == "2": left_number = number_two
  elif firstnumber == "3": left_number = number_three
  elif firstnumber == "4": left_number = number_four
  elif firstnumber == "5": left_number = number_five
  elif firstnumber == "6": left_number = number_six
  elif firstnumber == "7": left_number = number_seven
  elif firstnumber == "8": left_number = number_eight
  elif firstnumber == "9": left_number = number_nine
  elif firstnumber == "0": left_number = number_zero
  else: left_number = icon_question_mark

  if secondnumber == "1": right_number = number_one
  elif secondnumber == "2": right_number = number_two
  elif secondnumber == "3": right_number = number_three
  elif secondnumber == "4": right_number = number_four
  elif secondnumber == "5": right_number = number_five
  elif secondnumber == "6": right_number = number_six
  elif secondnumber == "7": right_number = number_seven
  elif secondnumber == "8": right_number = number_eight
  elif secondnumber == "9": right_number = number_nine
  elif secondnumber == "0": right_number = number_zero
  else: right_number = icon_question_mark


  # weather icon based on openweathermap icon

  weather_icon = w[0]["icon"]

  if weather_icon == "01d": icon = icon_sun
  elif weather_icon == "01n": icon = icon_moon
  elif weather_icon == "02d": icon = icon_clouds
  elif weather_icon == "02n": icon = icon_clouds
  elif weather_icon == "03d": icon = icon_clouds
  elif weather_icon == "03n": icon = icon_clouds
  elif weather_icon == "04d": icon = icon_clouds
  elif weather_icon == "04n": icon = icon_clouds
  elif weather_icon == "10d": icon = icon_rain
  elif weather_icon == "10n": icon = icon_rain
  elif weather_icon == "09d": icon = icon_raindrop
  elif weather_icon == "09n": icon = icon_raindrop

  else: icon = icon_question_mark

  # first set lumicube display to black
  display.set_all(black)
  # lumicube display
  display.set_panel("top", icon)
  display.set_panel("left", left_number)
  display.set_panel("right", right_number)

else:
  print(" Wrong city ID ")
