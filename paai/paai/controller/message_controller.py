from paai.model.device import Device
from paai.model.device_message import DeviceMessage, Sensor

class MessageController:
    """ A class having methods required for processing raw messages coming from devices.
    """

    # Transforming raw device messages into DeviceMessage datamodel
    @staticmethod
    def process_raw_message(raw_message: Device) -> DeviceMessage:
        """Transforms raw messages into DeviceMessage datamodel.
        """

        device_message = DeviceMessage(**{
            'timestamp': raw_message.timestamp,
            'device_id': raw_message.device_id,
            'sensor': MessageController.get_sensor(raw_message),
            'value': MessageController.get_value(raw_message)
        })

        return device_message

    @staticmethod
    def get_sensor(raw_message: Device) -> str:
        """Getting sensor based on the attribute of the raw message
        """

        if hasattr(raw_message, 'temperature'):
            return Sensor.temperature.value
        elif hasattr(raw_message, 'humidity'):
            return Sensor.humidity.value
        elif hasattr(raw_message, 'pressure'):
            return Sensor.pressure.name
        elif hasattr(raw_message, 'heart_rate'):
            return Sensor.heart_rate.value
        else:
            return Sensor.no_sensor.value

    @staticmethod
    def get_value(raw_message: Device) -> float:
        """Getting value of the sensor based on the attribute
        """
        if hasattr(raw_message, 'temperature'):
            return raw_message.temperature
        elif hasattr(raw_message, 'humidity'):
            return raw_message.humidity
        elif hasattr(raw_message, 'pressure'):
            return raw_message.pressure
        elif hasattr(raw_message, 'heart_rate'):
            return raw_message.heart_rate
        else:
            return 0