# Self watering IOT system
Made by: *Ludwig Fallström - lf222yi*

Water is usually essential for a plant's survival, which is a bad thing if it happens to be cared for by me. Remembering to water plants is not the top of my priorities and therefore this project helps with my plant's survival with the creation of a self-watering iot system. The device measures the moisture in a plant's soil and activates a pump if it goes below a certain threshold, automatically watering it. Along with the soil moisture percentage, the soil temperature, inner temperature, and inner humidity are also measured. The data is uploaded to Adafruit IO and displayed on a dashboard.

The time needed to implement this project greatly depends on previous experience, the sort of container to house the system in, and if custom solutions are to be implemented. With all hardware bought, and research complete, having the system up and running including hardware assembly and upload of given code, the project should take around 5 - 15 hours.

---

As stated in the beginning, the project is mainly chosen to have more healthy plants if watering them happens to be forgotten. However, it is not the only benefit. Having the plants water themselves when on vacation is also advantageous, along with having parameters to play with such as the soil moisture threshold to water the plants when it is most favourable.

Implementing this project you will learn about integrating software with hardware, setting up sensors and communicating with them from a microcontroller. You will also learn about electronics and circuitry, especially when connecting the pump, which is controlled by a relay and takes power from an external power supply. Insights into your plant's watering needs are also gained and how it potentially can benefit from it. Lastly, how uploading data using the MQ Telemetry Transport (MQTT) protocol is also taught, and how the data can be displayed using the Adafruit IO platform.

## Functionality
The self-watering device has a moisture sensor placed in the soil of a plant. The soil moisture and temperature are recorded. Inside the device, there is a humidity and temperature sensor that also takes measurements. It is used for making sure that the inside is not too hot or monitoring if there is any water spillage by seeing if humidity rises. Every 20 minutes the pump tries to activate and does so if the soil moisture is below 26%. It pumps 100ml and waits another 20 minutes before trying again. This lets the water flow evenly in the pot, making sure that it is not getting overwatered. Three modes are also available, controllable from the dashboard, and used by pressing the button on the device. Mode 1 resets the water level, mode 2 activates the pump manually, and mode 3 activates calibration mode. Calibration mode calculates the flow rate by measuring the time taken to pump 1L (the size of the water container) and uses it to pump the correct amount of water. The current water level is calculated using the pump's flow rate and the time the pump is active. If the water level goes below 10%, it is stopped to not damage the pump. 

The light on the device lights in different colours depending on what it currently does.


| Event | Light | 
| -------- | -------- |
| Connecting to wifi (slow blink)     | ![image](https://hackmd.io/_uploads/SysYB0AIA.png)| 
| Connected to wifi (fast blink) | ![image](https://hackmd.io/_uploads/SyeLSC0I0.png)|
| Unable to connect to wifi| ![image](https://hackmd.io/_uploads/rkj8IRAU0.png) |
| Mode 1: reset water level | ![image](https://hackmd.io/_uploads/rylkLAR8A.png)|
| Mode 2: pump manually | ![image](https://hackmd.io/_uploads/r1f3BARLC.png)|
|Mode 3: calibrate | ![image](https://hackmd.io/_uploads/SJC-8RCUC.png) |
| Error found (blink) | ![image](https://hackmd.io/_uploads/S1sHURCLR.png) |
| Operating as usual | ![image](https://hackmd.io/_uploads/HJLqLA0IC.png)|
| Measurements taken | ![image](https://hackmd.io/_uploads/SkLpUC0IA.png)|


# Hardware

The following hardware is necessary to replicate the device, however, the button, LED, and DHT11 sensor can be skipped if only automatic watering is desired. Hardware for the housing or tank can also be skipped or replaced with your solution. 


| Item | Cost (sek) | Image |
| -------- | -------- | -----|
| [Raspberry Pi Pico W](https://www.electrokit.com/raspberry-pi-pico-w) | 89| ![image](https://hackmd.io/_uploads/SJH_MJjUR.png)|
| [Adafruit STEMMA Soil Sensor - I2C Capacitive Moisture Sensor ](https://www.electrokit.com/jordfuktighetssensor-kapacitiv-i2c)    |   115   | ![image](https://hackmd.io/_uploads/BJCUoyj80.png)|
| [LED-module RGB](https://www.electrokit.com/led-modul-rgb)    | 22      | ![image](https://hackmd.io/_uploads/rkoAo1jU0.png) |
| [Button](https://www.electrokit.com/tryckknapp-momentan) | 19 |![image](https://hackmd.io/_uploads/Bk8fhyjUC.png)|
| [Luxorparts Relay](https://www.kjell.com/se/produkter/el-verktyg/elektronik/utvecklingskit/arduino/moduler/luxorparts-relamodul-for-arduino-1x-p87032) | 100 | ![image](https://hackmd.io/_uploads/BySS2ko8A.png)|
| [Digital temperature and moisture sensor DHT11](https://www.electrokit.com/digital-temperatur-och-fuktsensor-dht11) | 49| ![image](https://hackmd.io/_uploads/SkcOh1oU0.png) |
| [Submersible pump 3V DC](https://www.electrokit.com/drankbar-pump-3v) | 45| ![image](https://hackmd.io/_uploads/HyFRnkiUR.png) |
| [Coffe can](https://www.clasohlson.com/se/Kaffeburk-med-snapplock/p/44-2598-4)| 80| ![image](https://hackmd.io/_uploads/ByDzpyi8R.png)|
| [Bottle for fridge and freezer](https://www.clasohlson.com/se/Plastflaska-for-kyl-och-frys/p/44-1485-1) | 30| ![image](https://hackmd.io/_uploads/SyBBTks8A.png)|
| [PVC hose 6x1,5mm](https://www.bauhaus.se/pvc-slang-6x1-5mm?queryID=949173832e994f18aaa9c1811d20028b&objectID=425485&indexName=nordic_production_sv_products) | 20| ![image](https://hackmd.io/_uploads/rJTv6yiIA.png) |
| [Micro USB to USB-A cable](https://www.biltema.se/kontor---teknik/datortillbehor/datorkablar/usb-kablar/usb-micro/usb-kabel-med-micro-usb-kontakt-2000045459)| 30 |
| [USB A male to female x3](https://www.biltema.se/kontor---teknik/datortillbehor/datorkablar/usb-kablar/usb-typ-a/usb-20-a---a-1-8-m-2000060787) | 90|
| USB power supply x2| Na|
| | Total: 689 |



* **Raspberry Pi Pico W**
    * Raspberry Pi Pico is a microcontroller from the Raspberry Pi Foundation. It includes the RP2040 chip, containing a dual-core ARM processor, which provides a powerful and affordable platform for developing embedded systems and iot devices. 128kB ram is also available, along with 2MB of onboard flash storage. The Pico W variant, which this project uses, also includes a built-in wifi chip.
* **Adafruit STEMMA Soil Sensor - I2C Capacitive Moisture Sensor**
    * This is a digital sensor which measures the moisture level in the soil using Capacitive sensing. This is better than traditional resistive-style moisture sensors, where the conductivity of the soil is measured. Those are often lower price but are prone to degradation and therefore need recalibration, and do not offer the same accuracy. A thermometer is also built in, measuring the ambient temperature above the soil. 
* **LED-module RGB**
    * This RGB light emits a range of colours by mixing red, green, and blue. The amount of each colour is adjusted using PWM. Three 150Ω limiting resistors are built in to prevent burnout. The light is used in this project to indicate different modes, errors, and when the device is connected to wifi. 


* **Button**
    * This button outputs a high signal when pressed. It consists of a tactile push button and a pull-up resistor. It is used for resetting the water level, pumping manually, or calibrating the pump flow rate. 
* **Luxorparts Relay**
    * A relay is used for controlling the pump from an external power supply. The pump is rated for 3 - 5 volts, which could be taken directly from the Raspberry Pi's VBUS pin, however, the current needed might be too high for the Pico to safely deliver which necessitates the relay. The relay uses 5V to be controlled and is Max rated for 250 V AC/10 A, and 30 V DC/10 A.
* **Digital temperature and moisture sensor DHT11**
    * This module contains an internal thermistor and a capacitive humidity sensor. An internal chip converts the readings to a serial datastream which can be read by the Picos digital input pins. Its humidity range is between 20% to 90% RH, while its temperature range is 0ºC to 50ºC.


* **Submersible pump 3V DC**
    * This is a submersible pump, rated for 3V at the seller's website. Not much is known about the pump since limited information is provided by the seller. The pump is used with 5V in this project, which seems to work without issues. The flow rate, when measured, is around 28.6 ml/s with a 6mm diameter, and 1m long hose. 

* **External power supply**
    * Two USB phone chargers are used, outputting 5V each. One powers the pico and its sensors, and the other powers the pump. If the pump is replaced with a more powerful one, the power supply can also be changed to match the new pump's power requirements. 

# Computer setup
The IDE used is Visual Studio Code with the Pymakr extension. Thonny has also been tried, however, the IDE is lacking in functionality when compared with VS code. I believe the JetBrains IDEs, in this case Pycharm, are better than VS code, however getting it to work with the Pico was a challenge. The MicroPython plugin, available for all JetBrains IDEs was tried, uploading code to the Pico worked, however, no REPL was available, making debugging nearly impossible. All development was done on Mac OS, however, setting up the IDE for both Windows and Linux are similar. 

## Flashing the Raspberry Pi Pico
Before any development can begin, the Pico needs to be flashed with appropriate Firmware. Follow this guide for a thorough explanation: [Part 1: Update Firmware on Raspberry Pi Pico W and run a test code](https://hackmd.io/@lnu-iot/rkFw7gao_), In short:
1. Download the latest Pico W [MicroPyton Firmware](https://micropython.org/download/RPI_PICO_W/)
2. Press the Bootsel button on the Pico while connecting the usb to a computer.
3. Drag and drop the firmware file into the Picos folder.
4. Unplug and plug in the pico to restart it.
5. Done!


## IDE Setup
1. Download Visual Studio Code for your OS and install it - [Download Visual Studio Code](https://code.visualstudio.com/download)
2. Download and install Node.js for your operating system - [Download Node.js](https://nodejs.org/en/download/package-manager)
3. Download the Pymakr plugin for VS code and follow this [guide](https://github.com/sg-wireless/pymakr-vsc/blob/HEAD/GET_STARTED.md/) for setting it up. 
4. Navigate to the Pymakr tab located in the left vertical bar and press Create project.
5. A `main.py` file is created where the main code should go. A `.code-workspace` file is also created containing project specific configurations. Click on this file when opening the project in the future.
6. To upload the code to the pico, navigate to the Pymakr tab. In the tab the pico should be found, if not, see the previous guide. Click the upload cloud button named `sync project to device`. Or enable `development mode` which syncs the files automatically when saving. 
7. A bug that i found, when making changes to files in the lib folder, they are not uploaded automatically. In that case, unplug the pico, and upload again. Changes done in the main.py file should be uploaded automatically if development mode is activated.

## Libraries
Some external libraries are necessary for using the sensors. You can find them in the linked Github repository in the bottom of these instructions. Create a lib folder and place the libraries inside. 
* [MQTT](https://github.com/iot-lnu/pico-w/blob/main/network-examples/N2_WiFi_MQTT_Webhook_Adafruit/lib/mqtt.py) - For communicating with Adafruit IO
* [seesaw](https://github.com/mihai-dinculescu/micropython-adafruit-drivers/blob/master/seesaw/seesaw.py) - For getting readings from the soil sensor.
* [stemma soil sensor](https://github.com/mihai-dinculescu/micropython-adafruit-drivers/blob/master/seesaw/stemma_soil_sensor.py) - For getting readings from the soil sensor.

You can now start to code!


# Putting everything together
The wiring can be done both on a breadboard or soldered directly between the Pico and the sensors. Follow the circuit diagram below. Make sure that the relay gets 5V to control it. Here it is connected to the VSYS pin, taking power directly from the pico, but it can also be taken from the passthrough VBUS pin. Make sure that the pump is connected to the normally closed (NC) port on the relay. In the circuit diagram, the DHT11 sensor has four pins, this is also true for the real one, however, it is mounted on a board which has three pins. Make sure to connect the data to the leftmost, 3,3V in the middle, and ground to the rightmost. The wiring is mostly for a development setup, however it should also work for production. 

![project_diagram](https://hackmd.io/_uploads/S118UBoIR.png)

Circuit diagram made with the fritzing software.

![image](https://hackmd.io/_uploads/ryDX_XhLA.png)

All sensors and relay connected to the Pico using a breadboard.

![image](https://hackmd.io/_uploads/HJ5adXhUC.png)

All sensors and relay soldered directly to the Pico and mounted on the inner lid of the coffe can. 

![image](https://hackmd.io/_uploads/HyMjOQ2UR.png)

Female usb A's connected for powering the pico, connecting the soil moisture sensor, and for giving power to the pump. 



# Platform
The Adafruit IO platform was chosen since it provides an easy way to connect iot devices without much setup, is beginner friendly since not much code is needed, and presents the data in an easy-to-use dashboard, where different widgets can be added displaying the various data feeds. 

It is a cloud-based platform, meaning that no local server is needed. The free tier is used in this project, it offers a limited number of dashboards, data feeds, widgets, and data points per minute. It is sufficient in this case, however, if the system were to scale up, upgrading to the Plus plan could be wise since it offers unlimited dashboards and more data points per minute.


# The code
The code in this project is quite extensive, therefore only the core functionality and interesting solutions are explained. See the Github Repository at the bottom of this tutorial for the complete code.

The code consists of the following files:
* lib
    * `config.py` - Contains attributes for setting different values throughout the code.
    *  `connection.py` - Contains methods for setting up wifi connection and Adrafruit IO connection.
    *  `keys.py` - Contains SSID and Password for router and credentials for Adafruit IO, should be added to .gitignore.
    *  `mqtt.py` - Contains methods for communicating with Adafruit IO using the MQTT protocol.
    *  `seesaw.py` - Contains methods making it possible to get readings from the soil sensor.
    *  `sensor.py` - Contains methods for controlling all sensors and setting light colours. 
    *  `stemma_soil_sensor.py` - Contains methods making it possible to get readings from the soil sensor.
*  `boot.py` - Runs after booting, before `main.py`. Calls method in `connection.py` for setting up the wifi connection.
*  `main.py` - Contains the main loop.
*  `data.json` - For saving the pump rate, water level, and mode. Needed in case of restart so that the settings are not resetted. 


## Main logic

**The main logic of the device is the following:**

* Connect to wifi when booting.
* Connect to Adafruit IO and set callback function for subscribed messages.
* Enter main loop.
    * Read from the soil sensor and save to global variable.
    * Read from the DHT11 sensor and save to global variable.
    * Run the pump if soil moisture is below 26%, or if it should be dispensed manually.
    * Publish the data to Adafruit IO.
* If some exception occurred while connecting to Adafruit IO or in the main loop, enter infinite loop triggering error light and publish error log to the data feed. 

The following code is the main loop:

```python
try:
    water_level_low_log_switch = False

    # Connect to Adafruit IO
    connection = Connection()
    connection.subscribe(config.AIO_SET_MODE)

    # Main loop
    while True:
        
        set_mode()
        connection.check_msg()
        read_soil_sensor()
        read_dht_sensor()
        # only run pump if water level is above 10%
        if Sensor.retrieve_data("water_level") > 10 or WATER_LEVEL_RESET == True:
            pump_controller()
        else:
            if (not water_level_low_log_switch):
                connection.publish(config.AIO_LOGS, "Water level is too low")
                water_level_low_log_switch = True
     
        publish()
        time.sleep(.1)

except Exception as error:
    print("Exception occurred", error)
    sensor.kill_pump()
    # publish error to Adafruit IO
    connection.publish(config.AIO_LOGS, str(error))
    Sensor.error_light()

```


## Network connection

Function called from the `boot.py` file to connect to wifi. Borrowed from [Part 2: Using WiFi](https://hackmd.io/@lnu-iot/rJVQizwUh)

```python
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
```

## Adafruit IO connection and communication
Setting up the platform connection is done before entering the main loop. See [Part 3: Adafruit IO (MQTT & Webhooks)](https://hackmd.io/@lnu-iot/r1yEtcs55) for a complete guide of setting up connection and communicating with Adafruit IO.

This code is placed in the constructor of `connection.py`.
```python
            self.client = MQTTClient(config.AIO_CLIENT_ID, config.AIO_SERVER, config.AIO_PORT, keys.ADAFRUIT_AIO_USERNAME, keys.ADAFRUIT_AIO_KEY)

            self.client.set_callback(self.__sub_cb)
            self.client.connect()
```

When a mode is chosen from the dashboard, this callback function is run, saving the mode to the data.json file. The mode is later checked in the main loop for each iteration.

```python
   def __sub_cb(self, topic, msg):           
        Sensor.save_data("mode", int(msg))         
```

The following function is called from the main loop to publish data. The condition to publish is met when data has never been published before or the time taken since last publish, is greater than the set publish interval, in this case 2 minutes. 

```python
def publish():
    try: 
        # publish data to Adafruit IO at interval
        if last_publish_time is None or time.time() - last_publish_time > config.PUBLISH_INTERVAL_S:
            last_publish_time = time.time()
            connection.publish(config.AIO_SOIL_MOISTURE, str(soil_moisture))
            connection.publish(config.AIO_SOIL_TEMP, str(soil_temperature))
            connection.publish(config.AIO_INNER_HUM, str(inner_humidity))
            connection.publish(config.AIO_INNER_TEMP, str(inner_temperature))
            connection.publish(config.AIO_WATER_LEVEL, str(Sensor.retrieve_data("water_level")))
    except Exception as error:
        raise Exception("Error publishing data: %s" % error)
```

## Pump logic
This code is quite complicated and would need some refactoring, however it does contain the device's most important logic. See the `benchmark()` and `pump_controller` function in the `main.py` file in the repository. Note that the benchmark function has its own check if benchmarking the pump (calibrating it) is activated. When activating the pump and turning it off are mentioned, it is actually the relay.

It works as follows for each mode:

**1. Reset water level** - If button is pressed, call reset_water_level() function, and publish the new water level. 

**2. Pump manually** - If the button is pressed, start the pump light and note the pump start time. if the button is released, stop the pump and turn of the light. Calculate the total run time and obtain the new water level from the known flow rate, save it to the json and publish to Adafruit IO. 

**3. Calibrate pump** - Call the `benchmark()` function from `pump_controller()` when button is pressed and not in water level reset mode. Here the current time is saved. When the button is released, the time taken is divided with the water amount that has been pumped to obtain the flow rate. The new flowrate is saved in the json file. 

Automatic pumping works the same regardless of which mode is chosen, see code snippet below from the `pump_controller()` function. Here the pump tries to activate if the pump has never been on before or if it was 20 minutes ago. If the first condition is met and the soil moisture is under some threshold, the pump starts and pumps 100ml. 10% is removed from the water level, and it is saved to the json file.

```python
elif LAST_PUMP_END_TIME is 0 or time.time() - LAST_PUMP_END_TIME > config.PUMP_DELAY_S: 
            # Runs pump if moisture is under threshold
            if soil_moisture <= config.SOIL_MOISTURE_THRESHOLD:
                #print("Moisture is under threshold")
                ml_to_water = 100
                sensor.run_pump_ml(ml_to_water)

                if sensor.pump_stopped == True:
                    LAST_PUMP_END_TIME = time.time()

                    # calculate water level. Also makes sure that water level is not changed when benchmarking
                    if not BENCHMARK:
                        water_level = Sensor.retrieve_data("water_level")
                        water_level -= 10
                        Sensor.save_data("water_level", water_level)
                        print("Water level is: ", water_level)

                        #publish water level
                        connection.publish(config.AIO_WATER_LEVEL, str(Sensor.retrieve_data("water_level")))

```






# Transmitting the data / connectivity

Measurements from the sensors are taken every 3 seconds and stored in their respective variables. When 2 minutes have elapsed the current data values are sent using the MQTT protocol to their respective data feed in Adafruit IO. When the water level is updated, it is instead sent directly. All communication is done over Wifi since the device is always indoors and has easy wifi access. Also, no energy optimizations are needed since it is always plugged in, therefore data and sensor measurements can be sent and taken often. 

# Presenting the data
The dashboard shows the different data feeds. It saves data from the last 30 days when using the free tier. It saves data in the built in database every 2 minutes, or when an error is thrown by the code, or the water level is updated. It shows the following information:

* Current water level.
* Error logs from the last 24h.
* History of the soil temperature and soil moisture from the last 24h.
* History of inner temperature and humidity from the last 24h.
* Buttons for controlling the different modes. 1 for resetting water level, 2 for activating the pump, and 3 for calibrating the water flow rate. 

![image](https://hackmd.io/_uploads/SJDjUbhLC.png)




# Finalizing the design

The self-watering device does fulfil its purpose of automatically watering the plants. Prolonged testing has not been carried out, but the pump does start when the moisture level is too low. When adding water, the soil moisture goes almost immediately up to 100% and stays there for a while (has not been tested long enough for it to go down by itself). In the picture showing the dashboard in the previous section, the moisture level is seen to decrease abruptly, this is caused by moving the soil sensor to another pot. More testing is needed to iron out possible bugs and watch the moisture level decrease by itself. The device is not perfect and can be improved upon, such as:

* Fine tuning the settings, for example how much water to dispense at a time and at which soil humidity. This is however linked to which type of plant and pot size. 
* Use a longer hose, plug the end of it and add holes on the sides. This will water the soil more evenly.
* Show data for more than 24h in the dashboard, this is however just a setting that can be changed.
* Make it possible to change the moisture threshold from the dashboard.
* Add a physical mode switch to the device instead of using the dashboard. This was implemented at first but the switch was unfortunately broken. 

Overall the project went well without any major issues. The pymakr plugin for VS code seems to be filled with a lot of bugs. Sometimes the upload would freeze and the IDE had to be restarted. Also when changing code in a file in the lib folder, the device had to be replugged for the new code to be uploaded, this caused a lot of frustration. Some more testing is needed before i can fully rely on the device to water my plant without any hiccups but it looks promising. 



![image](https://hackmd.io/_uploads/HyfwDCAIR.png)

The Pico, sensors, and relay mounted to the inner lid of the coffe can. It was easy to remove and works great as a mount. 

![image](https://hackmd.io/_uploads/ryf9O00I0.png)

Longer cables soldered to the pump. The cables plug in to female connectors, the red one (positive) to the relay, and the black (negative) to the usb power supply. 

![image](https://hackmd.io/_uploads/ryypd0CL0.png)

The completed device with all components mounted in the coffe can.

![image](https://hackmd.io/_uploads/HkYGKRC8A.png)

The backside showing three female USB A connectors. Left for moisture sensor, middle for power to the Pico, and right for power to the pump. 


**[Video Demonstration](https://www.youtube.com/watch?v=hG9IqUO6Q6s)**

**Github Repository:** https://github.com/lurr3t/self_watering_plant

