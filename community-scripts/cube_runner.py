# Script Runner
# Simple script runner for lumicube
# Author: Kevin Haney
# Date: 12/9/2022
# 
# Scripts are assumed to be in /home/pi/AbstractFoundry/Daemon/Scripts.  Change the path if necessary.
# Note that if you want to use any of the example scripts, you'll need to save them to a file (they're not on disk, but in the web code).
# the sample script below us using two cubes - "cubes" array can have just one (or more) as necessary.   cube value should be the dns name
# or ip address of the lumicube pi host.
# in cubes, a cube can specify a filename, or random : True to pick from a list of random file.
# delay is in seconds
# to run, place the script on the pi and run it (e.g. python cube_runner.py).  
# You may want to comment out the print statements, they are useful for debugging though.
import requests
import json
import time
import random
import traceback

config = {
    'random' : [
        'vesuvius.py',
        'cylon.py',
        'yagol.py',
        'ripples.py',
        'Lava lamp 2.py',
        'digital-rain-v2.py',
        'pong.py'
    ],
    'groups' : [
            {
                'name' : '1',
                'delay' : 300,
                'cubes' : 
                [
                    { 'cube' : 'lumipi.lan', 'random' : True },
                    { 'cube' : 'lumipi2.lan', 'random' : True }
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
                    { 'cube' : 'lumipi2.lan', 'random' : True }
                ]
            },
            {
                'name' : '4',
                'delay' : 300,
                'cubes' : 
                [
                    { 'cube' : 'lumipi.lan', 'random' : True },
                    { 'cube' : 'lumipi2.lan', 'random' : True }
                ]
            },
            {
                'name' : '5',
                'delay' : 300,
                'cubes' : 
                [
                    { 'cube' : 'lumipi.lan', 'filename' : 'nest_thermostat.py' },
                    { 'cube' : 'lumipi2.lan', 'random' : True }
                ]
            }
    ]
}

if __name__ == "__main__":
    workingDirectory = '/home/pi/AbstractFoundry/Daemon/Scripts/'
    print(workingDirectory)

    # save config to file
    #with open(workingDirectory + 'config','w') as config_file:
    #    config_file.write(json.dumps(config, indent=4))

    while True:
        random_files = config['random']
        for group in config['groups']:
            name = group['name']
            delay = group['delay']
            print(f'Group {name}, delay {delay}')
            for cube in group['cubes']:
                cubename = cube['cube']
                if 'random' in cube:
                    filename = random_files[random.randrange(len(random_files))]
                else:
                    filename = cube['filename']
                with open(workingDirectory + filename, 'r') as file:
                    script = file.read()

                try:
                    url = "http://" + cubename + "/api/v1/scripts/main/methods/stop"
                    response = requests.post(url, timeout=30)
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
                    response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
                    if response.status_code != 200:
                        print(f'Unexpected response {response.status_code}')
                        print(response)
                except OSError as ose:
                    print(f'OSError exception talking to {cubename}')
                    print(getattr(ose, 'message', str(ose)))
                except Exception as e:
                    print(f'Unexpected exception talking to {cubename}')
                    print(traceback.format_exc())
            time.sleep(delay)