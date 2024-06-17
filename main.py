import sys
import dht
import machine
from sensor import Sensor
from machine import Pin
import time
import utime
import config
import json

# Restore water level
WATER_LEVEL_RESET = False # Set to True to reset water level, or set from dashboard
WATER_LEVEL = 100 #100% is full, 0% is empty. Container is 1L at max
WATER_CONTAINER_SIZE = 1000 # 1L


# ml/ms benchmark
BENCHMARK = False # Set to True to run benchmark, or set from dashboard
BENCHMARK_ML = 800
BENCHMARK_START_TIME: int = None
BENCHMARK_STARTED = False

# initial config
Sensor.turn_off_led()
LAST_PUMP_END_TIME = 0
RUN_PUMP_WHEN_PRESSED = False
sensor = Sensor()
sensor.kill_pump()

moisture: int = 0
temperature: int = 0

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
            data = {'pump_rate': pump_rate}
            with open('/data.json', 'w') as f:
                json.dump(data, f)
            sensor.load_pump_rate()



def pump_controller():
    global RUN_PUMP_WHEN_PRESSED
    global LAST_PUMP_END_TIME
    global moisture
    
    # If button is pressed, run pump
    if sensor.pump_button() == 0:
        print("Button is pressed")
        benchmark("start")
        sensor.run_pump_on_press(sensor.pump_button())
        RUN_PUMP_WHEN_PRESSED = True
        
    # Kill pump if button is released
    elif (RUN_PUMP_WHEN_PRESSED == True) and (sensor.pump_button() == 1):
        print("Button is released")
        benchmark("stop")
        sensor.kill_pump()
        RUN_PUMP_WHEN_PRESSED = False
        LAST_PUMP_END_TIME = time.time()
        
    # If pump has not been run for a while and moisture is under threshold, run pump
    elif LAST_PUMP_END_TIME is 0 or time.time() - LAST_PUMP_END_TIME > config.PUMP_DELAY_S: 
        # Runs pump if moisture is under threshold
        if moisture < config.SOIL_MOISTURE_THRESHOLD:
            #print("Moisture is under threshold")
            sensor.run_pump_ml(100)
            if sensor.pump_stopped == True:
                LAST_PUMP_END_TIME = time.time()
        else:
            #print("Moisture is above threshold")
            sensor.kill_pump()
            
def read_soil_sensor():
    global moisture
    global temperature
    moisture_temp, temperature_temp = sensor.read_soil()
    if moisture_temp != 0 and temperature_temp != 0:
        moisture = moisture_temp
        temperature = temperature_temp
        print("Temperature in soil is {} degrees and moisture is {}".format(temperature, moisture))


def read_dht_sensor():
    global temperature
    global humidity
    humidity, temperature = sensor.read_inner_humidity_temp()
    if humidity != 0 and temperature != 0:
        print("Inner temperature is {} degrees and humidity is {}%".format(temperature, humidity))



# main loop
while True:

    try:
        read_soil_sensor()
        read_dht_sensor()
        pump_controller()

    except Exception as error:
        print("Exception occurred", error)
        sensor.kill_pump()
        Sensor.error_light()
        break
    time.sleep(.1)