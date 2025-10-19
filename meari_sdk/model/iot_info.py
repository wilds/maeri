from dataclasses import dataclass
from typing import Optional
from dataclass_wizard import JSONWizard


@dataclass
class MQTT(JSONWizard):
    host: Optional[str] = None
    port: Optional[str] = None


@dataclass
class OpenAPI(JSONWizard):
    domain: Optional[str] = None


@dataclass
class Platform(JSONWizard):
    domain: Optional[str] = None
    signature: Optional[str] = None
    expireTime: Optional[int] = None


@dataclass
class PfApi(JSONWizard):
    mqtt: Optional[MQTT] = None
    mqttSignature: Optional[str] = None
    openapi: Optional[OpenAPI] = None
    platform: Optional[Platform] = None


@dataclass
class IotInfo(JSONWizard):
    cacheEndTime: Optional[int] = None
    pfApi: Optional[PfApi] = None
    aliIotEnable: Optional[str] = '0'
    time: Optional[int] = None
    keepalive: Optional[int] = None
