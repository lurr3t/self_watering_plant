import machine
import config
import dht
from machine import Pin
import time
import utime
from seesaw import Seesaw as seesaw
from stemma_soil_sensor import StemmaSoilSensor
import json


class Sensor:


    def __init__(self):
        #benchmark toggle light
        self.benchmark_light = False


        # pump
        self.relay = Pin(config.RELAY_PIN, Pin.OUT)
        self.pump_start_time = None
        self.pump_stopped = False
        # ml/ms
        self.load_pump_rate()

        # soil sensor
        self.soil_last_read_time = None

        # dht sensor
        self.dht_last_read_time = None


    # Methods for saving and loading to and from the data json file
    @staticmethod
    def save_data(key: str, value):
        # Load existing data
        with open('/data.json', 'r') as f:
            data = json.load(f)
        # Modify the key value pair
        data[key] = value
        # Write the data back to the file
        with open('/data.json', 'w') as f:
            json.dump(data, f)

    @staticmethod
    def retrieve_data(key: str):
        try:
            with open('/data.json', 'r') as f:
                data = json.load(f)
                return data[key]
        except Exception as error:
            raise Exception("Error retrieving data from json: %s" % error)


    def load_pump_rate(self):
        with open('/data.json', 'r') as f:
            data_loaded = json.load(f)
            self.pump_rate = data_loaded['pump_rate']






    # Lights methods

    @staticmethod
    def turn_off_led():
        Pin(config.RGB_LIGHT_RED_PIN, Pin.OUT).value(0)
        Pin(config.RGB_LIGHT_GREEN_PIN, Pin.OUT).value(0)
        Pin(config.RGB_LIGHT_BLUE_PIN, Pin.OUT).value(0)

    # stays in infinite loop
    @staticmethod
    def error_light():
        print("error light")
        LED_Pin_Red = Pin(config.RGB_LIGHT_RED_PIN, Pin.OUT)
        while True:
            LED_Pin_Red.value(1)
            time.sleep(1)
            LED_Pin_Red.value(0)
            time.sleep(1)

    # stays in infinite loop
    @staticmethod
    def wifi_error_light():
        print("wifi error light")
        while True:
            LED_Pin_Red = Pin(config.RGB_LIGHT_RED_PIN, Pin.OUT)
            LED_Pin_Red.value(1)
            machine.idle()

    # Toggles blue light for benchmark
    def toggle_benchmark_light(self):
        if self.benchmark_light:
            Pin(config.RGB_LIGHT_BLUE_PIN, Pin.OUT).value(0)
            self.benchmark_light = False
        else:
            Pin(config.RGB_LIGHT_BLUE_PIN, Pin.OUT).value(1)
            self.benchmark_light = True

    # Toggles light for pump
    def toggle_pump_light(self, mode: str):
        if mode == "off":
            Pin(config.RGB_LIGHT_BLUE_PIN, Pin.OUT).value(0)
            Pin(config.RGB_LIGHT_RED_PIN, Pin.OUT).value(0)
        elif mode == "on":
            Pin(config.RGB_LIGHT_BLUE_PIN, Pin.OUT).value(1)
            Pin(config.RGB_LIGHT_RED_PIN, Pin.OUT).value(1)

    def reset_water_level_light(self):
        Pin(config.RGB_LIGHT_GREEN_PIN, Pin.OUT).value(1)
        time.sleep(0.5)
        Pin(config.RGB_LIGHT_GREEN_PIN, Pin.OUT).value(0)




    # blink orange light with delay of 500ms. Introduces total delay of 1 sec
    @staticmethod
    def connecting_wifi_light():
        LED_Pin_Red = Pin(config.RGB_LIGHT_RED_PIN, Pin.OUT)
        LED_Pin_Green = Pin(config.RGB_LIGHT_GREEN_PIN, Pin.OUT)
        Pin(config.RGB_LIGHT_BLUE_PIN, Pin.OUT).value(0)
        LED_Pin_Red.value(1)
        LED_Pin_Green.value(1)
        time.sleep(0.5)
        Sensor.turn_off_led()
        time.sleep(0.5)

    # loops through 15 blinks
    @staticmethod
    def connected_wifi_light():
        print("connected wifi light")

        LED_Pin_Green = Pin(config.RGB_LIGHT_GREEN_PIN, Pin.OUT)

        for i in range(5):
            LED_Pin_Green.value(1)
            time.sleep(0.2)
            LED_Pin_Green.value(0)
            time.sleep(0.2)
        Sensor.turn_off_led()
        
        

    # other sensors

    def run_pump_ml(self, ml: int):
        try:
            self.pump_stopped = False
            if self.pump_start_time is None:
                # Turn on the pump
                self.relay.value(1)
                # Record the start time in milliseconds
                self.pump_start_time = utime.ticks_ms()
                print(f"start time is {self.pump_start_time}")
                # Calculate the run time in milliseconds. How long it should run
                self.run_time = ml / self.pump_rate  # no need to convert to s
                print(f"Starting pump: run time is {self.run_time} ms")
                    
            # If the pump is running and the run time has passed
            elif utime.ticks_ms() - self.pump_start_time >= self.run_time:
                # Turn off the pump
                self.relay.value(0)
                # Reset the start time
                self.pump_start_time = None
                self.pump_stopped = True
        except Exception as e:
            self.relay.value(0)
            self.pump_start_time = None
            self.pump_stopped = True
            raise Exception("Error running pump")
      

    def run_pump_on_press(self, button: int):
        if button == 0:
            self.relay.value(1)
        
    def kill_pump(self):
        print("Killing pump")
        self.relay.value(0)
        self.pump_start_time = None
        self.pump_stopped = True

    # is 0 if pressed
    def pump_button(self):
        return Pin(config.PUMP_BUTTON, Pin.IN, Pin.PULL_UP).value()
    
    

    # Both moisture and temperature are returned. Both are 0 if no measurements are taken
    def read_soil(self):
        moisture = 0
        temperature = 0

        if (self.soil_last_read_time is not None) and time.time() - self.soil_last_read_time < config.READ_SOIL_INTERVAL_S:
            return moisture, temperature

        #print("Reading temperature and moisture from soil sensor")
        i2c = machine.I2C(0, sda=machine.Pin(config.SOIL_SDA_PIN), scl=machine.Pin(config.SOIL_SCL_PIN), freq=400000)
        seesaw = StemmaSoilSensor(i2c)
        # get moisture
        moisture = seesaw.get_moisture()
        # get temperature
        temperature = seesaw.get_temp()
        self.soil_last_read_time = time.time()
        return moisture, temperature
    

    def read_inner_humidity_temp(self):
        humidity = 0
        temperature = 0
        try:

            if (self.dht_last_read_time is not None) and time.time() - self.dht_last_read_time < config.READ_DHT_INTERVAL_S:
                return humidity, temperature

            tempSensor = dht.DHT11(Pin(config.DHT_PIN)) 
            tempSensor.measure()
            temperature = tempSensor.temperature()
            humidity = tempSensor.humidity()
            self.dht_last_read_time = time.time()
            return humidity, temperature
        except Exception as e: # temporary fix. It gets a checksum error when pump is running. Interferance?
            print(e)
            return humidity, temperature
