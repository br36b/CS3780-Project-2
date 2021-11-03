# Recommended implementation from documentation page
import os
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from file_functions import write_bytes_to_file, read_bytes_from_file
from constants import *


# Function that will generate a hashed version of passed string
def generate_hashed_key(password, is_salted=False):
    # Get salt if option is passed
    salt = SaltManager(is_salted)

    crypt_salt = salt.get_salt()

    # class cryptography.hazmat.primitives.kdf.pbkdf2.PBKDF2HMAC(
    # algorithm, length, salt,
    # iterations, backend=None)
    # Salt can be empty if is_salted == False
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=16,
        salt=crypt_salt,
        iterations=1000,
    )

    encoded_key = base64.urlsafe_b64encode(kdf.derive(password))
    encoded_salt = crypt_salt

    decoded_keys = (encoded_key, encoded_salt)
    return decoded_keys


# Salt manager to find and read salt when given
class SaltManager(object):
    def __init__(self, should_salt, path=SALT_FILE):
        self.is_salted = should_salt
        self.path = path

    # Generate or fetch salt for given item
    def get_salt(self) -> bytes:
        if self.is_salted:
            # Salt should be capped at 1 byte
            return os.urandom(1)

        # If no salt was configured, just use an empty byte string
        return "".encode()
