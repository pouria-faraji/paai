
from fastapi import APIRouter, Response, status
from generator.controller.generator import Generator, generator
from loguru import logger

api_router = APIRouter(tags=["Generator"])

@api_router.post("/start")
async def start_generator(numDevices: int = 3) -> Response:
    logger.info(f"Starting generator with {numDevices} devices")

    if generator.isBusy():
        return Response("Generator is already running.", status_code=status.HTTP_208_ALREADY_REPORTED, headers={'Content-Type': 'text/plain'})

    if int(numDevices) <= 0:
        return Response("Number of devices should be more than 0", status_code=status.HTTP_406_NOT_ACCEPTABLE, headers={'Content-Type': 'text/plain'})

    generator.thread = generator.start(int(numDevices))

    # generator.start(numDevices)
    return Response(f"Generator has started with {numDevices} devices.", status_code=status.HTTP_200_OK, headers={'Content-Type': 'text/plain'})

@api_router.post("/stop")
async def stop_generator() -> Response:
    logger.info("Stopping generator")

    generator.stop()
    return Response("Generator has stopped working.", status_code=status.HTTP_200_OK, headers={'Content-Type': 'text/plain'})

@api_router.get("/status")
async def get_status() -> Response:
    logger.info("Getting generator status")
    return Response(generator.getStatus(), status_code=status.HTTP_200_OK, headers={'Content-Type': 'text/plain'})




