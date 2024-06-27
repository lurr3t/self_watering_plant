import ubinascii
import machine

# Lights
RGB_LIGHT_RED_PIN = 13
RGB_LIGHT_GREEN_PIN = 14
RGB_LIGHT_BLUE_PIN = 15

# Pump
PUMP_DELAY_S = 1200 # 20 minutes
RELAY_PIN = 18
PUMP_BUTTON = 12

# Soil sensor
SOIL_MOISTURE_THRESHOLD = 26
READ_SOIL_INTERVAL_S = 3
SOIL_SDA_PIN = 20
SOIL_SCL_PIN = 21

# DHT sensor
READ_DHT_INTERVAL_S = 3
DHT_PIN = 27

# Adafruit number to mode
RESET_WATER_LEVEL = 1
RUN_PUMP_WHEN_PRESSED = 2
BENCHMARK = 3

# Adafruit IO
AIO_SERVER = "io.adafruit.com"
AIO_PORT = 1883
AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())
#feeds
AIO_INNER_HUM = "lurr3t/feeds/inner-humidity"
AIO_INNER_TEMP = "lurr3t/feeds/inner-temp"
AIO_LOGS = "lurr3t/feeds/logs"
AIO_ML_PUMPED = "lurr3t/feeds/ml-pumped"
AIO_SET_MODE = "lurr3t/feeds/set-mode"
AIO_SOIL_MOISTURE = "lurr3t/feeds/soil-moisture"
AIO_SOIL_TEMP = "lurr3t/feeds/soil-temp"
AIO_WATER_LEVEL = "lurr3t/feeds/water-level"

#publish interval
PUBLISH_INTERVAL_S = 120


