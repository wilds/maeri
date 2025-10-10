import datetime


def get_timeout() -> str:
    """
    Returns a UTC timestamp (in seconds) representing the current time + 60 seconds,
    adjusted to remove local timezone and DST offsets.
    """

    local_time = datetime.datetime.now() + datetime.timedelta(seconds=60)

    offset = local_time.utcoffset()
    if offset is None:
        offset = datetime.timedelta()

    utc_time = local_time - offset
    utc_timestamp = int(utc_time.timestamp())
    return str(utc_timestamp)


def format_sn(sn: str) -> str:
    """
    Formats a serial number to match Meari IoT API requirements.

    - If the SN is empty or None, returns an empty string.
    - If the SN is 9 characters long, prepends '0000000'.
    - Otherwise, returns SN starting from the 5th character.
    """
    if not sn:
        return ""

    if len(sn) == 9:
        return "0000000" + sn
    else:
        return sn[4:]


def is_nvr_or_base_by_id(device_type_id: int) -> bool:
    return device_type_id in (11, 17)


def is_nvr_or_base(camera_info) -> bool:
    return camera_info is not None and is_nvr_or_base_by_id(camera_info.dev_type_id)


def is_low_power_device(camera_info) -> bool:
    """
    Determine whether the given camera device is a low-power device.

    Logic:
      - If the firmware version (ver) is >= 6:
          → The device is low power if it has PWM > 0 or its type ID == 6.
      - Otherwise (ver < 6):
          → The device is low power if its type ID is 4 or 5.
    """
    device_type_id = camera_info.dev_type_id

    if camera_info.ver >= 6:
        return camera_info.pwm > 0 or device_type_id == 6
    else:
        return device_type_id in (4, 5)


def is_iothub(info) -> bool:
    """
    Determine whether the given camera device is an IoT Hub.

    Logic:
      - If info is None → return True (same as the Java default case).
      - If device type ID == 6 → always True (explicit IoT Hub type).
      - Otherwise:
          * If protocol version >= 4:
              - If firmware version >= 15:
                  → Check the 'spp' value.
                     It's IoT Hub if spp == -1 OR the bitwise AND (spp & 2) == 2.
              - Else (ver < 15):
                  → IoT Hub if it's NOT a low power device.
          * If protocol version < 4:
              → Not an IoT Hub (False).
    """
    if info is None:
        return True

    is_low_power = is_low_power_device(info)

    if info.dev_type_id == 6:
        return True

    if info.protocol_version >= 4:
        if info.ver >= 15:
            spp = info.spp
            # bitwise check: 2 == (2 & spp)
            is_iothub = spp == -1 or (spp & 2) == 2
        else:
            is_iothub = not is_low_power
    else:
        is_iothub = False

    return is_iothub
