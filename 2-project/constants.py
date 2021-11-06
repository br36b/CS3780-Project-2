from string import ascii_lowercase
# Constants
SALT_LENGTH = 1
HASH_LENGTH = 32
HASH_ITERATIONS = 1

SALT_CHARS = list(ascii_lowercase)
SALT_CHARS.extend([str(num) for num in range(0, 10)])

# Output file names
PLAIN_TEXT_FILENAME = "users/data.txt"
HASH_TEXT_FILENAME = "users/data.hash"
HASH_SALT_TEXT_FILENAME = "users/data.hasalt"

# Default values for length requirements
MIN_USERNAME_SIZE = 1
MAX_USERNAME_SIZE = 10

MIN_PASSWORD_SIZE = 1
MAX_PASSWORD_SIZE = 10
