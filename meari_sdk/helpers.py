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