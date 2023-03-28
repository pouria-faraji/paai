
from fastapi import APIRouter, Response, status
from generator.controller.generator import Generator, generator
from loguru import logger
from json import dumps

api_router = APIRouter(tags=["Generator"])

@api_router.post("/start",
                 summary="Start Data Generation",
                 description="Starting the generation of IoT devices data. \n numDevices should be an Integer bigger than 0.\n Check /status endpoint for details about devices.")
async def start_generator(numDevices: int = 3) -> Response:
    """Starting the generation of IoT devices data. numDevices should be an Integer bigger than 0.

    Parameters
    ----------
    numDevices : int, optional
        Number of devices for data generation, by default 3
    """
    logger.info(f"Starting generator with {numDevices} devices")

    # Checking if the generator is already running.
    if generator.isBusy():
        return Response("Generator is already running.", status_code=status.HTTP_208_ALREADY_REPORTED, headers={'Content-Type': 'text/plain'})

    # Returning HTTP_406 error for values lower or equal than 0
    if int(numDevices) <= 0:
        return Response("Number of devices should be more than 0", status_code=status.HTTP_406_NOT_ACCEPTABLE, headers={'Content-Type': 'text/plain'})

    generator.thread = generator.start(int(numDevices))

    return Response(f"Generator has started with {numDevices} devices.", status_code=status.HTTP_200_OK, headers={'Content-Type': 'text/plain'})

@api_router.post("/stop",
                 summary="Stop Data Generation",
                 description="Stopping the generation of IoT devices data.")
async def stop_generator() -> Response:
    """Stopping the generation of IoT devices data.
    """
    logger.info("Stopping generator")

    generator.stop()
    return Response("Generator has stopped working.", status_code=status.HTTP_200_OK, headers={'Content-Type': 'text/plain'})

@api_router.get("/status",
                summary="Generator Status", 
                description="Getting details about devices and status of the generator.")
async def get_status() -> Response:
    """Getting details about devices and status of the generator.
    """
    logger.info("Getting generator status")
    return Response(dumps(generator.getStatus()), status_code=status.HTTP_200_OK, headers={'Content-Type': 'application/json'})




