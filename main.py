import sys
import dht
import machine
from sensor import Sensor
from machine import Pin
from connection import Connection
import time
import utime
import config
import json

# Set last publish time to None
last_publish_time: int = None

# Restore water level
WATER_LEVEL_RESET = False # Set to True to reset water level, or set from dashboard
WATER_CONTAINER_SIZE = 1000 # 1L

# ml/ms benchmark
BENCHMARK = False # Set to True to run benchmark, or set from dashboard
BENCHMARK_ML = 800
BENCHMARK_START_TIME: int = None
BENCHMARK_STARTED = False

# initial config
Sensor.turn_off_led()
PUMP_START_TIME: int = None
LAST_PUMP_END_TIME = 0
RUN_PUMP_WHEN_PRESSED = False #do not set. Is changed when pump is run
sensor = Sensor()
sensor.kill_pump()

soil_moisture: int = 0
soil_temperature: int = 0
inner_temperature: int = 0
inner_humidity: int = 0

#TODO make a temporary variable for flowrate when benchmarking, this is done to avoid changing the flowrate when pumping
# Pump benchmark
def benchmark(action: str):
    global BENCHMARK
    global BENCHMARK_START_TIME
    global BENCHMARK_STARTED

    if BENCHMARK == True:
        if action == "start" and BENCHMARK_STARTED == False:
            print("Start benchmark")
            sensor.toggle_benchmark_light()
            BENCHMARK_START_TIME = utime.ticks_ms()
            BENCHMARK_STARTED = True
        elif action == "stop" and BENCHMARK_START_TIME is not None:
            sensor.toggle_benchmark_light()
            time_taken = utime.ticks_ms() - BENCHMARK_START_TIME
            pump_rate = BENCHMARK_ML / time_taken
            print("Benchmark: ", pump_rate, "ml/ms", pump_rate * 1000, "ml/s \t Time taken: ", time_taken, "ms")
            BENCHMARK_START_TIME = None
            BENCHMARK_STARTED = False
            # store in data file
            Sensor.save_data("pump_rate", pump_rate)
            # reload pump rate
            sensor.load_pump_rate()


# Reset water level. Returns True if water level was reset and False if not
def reset_water_level():
    global WATER_LEVEL_RESET
    if WATER_LEVEL_RESET == True:
        Sensor.save_data("water_level", 100)
        print("Water level reset")
        sensor.reset_water_level_light()
        return True
    return False


def pump_controller():
    global RUN_PUMP_WHEN_PRESSED
    global LAST_PUMP_END_TIME
    global PUMP_START_TIME
    global WATER_CONTAINER_SIZE
    global soil_moisture
    
    # If button is pressed, run pump
    if sensor.pump_button() == 0:
        print("Button is pressed")
        benchmark("start")
        # If water level is not reset and run pump when pressed is enabled
        if not reset_water_level():
            if not BENCHMARK:
                sensor.toggle_pump_light("on")

            # used for calculating the water level
            if PUMP_START_TIME is None:
                PUMP_START_TIME = utime.ticks_ms()
            sensor.run_pump_on_press(sensor.pump_button())
            RUN_PUMP_WHEN_PRESSED = True
        
    # Kill pump if button is released
    elif (RUN_PUMP_WHEN_PRESSED == True) and (sensor.pump_button() == 1):
        print("Button is released")
        benchmark("stop")
        if not BENCHMARK:
            sensor.toggle_pump_light("off")
        sensor.kill_pump()
        RUN_PUMP_WHEN_PRESSED = False
        # calculate time pump was running
        if PUMP_START_TIME is not None:
            pump_run_time = utime.ticks_ms() - PUMP_START_TIME
            print("Pump ran for: ", pump_run_time, "ms")
            # calculate water level
            water_level = Sensor.retrieve_data("water_level")
            # calculate water_level
        
            water_dispensed = Sensor.retrieve_data("pump_rate") * pump_run_time / 10
            water_level -= water_dispensed
            print("Water dispensed %: ", water_dispensed)
            Sensor.save_data("water_level", water_level)
            print("Water level is: ", water_level)
            PUMP_START_TIME = None

        LAST_PUMP_END_TIME = time.time()
        
    # If pump has not been run for a while and moisture is under threshold, run pump
    elif LAST_PUMP_END_TIME is 0 or time.time() - LAST_PUMP_END_TIME > config.PUMP_DELAY_S: 
        # Runs pump if moisture is under threshold
        if soil_moisture < config.SOIL_MOISTURE_THRESHOLD:
            #print("Moisture is under threshold")
            ml_to_water = 100
            sensor.run_pump_ml(ml_to_water)

            if sensor.pump_stopped == True:
                LAST_PUMP_END_TIME = time.time()
                water_level = Sensor.retrieve_data("water_level")
                water_level -= 10
                Sensor.save_data("water_level", water_level)
                print("Water level is: ", water_level)


        else:
            #print("Moisture is above threshold")
            sensor.kill_pump()
            
def read_soil_sensor():
    global soil_moisture
    global soil_temperature
    moisture_temp, temperature_temp = sensor.read_soil()
    if moisture_temp != 0 and temperature_temp != 0:
        soil_moisture = moisture_temp
        soil_temperature = temperature_temp
        print("Temperature in soil is {} degrees and moisture is {}".format(soil_temperature, soil_moisture))


def read_dht_sensor():
    global inner_temperature
    global inner_humidity
    humidity_temp, temperature_temp = sensor.read_inner_humidity_temp()
    if humidity_temp != 0 and temperature_temp != 0:
        inner_temperature = temperature_temp
        inner_humidity = humidity_temp
        print("Inner temperature is {} degrees and humidity is {}%".format(inner_temperature, inner_humidity))


def set_mode():
    global WATER_LEVEL_RESET
    global BENCHMARK
    global RUN_PUMP_WHEN_PRESSED

    # Get mode from json
    mode = Sensor.retrieve_data("mode")
    #print("Mode is: ", mode)
    if mode is not None:
        if mode == config.RESET_WATER_LEVEL:
            WATER_LEVEL_RESET = True
            RUN_PUMP_WHEN_PRESSED = False
            BENCHMARK = False
        elif mode == config.RUN_PUMP_WHEN_PRESSED:
            #RUN_PUMP_WHEN_PRESSED = True
            WATER_LEVEL_RESET = False
            BENCHMARK = False
        elif mode == config.BENCHMARK:
            BENCHMARK = True
            #RUN_PUMP_WHEN_PRESSED = True
            WATER_LEVEL_RESET = False
        else:
            print("Mode not recognized")
    else:
        print("Mode is None")

def publish():
    global last_publish_time
    global connection
    global soil_moisture
    global soil_temperature
    global inner_temperature
    global inner_humidity

    # publish data to Adafruit IO at interval
    if last_publish_time is None or time.time() - last_publish_time > config.PUBLISH_INTERVAL_S:
        last_publish_time = time.time()
        connection.publish(config.AIO_SOIL_MOISTURE, str(soil_moisture))
        connection.publish(config.AIO_INNER_HUM, str(inner_humidity))
        connection.publish(config.AIO_WATER_LEVEL, str(Sensor.retrieve_data("water_level")))




# main loop
try:
    water_level_low_log_switch = False

    # Connect to Adafruit IO
    connection = Connection()
    connection.subscribe(config.AIO_SET_MODE)

    while True:
 
        set_mode()
        connection.check_msg()
        read_soil_sensor()
        read_dht_sensor()
        # only run pump if water level is above 10%
        if Sensor.retrieve_data("water_level") > 10 or WATER_LEVEL_RESET == True:
            pump_controller()
        else:
            print("Water level is low")
            if (not water_level_low_log_switch):
                connection.publish(config.AIO_LOGS, "Water level is to low")
                water_level_low_log_switch = True

        publish()
        time.sleep(.1)

except Exception as error:
    print("Exception occurred", error)
    sensor.kill_pump()
    # publish error to Adafruit IO
    connection.publish(config.AIO_LOGS, str(error))
    Sensor.error_light()
    