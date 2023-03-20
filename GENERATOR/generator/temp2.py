import requests
import time
import random

class Device:
    def __init__(self, device_type, device_id):
        self.device_type = device_type
        self.device_id = device_id
        self.tag = "thermostat" if device_type == "thermostat" else "barometer"
        self.field = "temperature" if device_type == "thermostat" else "pressure"
        
    def generate_data(self):
        timestamp = int(time.time())
        data = {
            "timestamp": timestamp,
            "device_id": self.device_id,
            "tag": self.tag,
            self.field: random.uniform(60, 80) if self.device_type == "thermostat" else random.uniform(900, 1100)
        }
        return data

devices = [Device("thermostat", "device1"), Device("thermostat", "device2"), 
           Device("thermostat", "device3"), Device("barometer", "device4"), Device("barometer", "device5")]

url = "http://your-post-endpoint-url"

while True:
    for device in devices:
        data = device.generate_data()
        response = requests.post(url, json=data)
        print(f"Sent data: {data}")
        print(f"Response status code: {response.status_code}")
    time.sleep(1)
