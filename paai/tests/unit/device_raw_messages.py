from datetime import timezone

from paai.model.barometer import Barometer
from paai.model.heart_rate_meter import HeartRateMeter
from paai.model.hygrometer import Hygrometer
from paai.model.thermostat import Thermostat
from paai.model.device_message import DeviceMessage, Sensor
from paai.controller.message_controller import MessageController


def test_valid_Thermostat() -> None:
    raw_message = {
        "device_id": "999",
        "timestamp": 1680185496,
        "temperature": 29.1,
        "tag": "Thermostat"
    }

    device_message = Thermostat.parse_obj(raw_message)

    assert device_message.device_id == "999"
    assert device_message.timestamp.replace(tzinfo=timezone.utc).timestamp() == 1680185496
    assert device_message.temperature == 29.1
    assert device_message.tag == "Thermostat"

def test_valid_Barometer() -> None:
    raw_message = {
        "device_id": "111",
        "timestamp": 1680185496,
        "pressure": 1060.0,
        "tag": "Barometer"
    }

    device_message = Barometer.parse_obj(raw_message)

    assert device_message.device_id == "111"
    assert device_message.timestamp.replace(tzinfo=timezone.utc).timestamp() == 1680185496
    assert device_message.pressure == 1060.0
    assert device_message.tag == "Barometer"

def test_valid_Hygrometer() -> None:
    raw_message = {
        "device_id": "222",
        "timestamp": 1680185496,
        "humidity": 50.4,
        "tag": "Hygrometer"
    }

    device_message = Hygrometer.parse_obj(raw_message)

    assert device_message.device_id == "222"
    assert device_message.timestamp.replace(tzinfo=timezone.utc).timestamp() == 1680185496
    assert device_message.humidity == 50.4
    assert device_message.tag == "Hygrometer"

def test_valid_HeartRateMeter() -> None:
    raw_message = {
        "device_id": "333",
        "timestamp": 1680185496,
        "heart_rate": 80,
        "tag": "HeartRateMeter"
    }

    device_message = HeartRateMeter.parse_obj(raw_message)

    assert device_message.device_id == "333"
    assert device_message.timestamp.replace(tzinfo=timezone.utc).timestamp() == 1680185496
    assert device_message.heart_rate == 80
    assert device_message.tag == "HeartRateMeter"

def test_transform_Thermostat():
    raw_message = {
        "device_id": "999",
        "timestamp": 1680185496,
        "temperature": 29.1,
        "tag": "Thermostat"
    }

    device_message = Thermostat.parse_obj(raw_message)

    processed_message: DeviceMessage = MessageController.process_raw_message(device_message)

    assert processed_message.device_id == device_message.device_id
    assert processed_message.timestamp == device_message.timestamp
    assert processed_message.sensor.value == Sensor.temperature.value
    assert processed_message.value == device_message.temperature

def test_transform_Barometer():
    raw_message = {
        "device_id": "111",
        "timestamp": 1680185496,
        "pressure": 1060.0,
        "tag": "Barometer"
    }

    device_message = Barometer.parse_obj(raw_message)

    processed_message: DeviceMessage = MessageController.process_raw_message(device_message)

    assert processed_message.device_id == device_message.device_id
    assert processed_message.timestamp == device_message.timestamp
    assert processed_message.sensor.value == Sensor.pressure.value
    assert processed_message.value == device_message.pressure

def test_transform_Hygrometer():
    raw_message = {
        "device_id": "333",
        "timestamp": 1680185496,
        "humidity": 50.4,
        "tag": "Hygrometer"
    }

    device_message = Hygrometer.parse_obj(raw_message)

    processed_message: DeviceMessage = MessageController.process_raw_message(device_message)

    assert processed_message.device_id == device_message.device_id
    assert processed_message.timestamp == device_message.timestamp
    assert processed_message.sensor.value == Sensor.humidity.value
    assert processed_message.value == device_message.humidity

def test_transform_Hygrometer():
    raw_message = {
        "device_id": "444",
        "timestamp": 1680185496,
        "heart_rate": 80,
        "tag": "HeartRateMeter"
    }

    device_message = HeartRateMeter.parse_obj(raw_message)

    processed_message: DeviceMessage = MessageController.process_raw_message(device_message)

    assert processed_message.device_id == device_message.device_id
    assert processed_message.timestamp == device_message.timestamp
    assert processed_message.sensor.value == Sensor.heart_rate.value
    assert processed_message.value == device_message.heart_rate