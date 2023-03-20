from typing import Union

from fastapi import APIRouter, Response, status
from loguru import logger
from paai.model import Barometer, HeartRateMeter, Hygrometer, Thermostat
from pydantic import Field
from typing_extensions import Annotated

api_router = APIRouter(tags=["Device"])

IoTDevice = Annotated[Union[Barometer, HeartRateMeter, Hygrometer, Thermostat], Field(discriminator='tag')]

@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/device")
async def message_from_device(iot_device: IoTDevice) -> Response:

    logger.debug(f"{type(iot_device)}: {iot_device}")
    # logger.debug(f"{type(iot_device.dict())}: {iot_device.dict()}")

    return Response(status_code=status.HTTP_200_OK)

