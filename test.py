from meari_sdk.meari_client import MeariClient
from meari_sdk.meari_mqtt_message_id import MeariMqttMessageId
from const import KNOWN_PARTNERS, INTEGRATION_LANGUAGES
import time


def main():

    user_account = ""
    user_password = ""
    lng_type = "it"

    country_code = INTEGRATION_LANGUAGES[lng_type]["country_code"]
    phone_code = INTEGRATION_LANGUAGES[lng_type]["phone_code"]

    phone_type = "a"

    client = MeariClient(country_code=country_code, phone_code=phone_code, phone_type=phone_type, lng_type=lng_type, partner=KNOWN_PARTNERS['iegeek'])

    login_data = client.login(user_account.lower(), user_password)
    user_id = login_data["userID"]
    user_token = login_data["userToken"]
    print(login_data)
    print(user_id)
    print(user_token)

    # device = client.get_device()
    # print(device)

    while True:
        try:
            iot_info = client.fetch_iot_info()
            print(iot_info)
            break
        except Exception as e:
            print(f"Exception occurred: {e}. Retrying in 5 seconds...")
            time.sleep(5)

    def event_handler(msg, rawmsg):
        print(msg)
        if msg['msgid']:
            match int(msg['msgid']):
                case MeariMqttMessageId.PUSH_NOTIFICATION:
                    print(msg['alert'])
                    print(msg['url'])
                case _:
                    print("Unknown message ID received")

    client.event_handler = event_handler

    client.connect_mqtt_server()

    client.mqtt_client.loop_start()
    client.meari_mqtt_client.loop_start()

    client.mqtt_client._thread.join()
    client.meari_mqtt_client._thread.join()

    # client.mqtt_client.loop_forever()


if __name__ == "__main__":
    main()


# queryDeviceStatus()
# getDeviceParams

# https://openapi-euce.mearicloud.com/openapi/device/config?accessid=XXXXX&expires=1740325092&signature=XXXXX&action=get&params=eyJjb2RlIjoxMDAwMDEsImFjdGlvbiI6ImdldCIsIm5hbWUiOiJpb3QifQ%3D%3D&deviceid=XXXXX&target=server


# https://openapi-euce.mearicloud.com/openapi/device/config?accessid=XXXXX&expires=1740325346&signature=XXXXX&action=set&params=eyJjb2RlIjoxMDAwMDEsImFjdGlvbiI6InNldCIsIm5hbWUiOiJpb3QiLCJpb3QiOnsiODA3Ijoie1wicHNcIjo4MCxcInRzXCI6MCxcInpzXCI6MH0ifX0%3D&deviceid=XXXXX
# https://openapi-euce.mearicloud.com/openapi/device/config?accessid=XXXXX&expires=1740325346&signature=XXXXX&action=set&params=eyJjb2RlIjoxMDAwMDEsImFjdGlvbiI6InNldCIsIm5hbWUiOiJpb3QiLCJpb3QiOnsiODA4Ijoie30ifX0%3D&deviceid=XXXXX

# https://github.com/Mearitek/MeariSdk/blob/94e045923b95e3c54b0c80960eb1cc66af185688/Android/docs/Meari%20Android%20SDK%20Guide.md#9-device-settings