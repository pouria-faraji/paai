from typing import Literal

from paai.model.device import Device


class HeartRateMeter(Device):
    
    heart_rate: float
    tag: Literal['HeartRateMeter']
