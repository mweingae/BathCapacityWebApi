import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import logging

from .logging_setup import setup_logging
from .config import *
from app.services.data_collector import DataCollector
from app.routers import data, facilities, settings

setup_logging(
    log_level=LOG_LEVEL,
    log_file=LOG_FILE
)
logger = logging.getLogger("app.main")

# Background task management
background_tasks = set()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start background data collection
    collector = DataCollector()
    task = asyncio.create_task(collector.run_continuous_collection())
    background_tasks.add(task)
    
    yield  # App is running
    
    # Shutdown: Cancel background tasks
    for task in background_tasks:
        task.cancel()
    await asyncio.gather(*background_tasks, return_exceptions=True)

app = FastAPI(lifespan=lifespan)

app.include_router(data.router)
app.include_router(facilities.router)
app.include_router(settings.router)

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>Bath Capacity Web Api</title>
        </head>
        <body>
            <h1>Welcome to Bath Capacity Web API!</h1>
        </body>
    </html>
    """
