import os
import random
import threading
import time
from datetime import datetime

import requests
from loguru import logger
from collections import defaultdict


class Generator(object):
    """Singleton Class for generating fake IoT device data
    """

    # To check if the generator is running or not
    busy: bool = False

    # Number of currently generating devices
    number_of_devices: int = 0

    # The interval of data sending can be modfified
    frequency = 1 # Sending data every {frequency} seconds

    # At the moment only 4 types of devices have been defined
    device_types = ['Thermostat', 'Barometer', 'Hygrometer', 'HeartRateMeter']

    # For keeping track of currently sending devices data
    generated_devices = {}

    # Sending requests to a POST API endpoint
    paai_endpoint = os.getenv("PAAI_ENDPOINT", "http://localhost:8000")
    iot_device_endpoint = paai_endpoint + '/api/v1/device'

    # This is a singleton class, so we keep track of the instance
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Generator, cls).__new__(cls)
        return cls.instance

    def start(self, number_of_devices):
        """Starting the data generation
        """
        # Setting seed will force generator to send the same devices each time the start is called.
        random.seed(50)

        # Making the current class busy
        self.busy = True
        self.number_of_devices = number_of_devices

        # Sending the requests using Thread to avoid blocking the UI
        thread = threading.Thread(target=self._run)
        thread.start()
        return thread
    

    def _run(self):
        """ Actual task of sending requests which runs on another thread
        """
        # Using lambda to return a random choice evertime we set a new key for the devices dictionary
        devices = defaultdict(lambda: random.choice(self.device_types))
        while self.busy:
            for i in range(1, self.number_of_devices + 1):
                device = devices[i]
                if device == "Thermostat":
                    temperature = round(random.uniform(10.0, 30.0), 2)
                    data = {'device_id': str(i), 'tag': device, 'timestamp': int(datetime.now().timestamp()), 'temperature': temperature}
                elif device == "Barometer":
                    pressure = round(random.uniform(900.0, 1100.0), 2)
                    data = {'device_id': str(i), 'tag': device, 'timestamp': int(datetime.now().timestamp()), 'pressure': pressure}
                elif device == "Hygrometer":
                    humidity = round(random.uniform(30.0, 100.0), 2)
                    data = {'device_id': str(i), 'tag': device, 'timestamp': int(datetime.now().timestamp()), 'humidity': humidity}
                elif device == "HeartRateMeter":
                    heart_rate = round(random.uniform(60.0, 100.0), 2)
                    data = {'device_id': str(i), 'tag': device, 'timestamp': int(datetime.now().timestamp()), 'heart_rate': heart_rate}

                # We also save the currently sending devices
                self.generated_devices[str(i)] = device

                logger.debug(f"ENDPOINT: {self.iot_device_endpoint}")

                # Sending a POST request to the API endpoint
                response = requests.post(self.iot_device_endpoint, json=data)
                if response.status_code == 200:
                    logger.debug(f"sent data: {data}")
            time.sleep(self.frequency)

    def stop(self):
        """Stopping the generator
        """
        self.busy = False

        # We wait for the thread to finish, if it has already not finished
        if hasattr(self, "thread"):
            self.thread.join()

    def isBusy(self) -> bool:
        """Getting the busy attribute of the generator
        """
        return self.busy

    def getStatus(self) -> str:
        """Getting the status of the generator
        """
        if self.busy:
            # Getting the status. number of devices, and device details 
            result = {
                'status': 'running',
                'numDevices': self.number_of_devices,
                'devices': [{'device_id': key, 'tag':value} for key, value in self.generated_devices.items()]
            }
            return result
        else:
            result = {
                'status': 'stopped'
            }
            return result

generator = Generator()
