from paai.model.device import Device
from paai.model.device_message import DeviceMessage
from paai.model.measurement import Measurement


class MessageController:
    @staticmethod
    def process_raw_message(raw_message: Device) -> DeviceMessage:

        device_message = DeviceMessage(**{
            'timestamp': raw_message.timestamp,
            'device_id': raw_message.device_id,
            'measurement': MessageController.get_measurement(raw_message)
        })

        return device_message

    @staticmethod
    def get_measurement(raw_message: Device) -> Measurement:

        measurement = Measurement()
        if hasattr(raw_message, 'temperature'):
            measurement.temperature = raw_message.temperature
        elif hasattr(raw_message, 'humidity'):
            measurement.humidity = raw_message.humidity
        elif hasattr(raw_message, 'pressure'):
            measurement.pressure = raw_message.pressure
        elif hasattr(raw_message, 'heart_rate'):
            measurement.heart_rate = raw_message.heart_rate

        return measurement