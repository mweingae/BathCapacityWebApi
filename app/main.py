import logging
from .logging_setup import setup_logging
from .config import *
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.routers import data, facilities, settings

setup_logging(
    log_level=LOG_LEVEL,
    log_file=LOG_FILE
)
logger = logging.getLogger("app.main")

app = FastAPI()

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
