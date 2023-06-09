import subprocess

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from generator.api.v1 import generator_api_router
from generator.settings import Settings

settings = Settings()
api_prefix = f'/api/v{settings.api_version}'
app_version = subprocess.check_output(['poetry', 'version']).decode('utf-8').split()[1] # Output is generator {version}
app = FastAPI(title=settings.project_name, openapi_url=f"{api_prefix}/openapi.json", version=app_version)

app.include_router(generator_api_router, prefix=api_prefix)

# Adding to CORS Middleware to allow connection from these URLs
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

@app.on_event("startup")
async def startup_event() -> None:
    """Initializations
    """
    logger.info('Generator Ready.')

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
