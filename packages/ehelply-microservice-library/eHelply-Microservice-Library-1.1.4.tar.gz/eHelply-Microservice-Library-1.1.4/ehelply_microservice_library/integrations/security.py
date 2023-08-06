from __future__ import annotations
from ehelply_bootstrapper.integrations.integration import Integration
from ehelply_microservice_library.integrations.fact import get_fact_endpoint
from ehelply_bootstrapper.utils.state import State
from fastapi import HTTPException, Header
from typing import List, Union
import requests
from pydantic import BaseModel


class Key(BaseModel):
    name: str
    summary: str


class Security(Integration):
    """
    Security integration is used to talk to the ehelply-security microservice
    """

    def __init__(self) -> None:
        super().__init__("security")

        self.m2m = State.integrations.get("m2m")

    def init(self):
        super().init()

    def load(self):
        super().load()

    def get_base_url(self) -> str:
        return get_fact_endpoint('ehelply-security')

    def create_token(self, length: int = 64) -> str:
        return self.m2m.requests.post(self.get_base_url() + "/tokens", json={"token": {"length": length}}).json()

    def create_key(self, key: Key, access_length: int = 32, secret_length: int = 32):
        return self.m2m.requests.post(self.get_base_url() + "/keys", json={"key": key.dict()},
                             params={"secret_length": secret_length, "access_length": access_length}).json()

    def verify_key(self, access: str, secret: str) -> Union[dict, bool]:
        payload: dict = {
            "key": {
                "access": access,
                "secret": secret
            }
        }
        response = self.m2m.requests.post(self.get_base_url() + "/keys/verify", json=payload)

        if response.status_code == 200:
            return response.json()

        return False


def verify_key(security: Security, access: str, secret: str, exception_if_unauthorized=True) -> Union[str, bool]:
    try:
        result = security.verify_key(access=access, secret=secret)

        if result:
            return result['uuid']

    except:
        pass

    if exception_if_unauthorized:
        raise HTTPException(status_code=403, detail="Unauthorized")
    else:
        return False
