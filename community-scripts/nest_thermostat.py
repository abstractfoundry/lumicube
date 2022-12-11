# Nest Thermostat
# uses the google_api.py and display_helpers.py modules to communicate with google to access nest thermostat information.
# Display current set point (or range for eco and HEATCOOL modes) and humidity.
# Will display in Celsius or Farenheit base on how the thermostat is configured.
# the top display will show the current mode (orange waves for heat mode, blue for cool mode.  other modes are "eco", fan and off).
# if the lumicube has buttons, the top and bottom buttons can be used to increase or decrease the current setpoint.
# the middle button will change the mode - how change mode works:
# - press the middle button, the mode icon on top will flash.  You have 30 seconds to change the mode with the top and bottom buttons.
# - Each time you press the top or bottom button, it'll scroll forward or back in the mode options, changing the top display to the next possible mode.
# - if you do select a different mode, do change to that mode, you must hit the center button again.  The mode will be changed and the top display 
#   will update to the new mode.
# setpoint color on the left will change to orange if currently  heating, and blue if currently cooling.
# if in "range" mode (eco mode or heatcool mode) there will be an orange or blue indicator to indicate which range we're seeing.
#
# you WILL need a google cloud account, and will need to 
# - create a new google cloud project - https://console.cloud.google.com/
# - enable the Smart Device Management API on that project
# - create a Web Application type credential - this will give you the oauth client_id and client_secret
# - on the oauth consent screen add a google user that has permission to access the project
# - create a device access project in the device access console - https://console.nest.google.com/device-access/project-list
#   you'll need to provide the oauth client id you got in the previous step
#   after this project is created, you'll have the project_id you'll need for configuration
# The program will look for it's configuration in the google folder in the home directory (usually /home/pi/Desktop)
# - create the google folder in the home folder
# - create a file called .nest-config in the google folder, with the folling format (add your project and client id values):
# {
#   "project_id" : "",
#   "client_id" : "",
#   "client_secret" : ""
# }
#
# when you run the first time, the lumicube will show a lock and question mark on screens.
# look at the console for a url
# - copy that url to a browser
# - you'll need to log in with an authorized google account, probably the one you used to create the project with, or another that you have authorized
# - allow the lumicube project to access the data
# - if all goes well, you should be redirected to the redirect_url that you configured - IN that url will be code.  copy that code from the URL
# check the console logs again, it should be asking you to put the code in a specific file 
# - create that file and add the code (I usually use echo to output to the file)
# - note that I would recommend editing a file of a different name, and renaming it when done, or just use echo "<code here" > <filename here>
#   if you open the final file in the editor the code may see it and try to read it immediately before you've saved it.
# the code will be used to fetch a refresh token and access token, which it will used to access the device api.  Even if you restart it will use the saved token.
# I've found that the token is good for about a week, after which you'll see the lock and question mark display - look at the console for instructions.
# 
# Useful links:
# - controlling a nest thermostat with python : https://www.wouternieuwerth.nl/controlling-a-google-nest-thermostat-with-python/
# - Device Access Guides : https://developers.google.com/nest/device-access/registration
# - Thermostat API - https://developers.google.com/nest/device-access/api/thermostat
# 
# Author: Kevin Haney
# Date: 12/9/2022
# v1.0
# history:
# - 1.0 - original (v1)

import os
import time
import requests
import json
import threading

import sys
sys.path.insert(0, '/home/pi/AbstractFoundry/Daemon/Scripts')
import display_helpers as helpers
import google_api as google

# right panel
question = [(8,6,1),(8,5,1),(8,4,1), (8,7,2),(8,6,2),(8,5,2),(8,4,2),(8,3,2), (8,7,3),(8,6,3),(8,3,3),(8,2,3),(8,0,3), (8,7,4),(8,6,4),(8,3,4),(8,2,4),(8,0,4),
            (8,7,5),(8,6,5),(8,5,5), (8,6,6),(8,5,6)]
# left panel(6,0,8),
lock = [(1,0,8),(1,1,8),(1,2,8),(1,3,8),(1,4,8), (2,0,8),(2,1,8),(2,2,8),(2,3,8),(2,4,8),(2,5,8),(2,6,8),(2,7,8), (3,0,8),(3,1,8),(3,2,8),(3,3,8),(3,4,8),(3,7,8),
        (4,0,8),(4,1,8),(4,2,8),(4,3,8),(4,4,8),(4,7,8), (5,0,8),(5,1,8),(5,2,8),(5,3,8),(5,4,8),(5,5,8),(5,6,8),(5,7,8), (6,0,8),(6,1,8),(6,2,8),(6,3,8),(6,4,8)]
lockShade = [(2,1,8),(2,3,8), (3,1,8),(3,3,8), (4,1,8),(4,3,8), (5,1,8),(5,3,8)]

#top panel
fan = [(0,8,0),(1,8,0),(6,8,0),(7,8,0), (0,8,1),(1,8,1),(2,8,1),(5,8,1),(6,8,1),(7,8,1), (1,8,2),(2,8,2),(5,8,2),(6,8,2),
       (3,8,3),(4,8,3), (3,8,4),(4,8,4), (1,8,5),(2,8,5),(5,8,5),(6,8,5), (0,8,6),(1,8,6),(2,8,6),(5,8,6),(6,8,6),(7,8,6),
       (0,8,7),(1,8,7),(6,8,7),(7,8,7)]

topWave = [(0,8,2),(0,8,3),(0,8,6),(0,8,7), (1,8,1),(1,8,2),(1,8,5), (2,8,0),(2,8,1),(2,8,4),(2,8,5), (3,8,0),(3,8,3), (4,8,2),(4,8,3), (5,8,1), (6,8,0),(6,8,1)]
    
botWave = [(1,8,6),(1,8,7), (2,8,6), (3,8,4),(3,8,5), (4,8,4),(4,8,7), (5,8,2),(5,8,3),(5,8,6),(5,8,7), (6,8,2),(6,8,5),(6,8,6), (7,8,0),(7,8,1),(7,8,4),(7,8,5)]

eco1 = [(1,8,3),(1,8,4),(1,8,5),(1,8,6), (2,8,2),(2,8,3),(2,8,4),(2,8,5),(2,8,6), (3,8,2),(3,8,3),(3,8,4),(3,8,5),(3,8,6),
       (4,8,1),(4,8,2),(4,8,3),(4,8,4),(4,8,5),(4,8,6), (5,8,1),(5,8,2),(5,8,3),(5,8,4),(5,8,5), (6,8,1),(6,8,2),(6,8,3)]
eco2 = [(2,8,5),(3,8,4),(4,8,3),(5,8,2)]

def set_display_mode(leds, status):
    for x in range(8):
        for z in range(8):
            leds[(x,8,z)] = black

    if status == None:
        display.set_3d(leds)
        return

    if status == 'FAN':
        for p in fan:
            leds[p] = white
    elif status == 'HEAT':
        for p in topWave:
            leds[p] = orange
        for p in botWave:
            leds[p] = orange
    elif status == 'COOL':
        for p in topWave:
            leds[p] = blue
        for p in botWave:
            leds[p] = blue
    elif status == 'HEATCOOL':
        for p in topWave:
            leds[p] = orange
        for p in botWave:
            leds[p] = blue
    elif status == 'ECO':
        for p in eco1:
            leds[p] = green
        for p in eco2:
            leds[p] = hsv_colour(.225,.88,.392) # 0c2264 decimal  12, 34, 100  hsv 225 88 39.2
    else:
        for p in topWave:
            leds[p] = grey
        for p in botWave:
            leds[p] = grey
    display.set_3d(leds)

def wait_on_buttons(delay):
    global button_warned
    action = None
    try:
        action = buttons.get_next_action(delay)
    except:
        if not button_warned:
            print('This lumicube does not appear to have buttons?')
            button_warned = True
        time.sleep(delay)
        
    return action
    
def get_current_mode(thermostat):
    if thermostat.fan_on:
        return 'FAN'
    elif thermostat.eco_mode:
        return 'ECO'
    return thermostat.mode

def blink_thread(leds,mode):
    while True:
        set_display_mode(leds,None)
        time.sleep(1)
        set_display_mode(leds,mode)
        time.sleep(1)

        if stop_blink_thread:
            break
        
def get_next_mode(mode,forward=True):
    modes = ['OFF','HEAT','COOL','HEATCOOL','ECO','FAN']
    
    for i in range(len(modes)):
        if modes[i] == mode:
            break
    
    if forward:
        i += 1
        if i == len(modes):
            i=0
    else:
        i -= 1
        if i < 0:
            i = len(modes)-1
            
    return modes[i]

# once they press the middle button, we're in wait mode.
# we'll flash the current selected mode with a thread.  
# we'll then wait for 30 seconds for another button to be pressed.
# if they push top or bottom button, we'll tell the blink thread to stop and wait,
# change the display mode to the next available mode, and start that blinking
# if they pressed the middle button, we'll stop the blink, then change the mode of the thermostat to the currently selected mode and return.
# if 30 seconds elapses before they press a button, we exit without any changes
def change_mode(leds,thermostat):
    global stop_blink_thread
    current_mode = get_current_mode(thermostat)
    new_mode = current_mode
    waiting = True
    while waiting:
        stop_blink_thread = False
        t1 = threading.Thread(target=blink_thread, args=(leds,new_mode))
        t1.start()
        
        button = wait_on_buttons(10)
        stop_blink_thread = True
        t1.join()    

        if button == None:
            print('no selection')
            set_display_mode(leds,current_mode)
            waiting = False
        elif button == 'top':
            new_mode = get_next_mode(new_mode,True)
            set_display_mode(leds,new_mode)
        elif button == 'bottom':
            new_mode = get_next_mode(new_mode,False)
        elif button == 'middle':
            if current_mode != new_mode or new_mode == 'FAN':
                print(f'changing mode from {current_mode} to {new_mode}')
                api.change_mode(new_mode,thermostat)
            else:
                print('no change')
            waiting = False    

def handle_action(leds,action,thermostat,heat):
    if action == None:
        return False
    if action == 'top':
        api.change_setpoint(1,thermostat,heat)
    elif action == 'bottom':
        api.change_setpoint(-1,thermostat,heat)
    elif action == 'middle':
        change_mode(leds,thermostat)
    time.sleep(1)
    return True
    
def display_test(leds):
    set_display_mode(leds,'HEAT')
    time.sleep(3)
    set_display_mode(leds,'COOL')
    time.sleep(3)
    set_display_mode(leds,'HEATCOOL')
    time.sleep(3)
    set_display_mode(leds,'FAN')
    time.sleep(3)
    set_display_mode(leds,'ECO')
    time.sleep(3)
    set_display_mode(leds,'OFF')
    time.sleep(3)
    
def show_security(leds):
    display.set_all(black)
    helpers.set_left(leds, lock, yellow, black, True)
    lockshadow = hsv_colour(.14,.063,.812) # cfc532,  decimal  207, 197, 50  hsv 14 6.3 81.2
    helpers.set_left(leds, lockShade, lockshadow, black, False)
    helpers.set_right(leds, question, red, black, True)
    display.set_3d(leds)
    
def get_set_temperature(t, heat):
    if t.mode == 'OFF':
        return None
    
    if t.eco_mode:
        if heat:
            return t.setpoint_eco_heat
        else:
            return t.setpoint_eco_cool
    if t.mode == 'HEAT':
        return t.setpoint_heat
    if t.mode == 'COOL':
        return t.setpoint_cool
    if t.mode == 'HEATCOOL':
        if t.status == 'HEATING':
            return t.setpoint_heat
        elif t.status == 'COOLING':
            return t.setpoint_cool
        else:
            if heat:
                return t.setpoint_heat
            else:
                return t.setpoint_cool

    return None

def get_font_color(t):
    font = grey
    if t.status == 'HEATING':
        font = orange
    elif t.status == 'COOLING':
        font = blue
    
    return font
        
def get_mode(t):
    mode = t.mode
    if t.fan_on:
        mode = 'FAN'
    if t.eco_mode:
        mode = 'ECO'

    return mode    

class Settings:
    def __init__(self, delay, humidity_every):
        # amount of time between updates
        self.delay = delay
        # normally show ambient temperature on the right, but every 'humidity_every' cycle show humidity
        self.humidity_every = humidity_every

if __name__ == "__main__":
    # if they don't have buttons, print a warning but just once
    button_warned = False
    settings = Settings(delay=10,humidity_every=12)
    humidity_count = 0

    display.set_all(black)

    working_directory = os.getcwd()
    print('working directory is ',working_directory)

    # initialize our led dictionary^M
    leds = {}
    for x in range(9):
        for y in range(9):
            for z in range(9):
                leds[(x,y,z)] = black

    api = google.GoogleApi(working_directory)
    #print(api.refresh_token,api.access_token,api.is_permissioned())
    if api.is_permissioned() == False:
        show_security(leds);
        
        if api.get_permission() == False:
            #show some indication that it failed?
            print('could not get permission')
            exit()

        # show some indication that it was successful?
        display.set_all(black)
        
    #display_test(leds)

    thermostats = api.fetch_thermostats()
    if len(thermostats) == 0:
        print('no thermostats found!')
        exit()

    last = ''
    heat = True
    while True:
      background = black
      font = white
      set_temp = 0
      for d in thermostats:
        t = api.fetch_thermostat(d)
        if t == None:
            print('couldn''t get thermostat - did credentials expire?')
            if api.is_permissioned() == False:
                print('restart the program and re-permission the application')
                show_security(leds);
                exit()
            time.sleep(10)
        else:
            #print(t)
            setTemp = get_set_temperature(t,heat)
            ambientTemp = t.ambient_temperature
            font = get_font_color(t)
            mode = get_mode(t)
            
            set_display_mode(leds, mode)
            
            text = f'{t}'
            if last != text:
              print(text)
            last = text
    
            if setTemp is not None:
                setTemp = int(round(setTemp,0))
            helpers.set_digits(leds,'left',setTemp,font,background)
            humidity_count +=1
            if humidity_count > settings.humidity_every:
                humidity_count = 0
                helpers.set_digits(leds,'right',int(round(t.humidity,0)),yellow,background)
            else:
                helpers.set_digits(leds,'right',int(round(ambientTemp,0)),green,background)
                
            if (t.eco_mode or t.mode == 'HEATCOOL') and t.status == 'OFF':
                if heat:
                    leds[(4,0,8)] = orange
                else:
                    leds[(4,0,8)] = blue

            display.set_3d(leds)
            
            action = wait_on_buttons(settings.delay)
            if action != None:
                if handle_action(leds,action,t,heat):
                    #toggling heat because if they changed temp during HEATCOOL cycle I want to show the same cycle again
                    heat = not heat

            heat = not heat