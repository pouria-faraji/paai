from typing import Optional

from pydantic import BaseModel


class Measurement(BaseModel):
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    pressure: Optional[float] = None
    heart_rate: Optional[float] = None
