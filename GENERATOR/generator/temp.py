import random
import time
import requests

# define device types and tags
DEVICE_TYPES = ['thermostat', 'barometer']
DEVICE_TAGS = {'thermostat': 'thermostat', 'barometer': 'barometer'}

# define HTTP POST endpoint
POST_URL = 'http://example.com/api/data'

# generate fake data for 5 devices
for device_id in range(1, 6):
    device_type = random.choice(DEVICE_TYPES)
    tag = DEVICE_TAGS[device_type]
    while True:
        timestamp = int(time.time())
        if device_type == 'thermostat':
            temperature = round(random.uniform(10.0, 30.0), 2)
            data = {'device_id': device_id, 'tag': tag, 'timestamp': timestamp, 'temperature': temperature}
        else:
            pressure = round(random.uniform(900.0, 1100.0), 2)
            data = {'device_id': device_id, 'tag': tag, 'timestamp': timestamp, 'pressure': pressure}
        response = requests.post(POST_URL, json=data)
        if response.status_code == 200:
            print(f'Sent data: {data}')
            break
        else:
            print(f'Error sending data: {response.status_code}')
        time.sleep(1)
