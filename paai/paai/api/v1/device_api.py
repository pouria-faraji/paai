import os
from typing import Union

from confluent_kafka import KafkaException
from fastapi import APIRouter, Request, Response, status
from loguru import logger
from paai.controller.message_controller import MessageController
from paai.model import Barometer, HeartRateMeter, Hygrometer, Thermostat
from pydantic import Field
from typing_extensions import Annotated

from json import dumps

api_router = APIRouter(tags=["Device"])

IoTDevice = Annotated[Union[Barometer, HeartRateMeter, Hygrometer, Thermostat], Field(discriminator='tag')]

@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/device")
async def message_from_device(iot_device: IoTDevice, request: Request) -> Response:

    logger.debug(f"{type(iot_device)}: {iot_device}")
    processed_message = MessageController.process_raw_message(iot_device)
    logger.debug(f"{type(processed_message)}: {processed_message}")

    try:
        await request.app.state.producer.produce(os.environ.get('PROCESSED_MESSAGES_TOPIC', 'processed_messages'), processed_message.json(exclude_none=True))
    except KafkaException as ex:
        logger.error(ex)
    # logger.debug(f"{type(iot_device.dict())}: {iot_device.dict()}")

    return Response(status_code=status.HTTP_200_OK)

