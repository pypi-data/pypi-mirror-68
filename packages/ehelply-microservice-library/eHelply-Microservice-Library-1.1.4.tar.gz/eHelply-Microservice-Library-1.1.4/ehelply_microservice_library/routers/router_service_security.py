"""
STD Libraries
Nothing interesting here
"""
import uuid
import datetime
from typing import List, Union, Dict, Any

"""
3rd Party Libraries
Not much interesting here. We have some default imports for FastAPI endpoints and common SQL Alchemy use cases
"""
from fastapi import APIRouter, Cookie, Depends, Body, Query, Header

"""
eHelply Bootstrapper
Now we are getting interesting.
- State provides you with access to the app state
- get_db is used with Dependency injection to obtain a fresh DB connection session
    `db: Session = Depends(get_db)`
- Responses imports a bunch of default HTTP responses that eHelply has standardized on. Use these where possible as your
    return from each endpoint
"""
from ehelply_bootstrapper.utils.state import State

from ehelply_bootstrapper.drivers.fast_api_utils.responses import *

from ehelply_batcher.abstract_timer_service import AbstractTimerService
from ehelply_logger.Logger import Logger
import threading

"""
Router
This is a self-contained router instance. By itself it does nothing, but by attaching endpoints to it using decorator
  notation, you can make an epic router!
"""
router = APIRouter()


@router.post(
    '/keys/categories/{category_name}',
    tags=["keys"],
)
async def add_key(category_name: str, data: dict = Body({})):
    """
    Add a new key
    :return:
    """
    State.secrets.add(data['key'], category=category_name)

    return http_200_ok({"message": "Added key"})


@router.delete(
    '/keys/categories/{category_name}',
    tags=["keys"],
)
async def remove_key(category_name: str, data: dict = Body({})):
    """
    Add a new key
    :return:
    """
    State.secrets.remove(data['key'], category=category_name)

    return http_200_ok({"message": "Removed key"})


class SecurityKeys(AbstractTimerService):
    """
    Periodically checks for new or removed keys
    """
    def __init__(self, logger: Logger, delay_seconds: int):
        self.logger: Logger = logger

        super().__init__(
            name="SecurityKeys",
            delay_seconds=delay_seconds,
            logger=logger,
        )

    def proc(self):
        pass
        # self.logger.info("PROC'd")


class SecurityKeysThread(threading.Thread):
    def __init__(self, logger: Logger, delay: int):
        super().__init__()
        self.timer: SecurityKeys = None
        self.logger = logger
        self.delay: int = delay

    def run(self) -> None:
        self.timer = SecurityKeys(
            logger=self.logger,
            delay_seconds=self.delay
        )
