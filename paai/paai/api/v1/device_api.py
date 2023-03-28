import os
from typing import Union

from confluent_kafka import KafkaException
from fastapi import APIRouter, Request, Response, status
from loguru import logger
from paai.controller.message_controller import MessageController
from paai.model import Barometer, HeartRateMeter, Hygrometer, Thermostat
from pydantic import Field
from typing_extensions import Annotated

api_router = APIRouter(tags=["Device"])

# Making a unified datamodel to be used as the API request body
IoTDevice = Annotated[Union[Barometer, HeartRateMeter, Hygrometer, Thermostat], Field(discriminator='tag')]

# This is the POST endpoint for receiving IoT devices data
@api_router.post("/device",
                 summary="Parse IoT Device Messages",
                 description="Parse, validate , and transform raw messages from IoT devices")
async def message_from_device(iot_device: IoTDevice, request: Request) -> Response:
    """Parse, validate , and transform messages from IoT devices
    """
    # Processing raw messages from IoT devices
    processed_message = MessageController.process_raw_message(iot_device)
    try:
        # Producing to the processed_messages topic in Kafka
        await request.app.state.producer.produce(os.environ.get('PROCESSED_MESSAGES_TOPIC', 'processed_messages'), processed_message.json(exclude_none=True))
    except KafkaException as ex:
        logger.error(ex)

    return Response(status_code=status.HTTP_200_OK)

