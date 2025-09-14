import string
import random


def create_random_string(length: int = 8, only_letter: bool = False) -> str:
    """
    Generate a random string of specified length.

    :param length: Length of the random string.
    :param only_letter: Boolean to include only letter.
    :return: Randomly generated string.
    """
    chars = string.ascii_lowercase if only_letter else string.digits + string.ascii_lowercase
    return ''.join(random.choice(chars) for _ in range(length))
