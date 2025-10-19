
import hashlib
import hmac
import base64
from Crypto.Cipher import AES, DES
from Crypto.Util.Padding import pad, unpad

from .const import DES_ENCODE_A, DES_ENCODE_B


def md5_32(input_str: str) -> str:
    return hashlib.md5(input_str.encode()).hexdigest()


def get_signature(data: str, secret: str) -> str:
    return base64.b64encode(hmac.new(secret.encode(), data.encode(), hashlib.sha1).digest()).decode()


def encode_param(param: str, api: str, timestamp: int, partner_id: str) -> str:
    key = base64.b64encode(f"{api}{partner_id}a{timestamp}".encode()).decode()[:16]
    cipher = AES.new(key.encode(), AES.MODE_CBC,  key.encode())
    encrypted = base64.b64encode(cipher.encrypt(pad(param.encode(), AES.block_size))).decode()
    return encrypted


def decode_param(param: str, api: str, timestamp: int, partner_id: str) -> str:
    key = base64.b64encode(f"{api}{partner_id}a{timestamp}".encode()).decode()[:16]
    cipher = AES.new(key.encode(), AES.MODE_CBC, key.encode())
    decrypted = unpad(cipher.decrypt(base64.b64decode(param)), AES.block_size).decode()
    return decrypted


def get_a() -> str:
    return base64.b64decode(DES_ENCODE_A).decode('utf-8')


def get_b() -> str:
    return base64.b64decode(DES_ENCODE_B).decode('utf-8')


def des_utils_encode(str_value: str) -> str:
    return des_utils_encode_with_params(get_a(), get_b(), str_value)


def des_utils_encode_with_params(str_value: str, str2: str, str3: str) -> str:
    secret_key = str_value.encode('utf-8')
    iv = str2.encode('utf-8')
    cipher = DES.new(secret_key[:8], DES.MODE_CBC, iv)
    padded_text = pad(str3.encode('utf-8'), DES.block_size)
    encrypted_text = cipher.encrypt(padded_text)
    return base64.b64encode(encrypted_text).decode('utf-8')


def decode_device_token(key: str, encrypted_str: str, decode_base64: bool) -> str:
    if not key or len(key) < 16 or not encrypted_str:
        return None

    try:
        decoded_bytes = base64.b64decode(encrypted_str)
        key_iv = key[:16].encode('utf-8')
        cipher = AES.new(key_iv, AES.MODE_CBC, key_iv)
        decrypted_bytes = cipher.decrypt(decoded_bytes)
        decrypted_bytes = unpad(decrypted_bytes, AES.block_size)

        if decode_base64:
            decrypted_bytes = base64.b64decode(decrypted_bytes)

        result = decrypted_bytes.decode('utf-8')
        return result

    except Exception as e:
        print(f"decodeDeviceToken error: {str(e)}")
        return None


def decode_img(image_data: bytes, device_sn: str) -> bytes:
    key = device_sn[4:20] if len(device_sn) >= 20 else (device_sn[4:] + '0' * (16 - len(device_sn[4:])))

    if len(image_data) <= 1024:
        return decrypt(key, image_data)

    decrypted_data = decrypt(key, image_data, 0, 1024)
    if decrypted_data is None:
        return None

    remaining_data = image_data[1024:]
    result_data = decrypted_data + remaining_data

    return result_data


def decrypt(key: str, encrypted: bytes, offset: int = 0, length: int = None) -> bytes:
    try:
        zero_iv = b'0000000000000000'
        raw = key.encode('UTF-8')
        cipher = AES.new(raw, AES.MODE_CBC, zero_iv)

        if length is not None:
            encrypted = encrypted[offset:offset+length]

        decrypted = cipher.decrypt(encrypted)
        return unpad(decrypted, AES.block_size)
    except Exception as e:
        print(e)
        return


def decrypt_string(key: str, encrypted: str) -> str:
    if not encrypted:
        return encrypted
    try:
        enc = base64.b64decode(encrypted.encode('UTF-8'))
        result = decrypt(key, enc)
        return result.decode('UTF-8')
    except Exception as e:
        print(e)
        return None


"""
def handle_encoded_image(image_url: str, image_data: bytes, device_sn: str, passwords_set: Set[str]) -> Tuple[bytes, bool]:
    decoded_data = image_data
    success = True

    if ".jpgx1" in image_url:
        decoded_data = decode_img(image_data, device_sn)
        success = True
    elif ".jpgx2" in image_url:
        success = False
        try:
            filename = image_url[:image_url.index(".jpg") + 4].split("/")[-1]
            if not passwords_set:
                passwords_set = set()

            data = MMKVUtil.getData(MMKVUtil.DEVICE_VIDEO_PASSWORD + device_sn)
            if data:
                passwords_set.add(data)

            for password in passwords_set:
                if password:
                    success = MeariMediaUtil.decodePic(filename, password, image_data) == 0
                    if success:
                        break

            if not success:
                logging.error("jpgx2 --- v1 ... ERR! key err!")
        except Exception as e:
            logging.error(f"jpgx2 --- v1 ... ERR! {e}")
    elif ".jpgx3" in image_url:
        success = False
        try:
            filename = image_url[:image_url.index(".jpg") + 4].split("/")[-1]
            formatted_license_id = format_license_id(device_sn)
            if formatted_license_id:
                success = MeariMediaUtil.decodePic(filename, formatted_license_id, image_data) == 0

            if not success:
                logging.error("jpgx3 --- v2 ... ERR! key err!")
        except Exception as e:
            logging.error(f"jpgx3 --- v2 ... ERR! {e}")

    return decoded_data,
"""
