from datetime import datetime
from enum import Enum, unique

from paai.model.measurement import Measurement
from pydantic import BaseModel

@unique
class Sensor(Enum):
    temperature = 'temperature'
    humidity = 'humidity'
    pressure = 'pressure'
    heart_rate = 'heart_rate'
    no_sensor = 'no_sensor'

class DeviceMessage(BaseModel):
    
    timestamp: datetime
    device_id: str
    # measurement: Measurement

    sensor: Sensor
    value: float

