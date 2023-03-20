from datetime import datetime

from paai.model.measurement import Measurement
from pydantic import BaseModel


class DeviceMessage(BaseModel):
    
    timestamp: datetime
    measurement: Measurement

