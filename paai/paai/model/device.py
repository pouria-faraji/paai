from datetime import datetime

from pydantic import BaseModel


class Device(BaseModel):

    device_id: str
    timestamp: datetime
    tag: str
