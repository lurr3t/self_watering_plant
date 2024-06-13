import network
from time import sleep
import machine
from machine import Pin
from sensor import Sensor
import keys



# Function to connect Pico to the WiFi
def do_connect():
  
    wlan = network.WLAN(network.STA_IF)         # Put modem on Station mode

    if not wlan.isconnected():                  # Check if already connected
        print('connecting to network...')
        wlan.active(True)                       # Activate network interface
        # set power mode to get WiFi power-saving off (if needed)
        wlan.config(pm = 0xa11140)
        wlan.connect(keys.WIFI_SSID, keys.WIFI_PASS)  # Your WiFi Credential
        print('Waiting for connection...', end='')
        # Check if it is connected otherwise wait
        while not wlan.isconnected() and wlan.status() >= 0:
            print('.', end='')
            # introduce delay of 1 sec
            Sensor.connecting_wifi_light()
    # Print the IP assigned by router
    ip = wlan.ifconfig()[0]
    print('\nConnected on {}'.format(ip))
    Sensor.connected_wifi_light()
    return ip




# Try WiFi Connection
try: 
    do_connect()
    
except Exception as e:
    print(f"WiFi Connection Failed {e}")
    Sensor.wifi_error_light()
    


