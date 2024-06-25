from sensor import Sensor
from connection import Connection



# Try WiFi Connection
try:
    print("Booting up...") 
    Connection.connect_wifi()
    
except Exception as e:
    print(f"WiFi Connection Failed {e}")
    Sensor.wifi_error_light()
    


