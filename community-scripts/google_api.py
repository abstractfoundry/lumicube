# Google API
# code to access the google api fetch nest thermostat information
# this module can be run without the display code, and will dump results to the console.
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
from datetime import datetime, timedelta

class Thermostat:
  def __init__(self, t):
    self.device_id = ''
    self.name = ''
    self.humidity = 0
    self.connectivity = ''
    self.mode = ''
    self.eco_mode = False
    self.fan_on = False
    self.setpoint_eco_heat = 0
    self.setpoint_eco_cool = 0
    self.status = ''
    self.scale = 'F'
    self.setpoint_heat = 0
    self.setpoint_cool = 0
    self.ambient_temperature = 0
    
    self.device_id = t['name']
    if 'traits' in t:
      traits = t['traits']
      self.name = traits['sdm.devices.traits.Info']['customName']
      scale = traits['sdm.devices.traits.Settings']['temperatureScale']
      if scale == 'FAHRENHEIT':
        self.scale = 'F'
      else:
        self.scale = 'C'
      self.humidity = traits['sdm.devices.traits.Humidity']['ambientHumidityPercent']
      self.connectivity = traits['sdm.devices.traits.Connectivity']['status']
      self.mode = traits['sdm.devices.traits.ThermostatMode']['mode']
      self.fan_on = traits['sdm.devices.traits.Fan']['timerMode'] != 'OFF'
      self.eco_mode = traits['sdm.devices.traits.ThermostatEco']['mode'] == 'MANUAL_ECO'
      self.setpoint_eco_heat = traits['sdm.devices.traits.ThermostatEco']['heatCelsius']
      if self.scale == 'F':
        self.setpoint_eco_heat = Thermostat.cToF(self.setpoint_eco_heat)
      self.setpoint_eco_cool = traits['sdm.devices.traits.ThermostatEco']['coolCelsius']
      if self.scale == 'F':
        self.setpoint_eco_cool = Thermostat.cToF(self.setpoint_eco_cool)
      self.status = traits['sdm.devices.traits.ThermostatHvac']['status']
      setpoint = traits['sdm.devices.traits.ThermostatTemperatureSetpoint']
      if 'heatCelsius' in setpoint:
        self.setpoint_heat = setpoint['heatCelsius']
        if self.scale == 'F':
          self.setpoint_heat = Thermostat.cToF(self.setpoint_heat)
      if 'coolCelsius' in setpoint:
        self.setpoint_cool = setpoint['coolCelsius']
        if self.scale == 'F':
          self.setpoint_cool = Thermostat.cToF(self.setpoint_cool)
      self.ambient_temperature = traits['sdm.devices.traits.Temperature']['ambientTemperatureCelsius']
      if self.scale == 'F':
        self.ambient_temperature = Thermostat.cToF(self.ambient_temperature)

      
  def __str__(self):
      fan = 'off'
      if self.fan_on:
        fan = 'on'
      info = f'{self.name} -- mode: {self.mode}, status: {self.status}, fan: {fan}, '
      if self.eco_mode:
        info += 'eco set: ' + f'{self.setpoint_eco_heat:3.1f} {self.scale} to {self.setpoint_eco_cool:3.1f} {self.scale}, '
      else:
        if self.mode == 'HEAT':
            info += 'set: ' + f'{self.setpoint_heat:3.1f} {self.scale}, '
        elif self.mode == 'COOL':
            info += 'set: ' + f'{self.setpoint_cool:3.1f} {self.scale}, '
        elif self.mode == 'HEATCOOL':
            info += 'set: ' + f'{self.setpoint_heat:3.1f} {self.scale} to {self.setpoint_cool:3.1f} {self.scale}, '
      info += 'current ' + f'{self.ambient_temperature:3.1f} {self.scale}, '
      info += f'humidity {self.humidity:3.1f} %'
      return info
      
  @staticmethod
  def cToF(celsius):
    return ((9/5)*celsius) + 32

  @staticmethod
  def fToC(farenheit):
    return (farenheit-32)*5/9

class GoogleApi:
    ACCESS_TOKEN_LIFETIME_MINUTES = 30
    
    def __init__(self, working_directory):
        self.working_directory = working_directory
        self._config_file_name = self.working_directory+'/google/.nest-config'
        try:
            with open(self._config_file_name,'r') as config_file:
                config_json = json.load(config_file)
            print('found config')
            self.project_id = config_json['project_id']
            self.client_id = config_json['client_id']
            self.client_secret = config_json['client_secret']

        except FileNotFoundError:
            print('did not find config file at',self._config_file_name)
            self.refresh_token = ''
            return

        self.access_token = ''
        self.access_token_expires = datetime.now()
        self.working_directory = working_directory
        self._token_file_name = self.working_directory+'/google/.refreshtoken'

        self.refresh_token = ''

        try:
            tokenFile = open(self._token_file_name,'r')
            self.refresh_token = tokenFile.read()
            tokenFile.close()
            print('found token')
            #print(self.refresh_token)
        except FileNotFoundError:
            print('no token file found in',self._token_file_name)
            self.refresh_token = ''

        if self.refresh_token != '':
            self.access_token = self.fetch_access_token()

    def is_permissioned(self):
        return self.refresh_token != ''

    def get_permission_url(self):
        redirect_uri = 'https://www.google.com'
        return 'https://nestservices.google.com/partnerconnections/'+self.project_id+'/auth?redirect_uri='+redirect_uri+'&access_type=offline&prompt=consent&client_id='+self.client_id+'&response_type=code&scope=https://www.googleapis.com/auth/sdm.service'

    def get_permission(self):
        redirect_uri = 'https://www.google.com'
        url = 'https://nestservices.google.com/partnerconnections/'+self.project_id+'/auth?redirect_uri='+redirect_uri+'&access_type=offline&prompt=consent&client_id='+self.client_id+'&response_type=code&scope=https://www.googleapis.com/auth/sdm.service'
                
        print("Go to this URL to log in:", flush=True)
        print(url)

        code = ''
        code_file_name = self.working_directory + '/google/.code'
        if os.path.exists(code_file_name):
            os.remove(code_file_name)
    
        while code == '':
            print(f'waiting for code in {code_file_name}',flush=True)
            try:
                code_file = open(code_file_name,'r')
                code = code_file.read()
            except FileNotFoundError:
                time.sleep(10)

        print(f'got code{code}',flush=True)
        self.fetch_refresh_token(code)
        return self.is_permissioned()

    def fetch_refresh_token(self,code):
        redirect_uri = 'https://www.google.com'
        print('fetch refresh token')
                
        params = (
            ('client_id', self.client_id),
            ('client_secret', self.client_secret),
            ('code', code),
            ('grant_type', 'authorization_code'),
            # get a new access token
            ('redirect_uri', redirect_uri),
        )
        response = requests.post('https://www.googleapis.com/oauth2/v4/token', params=params)
        response_json = response.json()

        self.access_token = response_json['token_type'] + ' ' + str(response_json['access_token'])
        self.access_token_expires = datetime.now() + timedelta(minutes=self.ACCESS_TOKEN_LIFETIME_MINUTES)
        self.refresh_token = response_json['refresh_token']
        print('created token')
        #save it
        refresh_file = open(self._token_file_name,'w')
        refresh_file.write(self.refresh_token)
        refresh_file.close()
        print('saved token to',self._token_file_name)
        return self.refresh_token

    def fetch_access_token(self):
        # get a new access token
        params = (
            ('client_id', self.client_id),
            ('client_secret', self.client_secret),
            ('refresh_token', self.refresh_token),
            ('grant_type', 'refresh_token'),
        )

        response = requests.post('https://www.googleapis.com/oauth2/v4/token', params=params)
        if response.status_code != 200:
            print(response,response.status_code,response.reason)
            if response.status_code == 400:
                self.refresh_token = ''
            self.access_token = ''
            return ''
            
        response_json = response.json()
        #  print(response_json)
        self.access_token = response_json['token_type'] + ' ' + response_json['access_token']
        self.access_token_expires = datetime.now() + timedelta(minutes=self.ACCESS_TOKEN_LIFETIME_MINUTES)
        #print('new Access token: ' + self.access_token,'expires',self.access_token_expires)
        return self.access_token
        
    def check_access_token(self):
        if self.access_token == '' or datetime.now() > self.access_token_expires:
            print('refreshing access token')
            self.fetch_access_token()

        return self.access_token != ''        

    def fetch_thermostats(self):
        if self.check_access_token() == False:
            print('could not refresh access token')
            return []
            
        # Get devices
        url_get_devices = 'https://smartdevicemanagement.googleapis.com/v1/enterprises/' + self.project_id + '/devices'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': self.access_token,
        }

        response = requests.get(url_get_devices, headers=headers)
        if response.status_code != 200:
            print(response,response.status_code,response.reason)
        response_json = response.json()

        #print(response_json)
        thermostats = []
        devices = response_json['devices']
        #print('found',len(devices),'devices')
        for d in devices:
            if 'type' in d and d['type'] == 'sdm.devices.types.THERMOSTAT':
                traits = d['traits']
                #print(traits)
            #    print('device :',traits['sdm.devices.traits.Info']['customName'])
            #    for t in traits:
            #       for x in traits[t]:
            #         print(t,x,traits[t][x])
                thermostats.append(Thermostat(d))    
        return thermostats
  
    def fetch_thermostat(self, t):
        if self.check_access_token() == False:
            print('could not refresh access token')
            return None

        # Get devices
        url_get_device = 'https://smartdevicemanagement.googleapis.com/v1/' + t.device_id
        headers = {
            'Content-Type': 'application/json',
            'Authorization': self.access_token,
        }

        success = False
        while not success:
            response = requests.get(url_get_device, headers=headers)
            if response.status_code != 200:
                print(response,response.status_code,response.reason)
                time.sleep(30)
            else:
                success = True
                response_json = response.json()
                #print(response,response_json)

        d = response_json
        #print(d)
        if 'type' in d and d['type'] == 'sdm.devices.types.THERMOSTAT':
            traits = d['traits']
            #print(traits)
        #      print('device :',traits['sdm.devices.traits.Info']['customName'])
        #      for t in traits:
        #       for x in traits[t]:
        #         print(t,x,traits[t][x])
        return Thermostat(d)
  
    def change_setpoint(self, change, thermostat, heat):
        if self.check_access_token() == False:
            print('could not refresh access token')
            return False

        current_setpoint = None
        params = None
        if thermostat.eco_mode:
            print('eco mode not supported yet for change_setpoint()',flush=True)
            return
        elif thermostat.mode == 'HEATCOOL':
            if thermostat.eco_mode:
                setpoint_heat = thermostat.setpoint_eco_heat
                setpoint_cool = thermostat.setpoint_eco_cool
            else:
                setpoint_heat = thermostat.setpoint_heat
                setpoint_cool = thermostat.setpoint_cool

            if heat:
                new_setpoint_heat = change + setpoint_heat
                new_setpoint_cool = setpoint_cool
            else:
                new_setpoint_heat = setpoint_heat
                new_setpoint_cool = change + setpoint_cool
            
            print(f'changing range from {setpoint_heat:3.1f} {thermostat.scale} - {setpoint_cool:3.1f} {thermostat.scale} to {new_setpoint_heat:3.1f} {thermostat.scale} - {new_setpoint_cool:3.1f} {thermostat.scale}')
            if thermostat.scale == 'F':
                new_setpoint_heat = Thermostat.fToC(new_setpoint_heat)
                new_setpoint_cool = Thermostat.fToC(new_setpoint_cool)
            command = 'SetRange'
            params = { 'heatCelsius': new_setpoint_heat , 'coolCelsius' : new_setpoint_cool }
        elif thermostat.mode == 'HEAT':
            command = 'SetHeat'
            point = 'heatCelsius'
            current_setpoint = thermostat.setpoint_heat
        elif thermostat.mode == 'COOL':
            command = 'SetCool'
            point = 'coolCelsius'
            current_setpoint = thermostat.setpoint_cool
        elif thermostat.mode == 'OFF':
            return
        else:
            print(thermostat.mode,'not supported yet for change_setpoint()',flush=True)
            return

        if params == None:
            new_setpoint = change + current_setpoint
            print(f'changing from {current_setpoint:3.1f} {thermostat.scale} to {new_setpoint:3.1f} {thermostat.scale}',flush=True)
            if thermostat.scale == 'F':
                new_setpoint = Thermostat.fToC(new_setpoint)
            params = { point : new_setpoint }

        url_exec_command = 'https://smartdevicemanagement.googleapis.com/v1/' + thermostat.device_id + ':executeCommand'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': self.access_token,
        }
        
        data = {'command': 'sdm.devices.commands.ThermostatTemperatureSetpoint.' + command,
                'params': params }
        #print(data)
        response = requests.post(url_exec_command, headers=headers, data=json.dumps(data))
        if response.status_code != 200:
            print(response,response.status_code,response.reason,flush=True)
            return False
        return True

    def change_mode(self, new_mode, thermostat):
        if new_mode == 'ECO':
            command = 'ThermostatEco.SetMode'
            params = { 'mode' : 'MANUAL_ECO' }
        elif new_mode == 'FAN':
            command = 'Fan.SetTimer'
            # fan is a toggle - if it was on, turn it off, it if was off, turn it on
            if thermostat.fan_on:
                params = { 'timerMode' : 'OFF' }
            else:
                params = { 'timerMode' : 'ON' }
        else:
            command = 'ThermostatMode.SetMode'
            params = { 'mode' : new_mode }
        
        url_exec_command = 'https://smartdevicemanagement.googleapis.com/v1/' + thermostat.device_id + ':executeCommand'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': self.access_token,
        }
        
        data = {'command': 'sdm.devices.commands.' + command,
                'params': params }
        #print(data)
        response = requests.post(url_exec_command, headers=headers, data=json.dumps(data))
        if response.status_code != 200:
            print(response,response.status_code,response.reason,flush=True)
            return False
        return True
        

if __name__ == "__main__":
    workingDirectory = os.getcwd()
    print(workingDirectory)

    api = GoogleApi(workingDirectory)
    if api.is_permissioned() == False:
        if api.get_permission() == False:
            print('could not get permision')

    thermostats = api.fetch_thermostats()
    t = thermostats[0]
    print(t)
    print('temp down')
    api.change_setpoint(-1,t, True)
    time.sleep(5)
    t = api.fetch_thermostat(t)
    print(t)
    print('temp up')
    api.change_setpoint(1,t, False)
    time.sleep(5)
    print(t)

    last = ''
    while True:
        for d in thermostats:
            t = api.fetch_thermostat(d)
            text = f'{t}'
            if last != text:
              print(text)
            last = text


        time.sleep(30)
