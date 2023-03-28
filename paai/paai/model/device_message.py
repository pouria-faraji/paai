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
    """DeviceMessage datamodel used for transmitting data to Kafka
    """
    timestamp: datetime
    device_id: str
    sensor: Sensor
    value: float

