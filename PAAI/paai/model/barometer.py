from typing import Literal

from paai.model.device import Device


class Barometer(Device):
    
    pressure: float
    tag: Literal['Barometer']
