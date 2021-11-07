# Recommended implementation from documentation page
# https://cryptography.io/en/latest/hazmat/primitives/key-derivation-functions/?highlight=pbkdf2#pbkdf2
import base64
import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidKey

from constants import SALT_LENGTH, HASH_LENGTH, HASH_ITERATIONS


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
        length=HASH_LENGTH,
        salt=crypt_salt,
        iterations=HASH_ITERATIONS,
    )

    encoded_key = base64.urlsafe_b64encode(kdf.derive(password))
    encoded_salt = crypt_salt

    data = (encoded_key, encoded_salt)
    return data


# Function that will reverse a hash/salt to verify password match
def is_correct_password(password: str, key: str, provided_salt: str = ""):
    # All operations must be done with byte string
    password = password.encode()

    # Key has to be sent to bytes, and then decoded from base64 operation performed earlier
    key = key.encode()
    key = base64.urlsafe_b64decode(key)
    provided_salt = provided_salt.encode()

    # Generate a key using the same parameters as in generation
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=HASH_LENGTH,
        salt=provided_salt,
        iterations=HASH_ITERATIONS,
    )

    # verify does not actually produce an output, only raised exceptions
    # InvalidKey exception is used to make sure keys match, asserting on invalid login
    try:
        kdf.verify(password, key)

        # print("Password matches")
        return True
    except InvalidKey:
        # print("Password did not match")
        return False


# Salt manager to find and read salt when given
class SaltManager(object):
    def __init__(self, should_salt):
        self.is_salted = should_salt

    # Generate or fetch salt for given item
    def get_salt(self) -> bytes:
        # Only generate the salt if specified
        if self.is_salted:
            while True:
                try:
                    # Salt should be capped at 1 byte
                    salt = os.urandom(SALT_LENGTH)
                    temp = salt.decode()

                    # For file storage don't allow blank spaces
                    # NOTE: For previous version of any char salt
                    if not salt.isspace():
                        return salt

                except UnicodeDecodeError:
                    # Error occurs because os.urandom is able to produce non-ascii chars
                    # Retry salt until valid one can be used
                    pass

        # If no salt was configured, just use an empty byte string
        return "".encode()
