from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from dataclass_wizard import JSONWizard, json_field


@dataclass
class PfKey(JSONWizard):
    accessid: Optional[str] = None
    platformSignature: Optional[str] = None
    platformDomain: Optional[str] = None
    accesskey: Optional[str] = None
    openapiDomain: Optional[str] = None


@dataclass
class MqttAws(JSONWizard):
    host: Optional[str] = None
    port: Optional[str] = None
    clientId: Optional[str] = None
    subTopic: Optional[str] = None
    cognitoPoolId: Optional[str] = None
    cognitoRegion: Optional[str] = None
    iotPolicyName: Optional[str] = None
    certId: Optional[str] = None


@dataclass
class Mqtt(JSONWizard):
    host: Optional[str] = None
    port: Optional[str] = None
    iotId: Optional[str] = None
    iotToken: Optional[str] = None
    pk: Optional[str] = None
    dn: Optional[str] = None
    clientId: Optional[str] = None
    deviceSecret: Optional[str] = None
    crtUrls: Optional[str] = None
    keepalive: Optional[str] = None
    protocol: Optional[str] = None
    subTopic: Optional[str] = None
    region: Optional[str] = None


@dataclass
class Iot(JSONWizard):
    pfKey: Optional[PfKey] = None
    mqtt_aws: Optional[MqttAws] = None
    mqtt: Optional[Mqtt] = None


@dataclass
class UserInfo(JSONWizard):
    jpush_alias: Optional[str] = json_field("jpushAlias", default=None)
    user_id: Optional[int] = json_field("userID", default=None)
    client_id: Optional[str] = json_field("clientID", default=None, metadata={"deprecated": True})
    nick_name: Optional[str] = json_field("nickName", default=None)
    user_account: Optional[str] = json_field("userAccount", default=None)
    password: Optional[str] = field(default=None)
    create_date: Optional[datetime] = json_field("createDate", default=None)
    update_date: Optional[datetime] = json_field("updateDate", default=None)
    user_token: Optional[str] = json_field("userToken", default=None)
    image_url: Optional[str] = json_field("imageUrl", default=None)
    sound_flag: Optional[str] = json_field("soundFlag", default=None)
    login_time: Optional[datetime] = json_field("loginTime", default=None)
    country_code: Optional[str] = json_field("countryCode", default=None)
    phone_code: Optional[str] = json_field("phoneCode", default=None)
    partner_id: Optional[str] = json_field("partnerId", default=None)
    api_server: Optional[str] = json_field("apiServer", default=None)
    log_server: Optional[str] = json_field("logServer", default=None)
    audio_server: Optional[str] = json_field("audioServer", default=None)
    status: Optional[str] = field(default=None, metadata={"deprecated": True})
    desc: Optional[str] = field(default=None, metadata={"deprecated": True})
    login_type: Optional[int] = json_field("loginType", default=None)
    ring_duration: Optional[str] = json_field("ringDuration", default=None)
    iot_type: Optional[int] = json_field("iotType", default=None)
    meari_plat_open_api_server: Optional[str] = json_field("meariPlatOpenApiServer", default=None)
    meari_plat_domain: Optional[str] = json_field("meariPlatDomain", default=None)
    meari_plat_signature: Optional[str] = json_field("meariPlatSignature", default=None)
    email_auth_flag: int = json_field("emailAuthFlag", default=-1)
    promotion: int = json_field("promotion", default=-1)
    iot: Optional[Iot] = json_field("iot", default=None)
