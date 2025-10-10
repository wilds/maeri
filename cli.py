from meari_sdk.meari_client import MeariClient
from const import KNOWN_PARTNERS, INTEGRATION_LANGUAGES
from meari_sdk.meari_mqtt_message_id import MeariMqttMessageId

import cmd
import threading


class MeariCLI(cmd.Cmd):
    prompt = '>> '
    intro = 'Welcome to MeariCLI. Type "help" for available commands.'

    client: MeariClient = None
    mqtt_thread: threading.Thread = None

    def __init__(self):
        super().__init__()

    def do_connect(self, args):
        """
        Establishes a connection to the specified partner's server using the provided user credentials
        and language type.
        Args:
            - user_account (str): The user's account name or email.
            - user_password (str): The user's password.
            - lng_type (str, optional): The language type (default is 'it').
            - partner (str, optional): The partner name (default is 'iegeek').
        """
        args_list = args.split()
        user_account = args_list[0] if len(args_list) > 0 else ''
        user_password = args_list[1] if len(args_list) > 1 else ''
        lng_type = args_list[2] if len(args_list) > 2 else 'it'
        partner = args_list[3] if len(args_list) > 3 else 'iegeek'
        print(f"Connecting to {partner} with user: {user_account}")
        country_code = INTEGRATION_LANGUAGES[lng_type]["country_code"]
        phone_code = INTEGRATION_LANGUAGES[lng_type]["phone_code"]
        phone_type = "a"

        try:
            self.client = MeariClient(country_code=country_code, phone_code=phone_code, phone_type=phone_type, lng_type=lng_type, partner=KNOWN_PARTNERS[partner])

            if (user_account == ''):
                self.login_data = self.client.load_login_data_from_file("./login_data.json")
            else:
                self.login_data = self.client.login(user_account.lower(), user_password)
            self.iot_info = self.client.fetch_iot_info()

            print(f"Connected to {partner} with user: {user_account}")

            self.client.store_login_data_to_file("./login_data.json")

            def event_handler(msg, rawmsg):
                print(msg)
                msgContent = msg.get('params', {}).get('result', {})
                match int(msgContent['msgid']):
                    case MeariMqttMessageId.PUSH_NOTIFICATION:
                        print(msgContent['alert'])
                        print(msgContent['url'])
                    case MeariMqttMessageId.LOGIN_ON_OTHER_DEVICES:
                        print("Logged in on other device")
                    case _:
                        print("Unknown message ID received")

            self.client.event_handler = event_handler

            print("Connecting to MQTT server")
            if self.client.connect_mqtt_server():
                # Start both MQTT client loops in a single thread
                def start_mqtt_loops():
                    try:
                        if self.client.mqtt_client:
                            self.client.mqtt_client.loop_start()
                        if self.client.meari_mqtt_client:
                            self.client.meari_mqtt_client.loop_start()
                        print("Connected to MQTT server")
                    except Exception as e:
                        print(f"Error starting MQTT: {e}")

                self.mqtt_thread = threading.Thread(target=start_mqtt_loops)
                self.mqtt_thread.daemon = True
                self.mqtt_thread.start()
        except Exception as e:
            print(f"Error: {e}")

    def do_print_user_info(self, line):
        print(self.login_data)

    def do_fetch_iot_info(self, line):
        """
        Fetches IoT (Internet of Things) information
        """
        try:
            self.iot_info = self.client.fetch_iot_info()
            print(self.iot_info)
        except Exception as e:
            print(f"Error: {e}")

    def do_get_devices(self, line):
        """
        Fetches device information
        """
        try:
            self.devices = self.client.get_device()
            print(self.devices)
        except Exception as e:
            print(f"Error: {e}")

    def do_set_device_config(self, args):
        args_list = args.split()
        if len(args_list) < 3:
            print("Usage: set_device_config DEVICE_ID CODE PARAM")
            return
        device_id = args_list[0]
        iot_type = 3  # Assuming IoT type 3 for Meari IoT SDK-style
        code = int(args_list[1])
        param = args_list[2]

        p = {str(code): param}

        try:
            result = self.client.set_device_config(None, device_id, iot_type, p)
            print(f"Configuration set successfully: {result}")
        except Exception as e:
            print(f"Error setting configuration: {e}")

    def do_hello(self, line):
        """Print a greeting."""
        print("Hello, World!")

    def do_quit(self, line):
        """Exit the CLI."""
        if self.mqtt_thread is not None:
            self.mqtt_thread.join()
        # self.client.mqtt_client._thread.join()
        # self.client.meari_mqtt_client._thread.join()
        return True

    def postcmd(self, stop, line):
        print()
        return stop


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='MeariCLI Command Line Interface')
    # parser.add_argument('-connect', nargs=2, metavar=('user', 'password'), help='Connect with user and password')
    # args = parser.parse_args()
    # if args.connect:
    #     user, password = args.connect
    #     print(f"Connecting with user: {user} and password: {password}")

    MeariCLI().cmdloop()
