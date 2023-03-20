import os
import random
import threading
import time
from datetime import datetime

import requests
from loguru import logger
from collections import defaultdict


class Generator(object):

    busy: bool = False
    number_of_devices: int = 0
    device_types = ['Thermostat', 'Barometer', 'Hygrometer', 'HeartRateMeter']

    paai_endpoint = os.getenv("PAAI_ENDPOINT", "http://localhost:8000")
    iot_device_endpoint = paai_endpoint + '/api/v1/device'

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Generator, cls).__new__(cls)
        return cls.instance

    # def get_random_device(self):
    #     return random.choice(self.device_types)

    def start(self, number_of_devices):
        random.seed(50)
        self.busy = True
        self.number_of_devices = number_of_devices
        


        thread = threading.Thread(target=self._run)
        thread.start()
        return thread
    

    def _run(self):
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
                response = requests.post(self.iot_device_endpoint, json=data)
                if response.status_code == 200:
                    logger.debug(f"sent data: {data}")
            time.sleep(1)

    def stop(self):
        self.busy = False

        if hasattr(self, "thread"):
            self.thread.join()

    def isBusy(self) -> bool:
        return self.busy

    def getStatus(self) -> str:
        if self.busy:
            return f"Generator is busy sending data of {self.number_of_devices} devices."
        else:
            return "Generator is stopped."

generator = Generator()
