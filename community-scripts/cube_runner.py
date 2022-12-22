# Script Runner
# Simple script runner for lumicube
# Author: Kevin Haney
# Date: 12/9/2022
# 
# Scripts are assumed to be in /home/pi/AbstractFoundry/Daemon/Scripts.  Change the path if necessary.
# Note that if you want to use any of the example scripts, you'll need to save them to a file (they're not on disk, but in the web code).
# the sample script below us using two cubes - "cubes" array can have just one (or more) as necessary.   cube value should be the dns name
# or ip address of the lumicube pi host.
# delay is in seconds
# to run, place the script on the pi and run it (e.g. python cube_runner.py).  
# You may want to comment out the print statements, they are useful for debugging though.
import requests
import json
import time

config = {
    'groups' : [
            {
                'name' : '1',
                'delay' : 60,
                'cubes' : 
                [
                    { 'cube' : 'lumipi.lan', 'filename' : 'vesuvius.py' },
                    { 'cube' : 'lumipi2.lan', 'filename' : 'cylon.py' }
                ]
            },
            {
                'name' : '2',
                'delay' : 300,
                'cubes' : 
                [
                    { 'cube' : 'lumipi.lan', 'filename' : 'nest_thermostat.py' },
                    { 'cube' : 'lumipi2.lan', 'filename' : 'yagol.py' }
                ]
            },
            {
                'name' : '3',
                'delay' : 300,
                'cubes' : 
                [
                    { 'cube' : 'lumipi2.lan', 'filename' : 'Lava lamp 2.py' }
                ]
            },
            {
                'name' : '4',
                'delay' : 300,
                'cubes' : 
                [
                    { 'cube' : 'lumipi.lan', 'filename' : 'ripples.py' },
                    { 'cube' : 'lumipi2.lan', 'filename' : 'Lava lamp 2.py' }
                ]
            },
            {
                'name' : '5',
                'delay' : 300,
                'cubes' : 
                [
                    { 'cube' : 'lumipi.lan', 'filename' : 'nest_thermostat.py' },
                    { 'cube' : 'lumipi2.lan', 'filename' : 'digital-rain-v2.py' }
                ]
            }
    ]
}

if __name__ == "__main__":
    workingDirectory = '/home/pi/AbstractFoundry/Daemon/Scripts/'
    print(workingDirectory)

    cube = "lumipi.lan"
    script = 'display.set_all(black)'

    # save config to file
    #with open(workingDirectory + 'config','w') as config_file:
    #    config_file.write(json.dumps(config, indent=4))

    while True:
        for group in config['groups']:
            name = group['name']
            delay = group['delay']
            print(f'Group {name}, delay {delay}')
            for cube in group['cubes']:
                cubename = cube['cube']
                filename = cube['filename']
                with open(workingDirectory + filename, 'r') as file:
                    script = file.read()

                url = "http://" + cubename + "/api/v1/scripts/main/methods/stop"
                response = requests.post(url)
                print(f'sending stop to {cubename}')
                if response.status_code != 200:
                    print(f'Unexpected response {response.status_code}')
                    print(response)
                
                headers = {
                    'Content-Type': 'application/json'
                }
                data = {
                    'body' : script 
                }
                print(f'sending start of script {filename} to {cubename}')
                url = "http://" + cubename + "/api/v1/scripts/main/methods/start"
                response = requests.post(url, headers=headers, data=json.dumps(data))
                if response.status_code != 200:
                    print(f'Unexpected response {response.status_code}')
                    print(response)
            time.sleep(delay)