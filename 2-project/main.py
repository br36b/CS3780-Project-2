# CS3780
# Name: Bryan Rojas
# Date: 11/8/2021
# Purpose: Experiment with storage and cracking of passwords

import random

from crypt_manager import generate_hashed_key, is_correct_password

from input_functions import *
from constants import *
from file_functions import *


# Display menu of options
def print_menu() -> ():
    print('''
    Would you like to:
        1) Create an account
        2) Authenticate
        3) Generate random accounts
        0) Exit
    ''')


# Function to get all lines from a file stored as an array
# To be used to read key file and username/password text pairs
# returns array with lines
def file_lines_to_users(filename: str) -> []:
    try:
        with open(filename, "r") as file:
            # 'readlines()' returns a list containing each line in the file as a list item
            return [user.strip().split(":") for user in file.readlines()]

    except IOError:
        print("FLTA: File was unable to be opened for writing")

    # In the case of an error just return empty array
    return []


# Re-usable format string for data construction of username:password
def user_data_format(username: str, *args) -> str:
    base_string = username

    # Unpack tuple containing (password_key, salt)
    for arg in args:
        # Prevent empty/default salt from being output into array structure
        if not arg == b"":
            base_string += ":"

            # Double check everything is decoded to avoid concatenation errors
            if isinstance(arg, bytes):
                base_string += arg.decode()
            else:
                base_string += arg

    return base_string


# Function to prevent duplicate usernames in files
def check_if_user_exists(username: str) -> bool:
    plain_users = file_lines_to_users(PLAIN_TEXT_FILENAME)
    hashed_users = file_lines_to_users(HASH_TEXT_FILENAME)
    salt_hash_users = file_lines_to_users(HASH_SALT_TEXT_FILENAME)

    user_data = [plain_users, hashed_users, salt_hash_users]
    user_data_strings = ["Plain-text", "Hashed", "Salt+Hashed"]

    for data in user_data:

        # Empty array, no matches
        if not data:
            return False

        # Username | Key | Salt
        for user in data:
            # return once a matching username is found
            if user[0] == username:
                return True

    return False

# Function to generate the files requested
    # A plaintext username password pair, stored in text in a file
    # A username and a hashed password, stored in some format in the file
    # A username, a salt and the result of the hashed (password + salt), stored in some format in the file
# Will send output directly to files and return
def generate_files(username: str, password: str) -> ():
    # print("\nUsername:", username, "Password:", password)
    # Convert to bytes for crypt functions
    byte_password = password.encode()

    # Key will just be stored in file, not really secure but simplicity
    # If empty then it assumes that you want to start over with no previous data
    # New key will be generated and stored for future usages so long as it's not overwritten/deleted
    hash_password = generate_hashed_key(password=byte_password, is_salted=False)
    salt_hash_password = generate_hashed_key(password=byte_password, is_salted=True)
    # hash_password2 = generate_hashed_key(password=byte_password, is_salted=False)

    # Print statement for test outputs
    # print("""
    # Password
    # Plain-text: {}
    # Hashed: {}
    # Hash + Salt: {}
    # """.format(password, hash_password, salt_hash_password))

    write_to_file(PLAIN_TEXT_FILENAME, user_data_format(username, password))
    write_to_file(HASH_TEXT_FILENAME, user_data_format(username, *hash_password))
    write_to_file(HASH_SALT_TEXT_FILENAME, user_data_format(username, *salt_hash_password))

    print("Account for", username, "successfully created")


# Sign-up function
def create_account() -> ():
    print("\nYou have chosen to create an account.")

    username = validate_username()
    password = validate_password()

    # Make sure username doesn't already have an entry
    if not check_if_user_exists(username):
        generate_files(username, password)
    else:
        print("Error: Account could not be created. Reason: Username is taken.")


def authenticate_account() -> ():
    print("\nYou have chosen to authenticate your account.")

    # Reusing creation functions, same behavior
    # Makes sure username and password rules are followed before proceeding
    username = validate_username()
    password = validate_password()

    # Fetch an array version of all
    plain_users = file_lines_to_users(PLAIN_TEXT_FILENAME)
    hashed_users = file_lines_to_users(HASH_TEXT_FILENAME)
    salt_hash_users = file_lines_to_users(HASH_SALT_TEXT_FILENAME)

    user_data = [plain_users, hashed_users, salt_hash_users]
    user_data_strings = ["Plain-text", "Hashed", "Salt+Hashed"]

    count = 0
    for data in user_data:
        is_found = False

        # Empty array meaning data failed to be compiled
        if not data:
            print("Auth Error: There were missing data files for {}.".format(user_data_strings[count]))
            return

        # Arrays constructed with formatted data
        # Username | Key | Salt
        # To reduce code length, each type of file will be iterated here
        for user in data:
            # Count variable used to modify password verification for each file type
            # Once a matching username is found
            if user[0] == username:
                # Plain-text
                if count == 0:
                    is_found = user[1] == password
                # Hashed
                elif count == 1:
                    is_found = is_correct_password(password, user[1])
                # Salt + Hash
                elif count == 2:
                    is_found = is_correct_password(password, user[1], provided_salt=user[2])

        # Output if a login was matched or not
        if is_found:
            print("{}: Account was found. Login successful.".format(user_data_strings[count]))
        else:
            print("{}: No account was found with that information.".format(user_data_strings[count]))

        # Increment count to allow hash/hash+salt
        count += 1


def generate_random_accounts() -> ():
    print("Generate Random Accounts")


# Main Loop
def main() -> ():
    is_running = True

    while is_running:
        # Prompt for user option, 1-3
        print_menu()
        menu_option = get_valid_integer("Please select a menu option", 0, 3)

        if menu_option == 1:  # Option 1 is to create an account
            create_account()
        elif menu_option == 2:  # Option 2 is to authenticate an account
            authenticate_account()
        elif menu_option == 3:
            generate_random_accounts()
        elif menu_option == 0:  # Option 0 is to exit
            print("Exiting...")
            is_running = False
        else:  # Input for menu should be locked and this line should not be reached
            print("Error with menu options. Exiting.")
            is_running = False


# Init function
if __name__ == '__main__':
    main()
