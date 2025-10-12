import base64
import json
import logging
# import asyncio
# import aiohttp
import random
import ssl
import time
from collections import defaultdict
from typing import Dict, Optional

import paho.mqtt.client as mqtt
import requests
from paho.mqtt.client import MQTTv311

from .const import APP_SIGN_FORMAT, BASE_DOMAIN, MEARI_KEY, MEARI_SECRET
from .crypto_helpers import (decode_param, des_utils_encode, encode_param,
                             get_signature, md5_32)
from .meari_error import (MeariError, MeariHttpError)
from .random_helpers import create_random_string
from .meari_iot_client import MeariIotClient

from .model.user_info import UserInfo, Mqtt
from .model.iot_info import IotInfo
from .model.device import MeariDevice
from .model.camera_info import CameraInfo

from .helpers import is_nvr_or_base

_LOGGER = logging.getLogger(__name__)


def map_to_query_string(params: Dict[str, str], encode: bool = False) -> str:
    if encode:
        return '&'.join(f"{key}={requests.utils.quote(value, safe='')}" for key, value in params.items())
    else:
        return '&'.join(f"{key}={value}" for key, value in params.items())


def map_to_query_string_signed(params: Dict[str, str], secret) -> str:
    timestamp = str(int(time.time() * 1000))
    next_int = random.randint(100000, 999999)
    params["signatureMethod"] = "HMAC-SHA1"
    params["timestamp"] = timestamp
    params["signatureVersion"] = "1.0"
    params["signatureNonce"] = next_int
    qs = '&'.join(f"{key}={value}" for key, value in sorted(params.items()))
    qs = qs + "&signature=" + get_signature(qs, secret)
    return qs


class MeariClient:
    """Meari http client."""
    # _main_loop: asyncio.AbstractEventLoop
    _country_code: str
    _phone_code: str
    _phone_type: str
    _lng_type: str
    _partner: dict

    _api_server: str = None
    _login_data: UserInfo = None
    _iot_info: IotInfo = None
    # _session: aiohttp.ClientSession

    _mqtt_client: mqtt.Client = None
    _meari_mqtt_client: mqtt.Client = None

    _iot_client: MeariIotClient = None

    _event_handler: Optional[callable] = None

    def __init__(
            self,
            country_code: str,
            phone_code: str,
            phone_type: str,
            lng_type: str,
            partner: dict,
            # loop: Optional[asyncio.AbstractEventLoop] = None
    ) -> None:
        """Constructor"""
        # self._main_loop = loop or asyncio.get_running_loop()
        self._country_code = country_code
        self._phone_code = phone_code
        self._phone_type = phone_type
        self._lng_type = lng_type
        self._partner = partner
        # self._session = aiohttp.ClientSession(loop=self._main_loop)

    @property
    def mqtt_client(self) -> mqtt.Client:
        return self._mqtt_client

    @property
    def meari_mqtt_client(self) -> mqtt.Client:
        return self._meari_mqtt_client

    @property
    def event_handler(self) -> Optional[callable]:
        return self._event_handler

    @event_handler.setter
    def event_handler(self, handler: callable) -> None:
        self._event_handler = handler

    @staticmethod
    def __get_http_header(url: str, user_token: Optional[str]) -> Dict[str, str]:
        headers = defaultdict(str)
        next_int = random.randint(100000, 999999)
        timestamp = str(int(time.time() * 1000))
        key = user_token if user_token else MEARI_KEY
        secret = user_token if user_token else MEARI_SECRET

        try:
            signature = get_signature(APP_SIGN_FORMAT.format('/ppstrongs/' + url, key, timestamp, next_int), secret)
            # signature = get_signature(f"api=/ppstrongs/{url}|X-Ca-Key={key}|X-Ca-Timestamp={timestamp}|X-Ca-Nonce={next_int}", secret)
            headers["X-Ca-Key"] = key
            headers["X-Ca-Timestamp"] = timestamp
            headers["X-Ca-Nonce"] = str(next_int)
            headers["X-Ca-Sign"] = signature

        except Exception as e:
            print(f"Error: {e}")

        return headers

    def __redirect(self, country_code: str, phone_code: str, user_account: str, phone_type: str, lng_type: str, partner: dict) -> None:
        signature = ""
        current_time_millis = int(time.time() * 1000)
        create_random = create_random_string(8)

        request_params = {
            "phoneType": phone_type,
            "appVer": partner["app_version"],
            "appVerCode": partner["app_version_code"],
            "lngType": lng_type,
            "t": str(current_time_millis),
            "sourceApp": partner['source_app'],
        }

        api_url = "/ppstrongs/redirect"
        if partner["init_type"] == "1":
            request_params["partnerId"] = partner['source_app']
            request_params["sign"] = md5_32(f"GET|{api_url}|{current_time_millis}|apis.meari.com.cn")
        else:
            request_params["partnerKey"] = partner['partner_key']
            request_params["partnerSecret"] = partner['partner_secret']
            api_url = "/ppstrongs/app/sdk/redirect"
            try:
                signature = get_signature(APP_SIGN_FORMAT.format(api_url, partner['partner_key'], current_time_millis, create_random), partner['partner_secret'])
            except Exception as e:
                print(f"Error: {e}")
                signature = ""
            request_params["sign"] = signature

        current_time_millis2 = int(time.time() * 1000)
        request_params["userAccount"] = encode_param(user_account, api_url, current_time_millis2, partner['partner_key'])
        request_params["localTime"] = str(current_time_millis2)
        request_params["nonce"] = create_random
        request_params["countryCode"] = country_code
        request_params["phoneCode"] = phone_code

        _LOGGER.debug(f"--->login2-redirect: {BASE_DOMAIN}{api_url}")
        _LOGGER.debug(map_to_query_string(request_params))

        try:
            redirect_response = requests.get(
                f"{BASE_DOMAIN}{api_url}?{map_to_query_string(request_params)}",
                headers=self.__get_http_header(api_url, None)
            )

            if redirect_response.status_code == 200:
                redirect_json = redirect_response.json()
                # print(redirect_json)
                if redirect_json.get("resultCode") == "1001":
                    return redirect_json.get("result", {})
                else:
                    raise MeariHttpError(
                        f"Login failed with resultCode: {redirect_json.get('resultCode')}",
                        redirect_json.get("resultCode"))
        except Exception as e:
            raise RuntimeError(f"Error: {e}")

    def __login(self, api_server: str, phone_code: str, user_account: str, phone_type: str, password: str, lng_type: str, limit_switch: bool, partner: dict) -> dict:

        current_time_millis = int(time.time() * 1000)

        login_request_params = {
            "phoneType": phone_type,
            "sourceApp":  partner['source_app'],
            "appVer":  partner['app_version'],
            "iotType": "4",  # TODO
            "equipmentNo": " ",
            "appVerCode": partner['app_version_code'],
            "localTime": str(current_time_millis),
            "password": des_utils_encode(password),
            "t": str(current_time_millis),
            "lngType": lng_type,
            # "countryCode": country_code,
            "userAccount": encode_param(user_account, "/meari/app/login", current_time_millis, partner['partner_key']),
            "phoneCode": phone_code,
        }
        if limit_switch:
            login_request_params["limitSwitch"] = "1"

        _LOGGER.debug(f"--->login2: {api_server}/meari/app/login")
        _LOGGER.debug(login_request_params)

        try:
            response = requests.post(
                f"{api_server}/meari/app/login",
                data=login_request_params,
                headers=self.__get_http_header("/meari/app/login", None)
            )
            if response.status_code == 200:
                # print(response.text)
                response_json = response.json()
                if response_json.get("resultCode") == "1001":
                    return response_json.get("result", {})
                else:
                    raise MeariHttpError(
                        f"Login failed with resultCode: {response_json.get('resultCode')}",
                        response_json.get("resultCode"))
        except Exception as e:
            raise RuntimeError(f"Error: {e}")

    def __get_iot_info(self, api_server: str, user_id: str, user_token: str, phone_code: str, phone_type: str, lng_type: str, partner: dict, refresh: int) -> dict:

        current_time_millis = int(time.time() * 1000)

        request_params = {
            "userToken": user_token,
            "userID": user_id,
            "phoneType": phone_type,
            "t": str(current_time_millis),
            "sourceApp":  partner['source_app'],
            "appVer":  partner['app_version'],
            "appVerCode": partner['app_version_code'],
            "lngType": lng_type,
            "phoneCode": phone_code,
            "iotType": "4",
        }
        if refresh == 1:
            request_params["refresh"] = refresh

        _LOGGER.debug(f"--->getIotInfo: {api_server}/v2/app/config/pf/init")
        _LOGGER.debug(map_to_query_string_signed(request_params, user_token))

        try:
            response = requests.get(
                f"{api_server}/v2/app/config/pf/init?{map_to_query_string_signed(request_params, user_token)}",
                headers=self.__get_http_header("/v2/app/config/pf/init", user_token)
            )
            if response.status_code == 200:
                # print(response.text)
                response_json = response.json()
                if response_json.get("resultCode") == "1001":
                    return response_json.get("result", {})
                else:
                    raise RuntimeError(f"getIotInfo failed with resultCode: {response_json.get('resultCode')}")
        except Exception as e:
            raise RuntimeError(f"Error: {e}")

    def __get_device(self, api_server: str, user_id: str, user_token: str, phone_code: str, phone_type: str, lng_type: str, partner: dict) -> dict:

        current_time_millis = int(time.time() * 1000)

        request_params = {
            "userToken": user_token,
            "userID": user_id,
            "phoneType": phone_type,
            # "deviceTypeID": device_type_id,
            "t": str(current_time_millis),
            "sourceApp":  partner['source_app'],
            "appVer":  partner['app_version'],
            "appVerCode": partner['app_version_code'],
            "lngType": lng_type,
            # "countryCode": country_code,
            "phoneCode": phone_code,
            "funSwitch": "1",
        }

        _LOGGER.debug(f"--->getDevice: {api_server}/ppstrongs/getDevice.action")
        _LOGGER.debug(request_params)

        try:
            response = requests.post(
                f"{api_server}/ppstrongs/getDevice.action",
                data=request_params,
                headers=self.__get_http_header("/ppstrongs/getDevice.action", user_token)
            )
            if response.status_code == 200:
                # print(response.text)
                response_json = response.json()
                if response_json.get("resultCode") == "1001":
                    return response_json
                else:
                    raise MeariError(f"getDevice failed with resultCode: {response_json.get('resultCode')}", response_json.get('resultCode'))
        except Exception as e:
            raise RuntimeError(f"Error: {e}")

    def login(self, user_account: str, user_password: str) -> UserInfo:
        try:
            redirect_data = self.__redirect(self._country_code, self._phone_code, user_account.lower(), self._phone_type, self._lng_type, self._partner)
            self._api_server = redirect_data.get("apiServer")

            self._login_data = UserInfo.from_dict(self.__login(self._api_server, self._phone_code, user_account.lower(), self._phone_type, user_password, self._lng_type, False, self._partner))
            self._user_id = self._login_data.user_id
            self._user_token = self._login_data.user_token

            if (self._login_data.api_server is None):
                self._login_data.api_server = self._api_server

            return self._login_data

        except MeariHttpError as mhe:
            _LOGGER.error(f"MeariHttpError occurred: {mhe}")
            raise
        except Exception as e:
            _LOGGER.error(f"An unexpected error occurred: {e}")
            raise RuntimeError(f"Login failed: {e}")

    def load_login_data_from_file(self, filename):
        try:
            with open(filename, "r") as file:
                data = json.load(file)

            self._login_data = UserInfo.from_dict(data)
            self._api_server = self._login_data.api_server
            self._user_id = self._login_data.user_id
            self._user_token = self._login_data.user_token

            return self._login_data

        except Exception as e:
            _LOGGER.error(f"An unexpected error occurred: {e}")
            raise RuntimeError(f"Login failed: {e}")

    def store_login_data_to_file(self, filename):
        try:
            with open("login_data.json", "w") as file:
                json.dump(self._login_data.to_dict(), file)
        except Exception as e:
            _LOGGER.error(f"An unexpected error occurred: {e}")
            raise RuntimeError(f"Login save failed: {e}")

    def fetch_iot_info(self) -> IotInfo:
        self._iot_info = IotInfo.from_dict(self.__get_iot_info(self._api_server, self._user_id, self._user_token, self._phone_code, self._phone_type, self._lng_type, self._partner, 0))
        self._iot_client = MeariIotClient()
        return self._iot_info

    def get_device(self) -> MeariDevice:
        device = self.__get_device(self._api_server, self._user_id, self._user_token, self._phone_code, self._phone_type, self._lng_type, self._partner)
        return MeariDevice.from_dict(device)

    def connect_mqtt_server(self) -> bool:
        # login_type = self._login_data.get('loginType')
        login_type = 2
        aliIotEnable = int(self._iot_info.aliIotEnable)
        if login_type == 0:
            # connection with userinfo
            # deprecated
            # format_str = f"iot-dev/{mqttInfo.get('pk')}/{mqttInfo.get('dn')}"
            # randomString = create_random_string(10, True)
            # try:
            #     str_value = get_signature(f"{mqttInfo.get('pk')}|{mqttInfo.get('dn')}", mqttInfo.get('deviceSecret'))
            # except Exception as e:
            #     print(f"Error in HMAC SHA1 encoding: {e}")
            # client_id = f"{format_str}{randomString}"
            # server_url = f"ssl://{mqttInfo['host']}:{port}"
            # username = format_str
            # password = str_value
            ...
        elif login_type == 1:
            # connection with mqttinfo
            # deprecated
            ...
        elif login_type == 2:
            # connection iot
            if aliIotEnable == 1:
                self._mqtt_client = self.__add_connect_iot(1, self._login_data, self._login_data.iot.mqtt, self._iot_info, self._partner)

            self._meari_mqtt_client = self.__add_connect_iot(3, self._login_data, self._login_data.iot.mqtt, self._iot_info, self._partner)

        return self._mqtt_client is not None or self._meari_mqtt_client is not None

    def __add_connect_iot(self, iot_type, user_info: UserInfo, mqtt_info: Mqtt, iot_info: IotInfo, partner: dict) -> None:
        if iot_type == 1:
            # ali
            # buildMqttIotService
            client_id = str(mqtt_info.clientId)
            server_url = mqtt_info.host
            port = int(mqtt_info.port)
            username = mqtt_info.iotId
            password = mqtt_info.iotToken
            keep_alive = iot_info.keepalive or 300

            topics = [
                mqtt_info.subTopic
            ]

        elif iot_type == 2:
            # aws
            ...

        else:
            # todo
            # buildMeariMqttIotService

            meariplat_signature = iot_info.pfApi.platform.signature
            decoded_device_token = decode_param(meariplat_signature, user_info.user_id, iot_info.pfApi.platform.expireTime, partner['source_app'])

            # key_temp = f"{user_info['userID']}{partner['source_app']}a{iot_info['pfApi']['platform']['expireTime']}"
            # encoded_key = base64.b64encode(key_temp.encode('utf-8')).decode('utf-8')
            # decoded_device_token = decode_device_token(encoded_key, meariplat_signature, False)
            # print(decoded_device_token)

            # Estrai la parte prima di "-" e decodificala in Base64
            first_part = decoded_device_token.split("-")[0]
            decoded_info_str = base64.b64decode(first_part.encode('utf-8')).decode('utf-8')
            base_json_object = json.loads(decoded_info_str)
            # Estrai accessid e accesskey
            meariplat_access_id = base_json_object.get("accessid")
            # meariplat_access_key = base_json_object.get("accesskey")

            client_id = str(user_info.user_id)
            server_url = iot_info.pfApi.mqtt.host
            port = int(iot_info.pfApi.mqtt.port)
            username = meariplat_access_id
            password = iot_info.pfApi.mqttSignature
            keep_alive = 300

            topics = [
                f"$bsssvr/iot/{user_info.user_id}/{user_info.user_id}/event/update/accepted",
                f"$bsssvr/iot/presence/disconnected/{user_info.user_id}"
            ]

        # print(f"client_id {client_id}")
        # print(f"server_url {server_url}")
        # print(f"port {port}")
        # print(f"username {username}")
        # print(f"password {password}")
        # print(topics)
        # print(f"keep_alive {keep_alive}")

        mqtt_client = mqtt.Client(client_id=client_id, protocol=MQTTv311)

        def on_connect(client, userdata, flags, reason_code):
            if reason_code > 0:
                print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
            else:
                print("connected")
                for topic in topics:
                    client.subscribe(topic)

        def on_connect_fail(client, userdata):
            print("connect failed")

        def on_message(client, userdata, msg):
            # print("message received "   , str(msg.payload.decode("utf-8")))
            # print("message topic="      , msg.topic)
            # print("message qos="        , msg.qos)
            # print("message retain flag=", msg.retain)
            event_handler = self._event_handler
            if event_handler:
                try:
                    event_handler(json.loads(msg.payload.decode("utf-8")), msg)
                except Exception as err:
                    _LOGGER.error(f"Caught exception in user defined callback function event_handler: {err}")
                    raise

        def on_disconnect(client, userdata, rc):
            print(f"disconnected with reason code: {rc}")

        def on_subscribe(client, userdata, mid, reason_code_list):
            print(f"subscribed {mid}")

        mqtt_client.on_connect = on_connect
        mqtt_client.on_connect_fail = on_connect_fail
        mqtt_client.on_message = on_message
        mqtt_client.on_disconnect = on_disconnect
        mqtt_client.on_subscribe = on_subscribe

        mqtt_client.tls_set(cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLSv1_2)
        mqtt_client.tls_insecure_set(True)

        mqtt_client.username_pw_set(username, password)
        mqtt_client.connect(server_url, port, keep_alive)

        return mqtt_client

    def query_device_status(self) -> Dict[str, int]:
        """
        Get device online status
        String Intercepted SN, cameraInfo.getSnNum().substring(4)
        Integer 0-connecting; 1-online; 2-offline; 3-sleep

        """
        ...
        # TODO

    def get_device_params(self, thing_name: str, sn_num: str, iot_type: int) -> Dict[str, str]:  # return type DeviceParams.java
        """
        Get device parameters
        """
        return self.__get_iot_property(self._login_data, iot_type, thing_name, sn_num, None)

    def __get_iot_property(self, user_info: UserInfo, iot_type, thing_name, sn_num, tag):
        if iot_type == 2:
            # try:
            #     # AWS IoT Shadow-style
            #     result = get_shadow_task(thing_name)
            #     obj = json.loads(result)
            #     state = obj.get("state", {})
            #     reported = state.get("reported", {})
            #     callback.on_success(JsonUtil.get_device_params_iot(reported))
            # except Exception as e:
            #     callback.on_failed(-1, str(e))
            ...

        elif iot_type == 3:
            # Meari IoT SDK-style
            camera_info: CameraInfo = None  # TODO: get camera info by sn_num
            is_nvr = is_nvr_or_base(camera_info)
            nvr_channel_id = camera_info.nvr_channel_id if is_nvr else None
            is_all_config = not is_nvr

            if is_nvr and nvr_channel_id > 0:
                return self._iot_client.get_device_all_config(self._login_data, self._iot_info, sn_num, False, nvr_channel_id)
            else:
                return self._iot_client.get_device_all_config(self._login_data, self._iot_info, sn_num, True, is_all_config)

        else:
            try:
                country_code = user_info.countryCode
                user_token = user_info.userToken

                url = f"{self.api_server}/meari/app/iot/model/get?iotType=4&countryCode={country_code()}"
                headers = self.__get_http_headers(
                    path="/meari/app/iot/model/get",
                    token=user_token
                )
                params = {"sn": sn_num}

                response = requests.get(url, headers=headers, params=params)
                if response.status_code == 200:
                    data = response.json()
                    result_code = data.get("resultCode")
                    if result_code == 1001:
                        result = data.get("jsonResult", {}).get("result", {})
                        # callback.on_success(JsonUtil.get_device_params_iot(result))
                        return result
                    else:
                        # callback.on_failed(result_code, data.get("errorMessage"))
                        ...
                else:
                    # callback.on_failed(response.status_code, response.text)
                    ...

            except Exception as e:
                print(e)
                # callback.on_failed(-1, str(e))
                ...

    def set_device_config(self, thing_name: str, sn_num: str, iot_type: int, params: dict) -> None:
        return self.__set_device_config(self._login_data, self._iot_info, iot_type, thing_name, sn_num, params)

    def __set_device_config(self, user_info: UserInfo, iot_info: IotInfo, iot_type: int, thing_name: str, sn_num: str, params: dict) -> None:
        """
        Sends a configuration to the device, supporting multiple types of IoT devices.

        :param iot_type: type of device (2 = shadow, 3 = Meari IoT, other = HTTP API)
        :param thing_name: device name (used for shadow)
        :param sn_num: device serial number
        :param params: dictionary of parameters to send (e.g. {"106": 1})
        :param tag: identifier object for the request (used for tracking/logging)
        :param callback: object with on_success(result) and on_error(code, message) methods

        """

        if iot_type == 2:
            # AWS IoT Shadow-style
            # payload = {
            #     "state": {
            #         "desired": params
            #     }
            # }
            # def on_success(result):
            #     callback.on_success(result)
            #
            # def on_error(error):
            #     callback.on_error(-1, str(error))
            #
            # try:
            #     self.__update_shadow(
            #         thing_name, payload,
            #         on_success=on_success,
            #         on_error=on_error
            #     )
            # except Exception as e:
            #     on_error(e)
            ...

        elif iot_type == 3:
            # Meari IoT SDK-style
            try:
                return self._iot_client.set_device_config(user_info, iot_info, sn_num, params, True, 0)
            except Exception as e:
                raise RuntimeError(f"Error: {e}")

        else:
            # HTTP REST API fallback
            request_params = {
                "": json.dumps(params)  # il backend si aspetta il payload come stringa JSON
            }

            country_code = user_info.country_code
            user_token = user_info.user_token

            url = f"{self.api_server}/meari/app/iot/model/set?sn={sn_num}&iotType=4&countryCode={country_code}"

            headers = self.__get_http_headers(
                path="/meari/app/iot/model/set",
                token=user_token
            )

            _LOGGER.debug(f"--->set_device_config: {url}")
            _LOGGER.debug(f"Params: {request_params}")

            try:
                response = requests.post(
                    url,
                    data=request_params,
                    headers=headers
                )

                if response.status_code == 200:
                    data = response.json()
                    _LOGGER.info(f"set_device_config result: {data.get('result')}")

                    if data.get("resultCode") == 1001:
                        # callback.on_success(data.get("result"))
                        return data
                    else:
                        # callback.on_error(data.get("resultCode"), data.get("errorMessage"))
                        ...
                else:
                    # callback.on_error(response.status_code, response.text)
                    ...

            except Exception as e:
                # callback.on_error(-1, str(e))
                print(e)

    def get_device_config(self, thing_name: str, sn_num: str, iot_type: int, params: dict) -> None:
        return self.__get_device_config(self._login_data, self._iot_info, iot_type, thing_name, sn_num, params)

    def __get_device_config(self, user_info: UserInfo, iot_info: IotInfo, iot_type: int, thing_name: str, sn_num: str, params: dict) -> None:
        # TODO
        if iot_type == 2:
            ...
        elif iot_type == 3:
            # Meari IoT SDK-style
            try:
                return self._iot_client.get_device_config(user_info, iot_info, sn_num, params, self.__is_server(params), 0)
            except Exception as e:
                raise RuntimeError(f"Error: {e}")

    def __is_server(self, params_list: dict) -> None:
        """
        Decides whether to send device config to server or device based on DP keys
        :param params_list: Dictionary of DP values to set
        """
        is_to_server = True

        try:
            for key in params_list.keys():
                dp = int(key)
                # If dp is outside the [800–899] range OR it's 825, send to server
                if dp < 800 or dp >= 900 or dp == 825:
                    is_to_server = True
                    break
                else:
                    is_to_server = False
        except Exception as e:
            _LOGGER.exception(f"Error determining is_to_server flag. err: {e}")
            is_to_server = False  # Fallback to safe default

        return is_to_server
