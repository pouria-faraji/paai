import os
import subprocess

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from paai.api.v1 import device_api_router
from paai.controller.kafka.aio_producer import AIOProducer
from paai.controller.kafka.kafka_controller import KafkaController
from paai.settings import Settings

settings = Settings()
api_prefix = f'/api/v{settings.api_version}'
app_version = subprocess.check_output(['poetry', 'version']).decode('utf-8').split()[1] # Output is paai {version}
app = FastAPI(title=settings.project_name, openapi_url=f"{api_prefix}/openapi.json", version=app_version)

app.include_router(device_api_router, prefix=api_prefix)

origins = [
    "http://localhost",
    "http://localhost:7000",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

kafka_producer_settings = {"bootstrap.servers": os.environ.get('BOOTSTRAP_SERVERS', 'localhost:9092')}

@app.on_event("startup")
async def startup_event() -> None:
    """Initializations
    """
    logger.info('PAAI Ready.')
    logger.info(f"Kafka bootstrap server is {kafka_producer_settings['bootstrap.servers']}")

    kafka_controller = KafkaController(kafka_producer_settings)
    kafka_controller.create_topic(os.environ.get('PROCESSED_MESSAGES_TOPIC', 'processed_messages'))

    app.state.producer = AIOProducer(kafka_producer_settings)

@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Shuting down.
    """
    logger.info("Done. Bye")

if __name__ == "__main__":
    uvicorn.run("main:app",
                host=settings.host,
                port=settings.port,
                log_level=settings.log_level,
                reload=settings.hot_reload)
