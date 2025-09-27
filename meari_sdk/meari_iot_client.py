import base64
import json
import logging
import requests

from .helpers import (get_timeout, format_sn)
from .meari_error import (MeariError, MeariHttpError)
from .crypto_helpers import get_signature

from .model.user_info import UserInfo
from .model.iot_info import IotInfo

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
    ) -> None:

        pfKey = user_info.iot.pfKey
        http_params = {
            "accessid": pfKey.accessid,
            "expires": get_timeout(),
            "signature": self.__get_signature(DEVICE_CONFIG_PATH, "set", pfKey.accesskey),
            "action": "set",
            "deviceid": format_sn(sn)
        }

        if is_to_server:
            http_params["target"] = "server"

        # --- Prepara il payload JSON codificato ---
        params_json = self.__set_params_json(params_list, channel_id)
        _LOGGER.info(f"meariIot--setDeviceConfig--paramsJson: {params_json}")
        encoded_params = base64.b64encode(params_json.encode()).decode('utf-8')

        http_params["params"] = encoded_params

        url = f"{iot_info.pfApi.openapi.domain}{DEVICE_CONFIG_PATH}"

        _LOGGER.debug(f"GET {url} with params: {http_params}")

        try:

            response = requests.get(url, params=http_params)

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
                    #     self.set_device_config_advanced(sn, params_list, is_to_server, channel_id, callback)
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
                        # self.deal_wake(sn)
                        return response_json
                    else:
                        raise MeariError(error_msg, result_code)

        except Exception as e:
            raise RuntimeError(f"Error: {e}")

    def __set_params_json(self, params_list: dict, channel_id: int) -> str:
        """
        Builds the parameter JSON string required by the Meari IoT API.

        - Adds static fields: code, action, name
        - Optionally includes channel ID if > 0
        - Embeds `params_list` under the "iot" key
        - Returns a JSON-formatted string
        """
        params_object = {
            "code": 100001,
            "action": "set",
            "name": "iot",
            "iot": params_list
        }

        if channel_id > 0:
            params_object["channel"] = channel_id

        return json.dumps(params_object)

    def __get_signature(self, path: str, action: str, access_key: str) -> str:
        origin = f"GET\n\n\n{get_timeout()}\n{path}\n{action}"
        return get_signature(origin, access_key)

    def get_camera_info(self) -> None:
        ...

    def get_device_all_config(self, sn_num, is_to_server, channel_id) -> None:
        ...
