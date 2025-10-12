import base64
import json
import logging
import requests
import time

from .helpers import (get_timeout, format_sn, parse_status)   # is_low_power_device
from .meari_error import (MeariError, MeariHttpError)
from .crypto_helpers import get_signature

from .model.user_info import UserInfo, PfKey
from .model.iot_info import IotInfo
# from .model.camera_info import CameraInfo

# Device API paths
DEVICE_STATUS_PATH = "/openapi/device/status"
DEVICE_CONFIG_PATH = "/openapi/device/config"
DEVICE_WAKE_PATH = "/openapi/device/awaken"
USER_CONFIG_PATH = "/openapi/client/config"
DEVICE_HISTORY_PATH = "/openapi/device/info/history"

# MQTT / Client communication paths
CUSTOMER_SEND_MSG = "/openapi/iot/client/pub"
CUSTOMER_ACK_CONFIRM = "/openapi/iot/client/ack"
CUSTOMER_PULL_MSG = "/openapi/iot/client/pull"
CUSTOMER_STATUS_MSG = "/openapi/client/status"

_LOGGER = logging.getLogger(__name__)


class MeariIotClient:

    def set_device_config(
        self,
        user_info: UserInfo,
        iot_info: IotInfo,
        sn: str,
        params_list: dict,
        is_to_server: bool,
        channel_id: int
    ) -> dict:

        pfKey: PfKey = user_info.iot.pfKey
        # http_params = {
        #     "accessid": pfKey.accessid,
        #     "expires": get_timeout(),
        #     "signature": self.__get_signature(DEVICE_CONFIG_PATH, "set", pfKey.accesskey),
        #     "action": "set",
        #     "deviceid": format_sn(sn)
        # }
        http_params = self.__build_http_params(pfKey, "set", sn, DEVICE_CONFIG_PATH)

        if is_to_server:
            http_params["target"] = "server"

        # --- Prepara il payload JSON codificato ---
        params_json = self.__params_json("set", params_list, channel_id)
        _LOGGER.info(f"meariIot--setDeviceConfig--paramsJson: {params_json}")
        encoded_params = base64.b64encode(params_json.encode()).decode('utf-8')

        http_params["params"] = encoded_params

        url = f"{iot_info.pfApi.openapi.domain}{DEVICE_CONFIG_PATH}"

        _LOGGER.debug(f"GET {url} with params: {http_params}")

        try:

            response = self.__get_request(http_params, url)
            self.__deal_wake(user_info, iot_info, sn)
            return response

        except Exception as e:
            raise RuntimeError(f"Error: {e}")

    def get_device_config(
        self,
        user_info: UserInfo,
        iot_info: IotInfo,
        sn: str,
        params_list: list[str],
        is_from_server: bool,
        channel_id: int
    ) -> None:

        pfKey: PfKey = user_info.iot.pfKey
        http_params = self.__build_http_params(pfKey, "get", sn, DEVICE_CONFIG_PATH)

        if is_from_server:
            http_params["target"] = "server"

        params_json = self.__params_json("get", params_list, channel_id)
        _LOGGER.info(f"meariIot--getDeviceConfig--paramsJson: {params_json}")
        http_params["params"] = base64.b64encode(params_json.encode()).decode("utf-8")

        url = f"{iot_info.pfApi.openapi.domain}{DEVICE_CONFIG_PATH}"

        try:
            response = self.__get_request(http_params, url)
            result = response.get("iot")
            return result

        except Exception as e:
            raise RuntimeError(f"Error: {e}")

    def get_device_status_get(
        self,
        user_info: UserInfo,
        iot_info: IotInfo,
        sn: str
    ) -> None:
        pfKey: PfKey = user_info.iot.pfKey
        http_params = self.__build_http_params(pfKey, "query", sn, DEVICE_STATUS_PATH)
        url = f"{iot_info.pfApi.openapi.domain}{DEVICE_STATUS_PATH}"

        _LOGGER.debug(f"GET {url} with params: {http_params}")

        try:
            response = self.__get_request(http_params, url)
            status = response.get("status")
            parsed_status = parse_status(status)
            return parsed_status

        except Exception as e:
            raise RuntimeError(f"Error: {e}")

    def get_device_all_config(
        self,
        user_info: UserInfo,
        iot_info: IotInfo,
        sn: str,
        is_from_server: bool,
        channel_id: int
    ) -> None:
        pfKey: PfKey = user_info.iot.pfKey
        http_params = self.__build_http_params(pfKey, "get", sn, DEVICE_CONFIG_PATH)

        if is_from_server:
            http_params["target"] = "server"

        params_json = self.__params_json("get", [], channel_id)
        _LOGGER.info(f"meariIot--getDeviceAllConfig--paramsJson: {params_json}")
        http_params["params"] = base64.b64encode(params_json.encode()).decode("utf-8")

        url = f"{iot_info.pfApi.openapi.domain}{DEVICE_CONFIG_PATH}"

        try:

            response = self.__get_request(http_params, url)
            # d = response.get("iot")
            # TODO map to DeviceParams
            return response

        except Exception as e:
            raise RuntimeError(f"Error: {e}")

    def __build_http_params(self, pfKey: PfKey, action: str, sn: str, url: str) -> dict:
        http_params = {
            "accessid": pfKey.accessid,
            "expires": get_timeout(),
            "signature": self.__get_signature(url, action, pfKey.accesskey),
            "action": action,
            "deviceid": format_sn(sn)
        }
        return http_params

    def __deal_wake(self, user_info: UserInfo, iot_info: IotInfo, sn: str) -> None:
        """Gestisce il wake del dispositivo se necessario."""
        if self.__need_wake(sn):
            self.__wake_device(user_info, iot_info, sn)

    def __need_wake(self, sn: str) -> bool:
        """Verifica se il dispositivo deve essere 'risvegliato'."""
        # camera_info: CameraInfo = MeariUser.get_instance().get_camera_info()
        # if (
        #     camera_info
        #     and sn == camera_info.sn_num
        #     and is_low_power_device(camera_info)
        # ):
        #     sn_num = format_sn(sn)
        #     tem_status = MeariIotController.get_instance().query_device_status()
        #
        #     _LOGGER.info(f"meariIot--dealWake--status: {tem_status.get(sn_num) if tem_status else None}")
        #
        #     if (
        #         tem_status
        #         and sn_num in tem_status
        #         and tem_status[sn_num] is not None
        #         and int(tem_status[sn_num]) != 1
        #     ):
        #         return True

        return False

    def __wake_device(self, user_info: UserInfo, iot_info: IotInfo, sn: str) -> None:
        """Invia la richiesta HTTP per 'svegliare' un dispositivo in sleep."""
        pfKey: PfKey = user_info.iot.pfKey
        http_params = self.__build_http_params(pfKey, "set", sn, DEVICE_WAKE_PATH)

        # Genera un sid univoco (max 30 caratteri)
        sid = f"{format_sn(sn)}{int(time.time() * 1000)}"[:30]
        http_params["sid"] = sid

        url = f"{iot_info.pfApi.openapi.domain}{DEVICE_WAKE_PATH}"

        _LOGGER.debug(f"GET {url} with params: {http_params}")

        try:
            self.__get_request(http_params, url)
            _LOGGER.info(f"Device {sn} wake request sent successfully.")
        except Exception as e:
            _LOGGER.error(f"Error waking device {sn}: {e}")

    def __params_json(self, action: str, params_list: dict, channel_id: int) -> str:
        """
        Builds the parameter JSON string required by the Meari IoT API.

        - Adds static fields: code, action, name
        - Optionally includes channel ID if > 0
        - Embeds `params_list` under the "iot" key
        - Returns a JSON-formatted string
        """
        params_object = {
            "code": 100001,
            "action": action,
            "name": "iot",
            "iot": params_list
        }

        if channel_id > 0:
            params_object["channel"] = channel_id

        return json.dumps(params_object)

    def __get_signature(self, path: str, action: str, access_key: str) -> str:
        origin = f"GET\n\n\n{get_timeout()}\n{path}\n{action}"
        return get_signature(origin, access_key)

    def __get_request(
        self,
        http_params: dict,
        url: str
    ) -> dict:

        _LOGGER.debug(f"GET {url} with params: {http_params}")

        try:

            response = requests.get(url, params=http_params)
            response.raise_for_status()

            if response.status_code == 200:

                response_json = response.json()

                # --- Controlla se mancano dati ---
                if not response_json:
                    raise MeariHttpError("Empty response")

                _LOGGER.info(f"meariIot--setDeviceConfig--URL: {response.url}")
                _LOGGER.info(f"meariIot--setDeviceConfig--data: {response_json}")

                # --- Controllo errori con errid === 401 + Timeout ---
                errid = response_json.get("errid")
                reason = response_json.get("reason", "")
                result_code = response_json.get("resultCode", -1)
                error_msg = response_json.get("errorMessage", "Unknown error")

                if errid == 401 and reason == "Timeout":
                    raise MeariError(error_msg, result_code)
                    # Richiedi nuovi token (simulate getIotInfoV2)
                    # def on_refresh_success():
                    #     self.__get_request(http_params, url)
                    #
                    # def on_refresh_error(code, msg):
                    #     callback.on_error(result_code, error_msg)
                    #
                    # try:
                    #     self.get_iot_info_v2(on_success=on_refresh_success, on_error=on_refresh_error, retry_count=1)
                    # except Exception as e:
                    #     raise MeariError(error_msg, result_code)
                else:
                    if result_code == 1001 or not errid:
                        return response_json
                    else:
                        raise MeariError(error_msg, result_code)

        except Exception as e:
            raise RuntimeError(f"Error: {e}")

    def __post_request(
        self,
        http_params: dict,
        url: str
    ) -> None:
        # TODO
        ...
