# CS3780
# Name: Bryan Rojas
# Date: 11/8/2021
# Purpose: Experiment with storage and cracking of passwords

import random

from cryptography.fernet import Fernet

from crypt_manager import generate_hashed_key

from input_functions import *
from constants import *
from file_functions import *


# Display menu of options
def print_menu() -> ():
    print('''\n
    Would you like to:
    1) Create an account
    2) Authenticate
    3) Exit
    ''')


# Function to get all lines from a file stored as an array
# To be used to read key file and username/password text pairs
# returns array with lines
def file_lines_to_array(filename: str) -> []:
    try:
        with open(filename, "r") as file:
            # 'readlines()' returns a list containing each line in the file as a list item
            return file.readlines()

    except IOError:
        print("FLTA: File was unable to be opened for writing")

    # In the case of an error just return empty array
    return []


# Re-usable format string for data construction of username:password
def user_data_format(username: str, *args) -> str:
    base_string = username

    for arg in args:
        if not arg == b"":
            base_string += ":"

            # Double check everything is decoded
            if isinstance(arg, bytes):
                base_string += arg.decode()
            else:
                base_string += arg

    return base_string


# Function to generate the files requested
    # A plaintext username password pair, stored in text in a file
    # A username and a hashed password, stored in some format in the file
    # A username, a salt and the result of the hashed (password + salt), stored in some format in the file
# Will send output directly to files and return
def generate_files(username: str, password: str) -> ():
    print("\nUsername:", username, "Password:", password)
    # Convert to bytes for crypt functions
    byte_password = password.encode()

    # Key will just be stored in file, not really secure but simplicity
    # If empty then it assumes that you want to start over with no previous data
    # New key will be generated and stored for future usages so long as it's not overwritten/deleted
    hash_password = generate_hashed_key(password=byte_password, is_salted=False)
    salt_hash_password = generate_hashed_key(password=byte_password, is_salted=True)
    # hash_password2 = generate_hashed_key(password=byte_password, is_salted=False)

    print("""
    Password
    Plain-text: {}
    Hashed: {}
    Hash + Salt: {}
    """.format(password, hash_password, salt_hash_password))

    write_to_file(PLAIN_TEXT_FILENAME, user_data_format(username, password))
    write_to_file(HASH_TEXT_FILENAME, user_data_format(username, *hash_password))
    write_to_file(HASH_SALT_TEXT_FILENAME, user_data_format(username, *salt_hash_password))


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
