from typing import Literal

from paai.model.device import Device

class Thermostat(Device):
    
    temperature: float
    tag: Literal['Thermostat']