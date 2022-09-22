# Raspberry Pi OS Lite install

If you would rather use the Raspberry Pi OS Lite image for your lumicube you need to do a few extra steps.

### Download the image

Only use the official repo: https://www.raspberrypi.com/software/operating-systems/

You want the 32-bit image called "Raspberry Pi OS Lite" as the java daemon is not built for x86_64.

Get this flashed onto your SD card using your favorite tool. If you would rather use the official Raspberry Pi Imager tool (https://www.raspberrypi.com/software/) do pay close attention when choosing the OS.

### Extra install steps

Once the image is on the SD card and you have fired up your raspberry with keyboard, mouse and monitor, added your user and password - the following needs to be done:

1. Get the WiFi working

> sudo raspi-config

This will open a menu. Go into System Options. Select Wireless LAN and follow the instructions.

2. Update and install needed packages

> sudo apt-get update && sudo apt-get upgrade -y && sudo apt install pulseaudio pulseaudio-utils python3-psutil 

3. Install the lumicube resources according to https://www.abstractfoundry.com/lumicube/resources/

> python3 <(curl -fL https://www.abstractfoundry.com/lumicube/download/install.py)

4. Make sure the daemon starts after reboot with your raspberry user

> sudo loginctl enable-linger <your user name>

5. Reboot

### Do not forget

Using the lumicube will be done via the http interface, however if yt a later point you want to ssh into your raspi to update or add something you will need to enable this (as it is disabled by default).

> sudo systemctl enable ssh && sudo systemctl start ssh


