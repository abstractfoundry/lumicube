from LumicubeInterface import LumicubeInterface


def main():
    #Create instance of the Interface (make sure to change the IP-Adress
    #Parameters are optional default are:
    #api_version = v1
    #url = 127.0.0.1 (localhost)
    lc_interface = LumicubeInterface(api_version='v1', url='192.168.178.10')

    #exeptional cases:
    #set_leds() and set_3d() refer the github documentation for further information
    lc_interface.modules.display.set_led(1, 1, 0xFF000)


if __name__ == '__main__':
    main()
