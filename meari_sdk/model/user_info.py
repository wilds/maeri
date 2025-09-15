from dataclasses import dataclass, field
from typing import Optional, Dict
from datetime import datetime
from dataclass_wizard import JSONWizard, json_field


@dataclass
class UserInfo(JSONWizard):
    jpush_alias: Optional[str] = json_field("jpushAlias")
    user_id: Optional[int] = json_field("userID")
    client_id: Optional[str] = json_field("clientID", default=None, metadata={"deprecated": True})
    nick_name: Optional[str] = json_field("nickName")
    user_account: Optional[str] = json_field("userAccount")
    password: Optional[str] = None
    create_date: Optional[datetime] = json_field("createDate")
    update_date: Optional[datetime] = json_field("updateDate")
    user_token: Optional[str] = json_field("userToken")
    image_url: Optional[str] = json_field("imageUrl")
    sound_flag: Optional[str] = json_field("soundFlag")
    login_time: Optional[datetime] = json_field("loginTime")
    country_code: Optional[str] = json_field("countryCode")
    phone_code: Optional[str] = json_field("phoneCode")
    partner_id: Optional[str] = json_field("partnerId")
    api_server: Optional[str] = json_field("apiServer")
    log_server: Optional[str] = json_field("logServer")
    audio_server: Optional[str] = json_field("audioServer")
    status: Optional[str] = field(default=None, metadata={"deprecated": True})
    desc: Optional[str] = field(default=None, metadata={"deprecated": True})
    login_type: Optional[int] = json_field("loginType")
    ring_duration: Optional[str] = json_field("ringDuration")
    iot_type: Optional[int] = json_field("iotType")
    meari_plat_open_api_server: Optional[str] = json_field("meariPlatOpenApiServer")
    meari_plat_domain: Optional[str] = json_field("meariPlatDomain")
    meari_plat_signature: Optional[str] = json_field("meariPlatSignature")
    email_auth_flag: int = json_field("emailAuthFlag", default=-1)
    promotion: int = json_field("promotion", default=-1)
    iot: Dict = None
