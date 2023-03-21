from typing import Literal

from paai.model.device import Device

class Hygrometer(Device):
    
    humidity: float
    tag: Literal['Hygrometer']