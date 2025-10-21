from meari_sdk.meari_client import MeariClient
from const import KNOWN_PARTNERS, INTEGRATION_LANGUAGES
from meari_sdk.meari_mqtt_message_id import MeariMqttMessageId

import cmd
import threading

import meari_sdk.meari_commands


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
        country_code = INTEGRATION_LANGUAGES[lng_type]["country_code"]
        phone_code = INTEGRATION_LANGUAGES[lng_type]["phone_code"]
        phone_type = "a"

        try:
            self.client = MeariClient(country_code=country_code, phone_code=phone_code, phone_type=phone_type, lng_type=lng_type, partner=KNOWN_PARTNERS[partner])

            if (user_account == ''):
                print(f"Connecting to {partner} - restore session")
                self.login_data = self.client.load_login_data_from_file("./login_data.json")
            else:
                print(f"Connecting to {partner} with user: {user_account}")
                self.login_data = self.client.login(user_account.lower(), user_password)
            self.iot_info = self.client.fetch_iot_info()

            print(f"Connected to {partner} with user: {self.login_data.user_account}")

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
        """
        Prints the current user's login information.

        This command displays the login data currently loaded or retrieved during
        the last connection session. The information typically includes user account
        details such as username, authentication tokens, and session metadata.

        Usage:
            >> print_user_info
        """
        print(self.login_data)

    def do_fetch_iot_info(self, line):
        """
        Fetches IoT (Internet of Things) platform information for the current session.

        This command retrieves general information from the Meari IoT platform,
        including account linkage data, platform configuration, and available services.

        Example:
            >> fetch_iot_info

        Notes:
            - The method calls `self.client.fetch_iot_info()` from the Meari SDK.
            - The result typically contains information about cloud region, MQTT endpoints,
              and integration metadata.
        """
        try:
            self.iot_info = self.client.fetch_iot_info()
            print(self.iot_info)
        except Exception as e:
            print(f"Error: {e}")

    def do_get_devices(self, line):
        """
        Fetches the list of devices associated with the current user's account.

        This command retrieves all devices registered under the logged-in account
        (e.g., cameras, sensors, or smart devices linked to the Meari ecosystem).

        Example:
            >> get_devices

        Notes:
            - Uses `self.client.get_device()` to query the device list from the Meari API.
            - The result may include device identifiers, names, models, online status,
              and binding information.
        """
        try:
            self.devices = self.client.get_device()
            print(self.devices)
        except Exception as e:
            print(f"Error: {e}")

    def do_set_device_config(self, args):
        """
        Sets a configuration parameter on a specific IoT device.

        Args:
            - DEVICE_ID (str): Serial number of the device .
            - CODE (int): The configuration code to modify (depends on the device model and SDK specs).
            - PARAM (int): The new value to assign to the specified configuration code.

        Example:
            >> set_device_config 1234567890 1001 1

        Notes:
            - Uses IoT type 3 by default (Meari SDK convention).
            - The configuration parameters are passed as a dictionary where
              the key is the configuration code (as a string) and the value is the parameter.
        """
        args_list = args.split()
        if len(args_list) < 3:
            print("Usage: set_device_config DEVICE_ID CODE PARAM")
            return
        device_id = args_list[0]
        iot_type = 3  # Assuming IoT type 3 for Meari IoT SDK-style
        code = int(args_list[1]) if args_list[1].isdigit() else getattr(meari_sdk.meari_commands, args_list[1], None)
        param = args_list[2]

        p = {str(code): int(param)}

        try:
            result = self.client.set_device_config(None, device_id, iot_type, p)
            print(f"Configuration set successfully: {result}")
        except Exception as e:
            print(f"Error setting configuration: {e}")

    def do_get_device_config(self, args):
        """
        Retrieves a specific configuration parameter from a device.

        Args:
            - DEVICE_ID (str): Serial number of the device.
            - CODE (int): The configuration code to query.

        Example:
            >> get_device_config 1234567890 1001

        Notes:
            - Uses IoT type 3 by default (Meari SDK convention).
            - The command requests the current configuration value for the specified
              code and prints the response from the Meari API.
        """
        args_list = args.split()
        if len(args_list) < 2:
            print("Usage: get_device_config DEVICE_ID CODE")
            return
        device_id = args_list[0]
        iot_type = 3  # Assuming IoT type 3 for Meari IoT SDK-style
        code = int(args_list[1]) if args_list[1].isdigit() else getattr(meari_sdk.meari_commands, args_list[1], None)

        p = [str(code)]

        try:
            result = self.client.get_device_config(None, device_id, iot_type, p)
            print(f"Configuration get successfully: {result}")
        except Exception as e:
            print(f"Error getting configuration: {e}")

    def do_get_device_params(self, args):
        """
        Retrieves all available parameters and their current values for a given device.

        Args:
            - DEVICE_ID (str): The unique identifier of the device.

        Example:
            >> get_device_params 1234567890

        Notes:
            - Uses IoT type 3 by default (Meari SDK convention).
            - This command fetches a complete parameter list from the device,
              including status and configuration data.
        """
        args_list = args.split()
        if len(args_list) < 1:
            print("Usage: get_device_params DEVICE_ID")
            return
        device_id = args_list[0]
        iot_type = 3  # Assuming IoT type 3 for Meari IoT SDK-style

        try:
            result = self.client.get_device_params(None, device_id, iot_type)
            print(f"Configuration get successfully: {result}")
        except Exception as e:
            print(f"Error getting configuration: {e}")

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
