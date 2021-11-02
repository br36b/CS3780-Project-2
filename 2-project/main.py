# CS3780
# Name: Bryan Rojas
# Date: 11/8/2021
# Purpose: Experiment with storage and cracking of passwords

import random

from cryptography.fernet import Fernet

from input_functions import *

# Constants
SALT_LENGTH = 1

CRYPT_KEY = ""

KEY_FILENAME = "crypt.key"
PLAIN_TEXT_FILENAME = "data.txt"
HASH_TEXT_FILENAME = "data.hash"
HASH_SALT_TEXT_FILENAME = "data.hasalt"


# Display menu of options
def print_menu() -> ():
    print('''\n
    Would you like to:
    1) Create an account
    2) Authenticate
    3) Exit
    ''')


def write_to_file(filename: str, data: str) -> ():
    """
    Function to write string to file
    To be used to write user data files
    Data should not be modified here, just written
    """
    try:
        with open(filename, "a") as file:
            file.write("{}\n".format(data))

    except IOError:
        print("File was unable to be opened for writing")


def write_bytes_to_file(filename: str, data: bytes) -> ():
    """
    Function to write to bytes
    To be used to store key
    Modifies file and returns
    """
    try:
        with open(filename, "wb") as file:
            file.write(data)

    except IOError:
        print("File was unable to be opened for writing")


# Get bytes from a key file that will be used
# return bytes from the file
def read_bytes_from_file(filename: str) -> bytes:
    try:
        with open(filename, "rb") as file:
            # Read bytes from file, binary
            return file.read()

    except IOError:
        print("File was unable to be opened for writing")


# Function to get all lines from a file stored as an array
# To be used to read key file and username/password text pairs
# returns array with lines
def file_lines_to_array(filename: str) -> []:
    try:
        with open(filename, "r") as file:
            # 'readlines()' returns a list containing each line in the file as a list item
            return file.readlines()

    except IOError:
        print("File was unable to be opened for writing")

    # In the case of an error just return empty array
    return []


# Function to generate the files requested
    # A plaintext username password pair, stored in text in a file
    # A username and a hashed password, stored in some format in the file
    # A username, a salt and the result of the hashed (password + salt), stored in some format in the file
# Will send output directly to files and return
def generate_files(username: str, password: str) -> ():
    print("\nUsername:", username, "Password:", password)

    temp_key = read_bytes_from_file(KEY_FILENAME)

    # Key will just be stored in file, not really secure but simplicity
    # If empty then it assumes that you want to start over with no previous data
    # New key will be generated and stored for future usages so long as it's not overwritten/deleted
    if not temp_key:
        temp_key = Fernet.generate_key()
        write_bytes_to_file(filename=KEY_FILENAME, data=temp_key)

    # Python requires global variable be explicitly set
    # Otherwise a key was already in the file and we should just use it
    global CRYPT_KEY
    CRYPT_KEY = temp_key








# Sign-up function
def create_account() -> ():
    print("\nYou have chosen to create an account.")

    username = create_username()
    password = create_password()

    generate_files(username, password)


def authenticate_account() -> ():
    print("\nYou have chosen to authenticate your account.")


# Main Loop
def main() -> ():
    # Prompt for user option, 1-3
    print_menu()
    menu_option = get_valid_integer("Please select a menu option", 1, 3)

    if menu_option == 1:  # Option 1 is to create an account
        create_account()
    elif menu_option == 2:  # Option 2 is to authenticate an account
        authenticate_account()
    elif menu_option == 3:  # Option 3 is to exit
        print("Exiting...")
    else:  # Input for menu should be locked and this line should not be reached
        print("Error with menu options. Exiting.")


# Init function
if __name__ == '__main__':
    main()
