import network
from time import sleep
import machine
from machine import Pin
from sensor import Sensor
import keys
import config
from mqtt import MQTTClient


class Connection: 


    # constructor
    def __init__(self):
        try:
            # Use the MQTT protocol to connect to Adafruit IO
            self.client = MQTTClient(config.AIO_CLIENT_ID, config.AIO_SERVER, config.AIO_PORT, keys.ADAFRUIT_AIO_USERNAME, keys.ADAFRUIT_AIO_KEY)

            # Subscribed messages will be delivered to this callback
            self.client.set_callback(self.__sub_cb)
            self.client.connect()

            #self.client.subscribe(AIO_LIGHTS_FEED)
            #print("Connected to %s, subscribed to %s topic" % (AIO_SERVER, AIO_LIGHTS_FEED))
        except Exception as e:
            raise Exception("Error connecting to Adafruit IO: %s" % e)


    
    # Callback Function to respond to messages from Adafruit IO
    
    def __sub_cb(self, topic, msg):          # sub_cb means "callback subroutine"
        print((topic, msg))          # Outputs the message that was received. Debugging use.
        Sensor.save_data("mode", int(msg))          # sets the mode
        # convert msg to int

    def subscribe(self, topic):
        self.client.subscribe(topic)
        print("Subscribed to %s topic" % topic)

    def check_msg(self):
        return self.client.check_msg()
    
    
    def publish(self, topic, msg: str):
        self.client.publish(topic, msg)




    # Function to connect Pico to the WiFi
    @staticmethod
    def connect_wifi():
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

