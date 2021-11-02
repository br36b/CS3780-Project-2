# CS3780
# Name: Bryan Rojas
# Date: 11/8/2021
# Purpose: Experiment with storage and cracking of passwords

import random

from cryptography.fernet import Fernet

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

# Input functions


# Function to get a valid int within specified range
# Will be INCLUSIVE of both bounds
# returns validated int
def get_valid_integer(prompt: str, lower_bound: int, upper_bound: int) -> int:
    # Print out passed prompt
    print("\n" + prompt)

    invalid_number = True
    response = -1

    while invalid_number:
        try:
            response = int(input("Please enter a number"
                                 " between {} and {} (Inclusive): ".format(lower_bound, upper_bound)))

            # Check to see if the number is within bounds
            if response < lower_bound:
                print("Please enter a number {} or greater.".format(lower_bound))
            elif response > upper_bound:
                print("Please enter a number lower or equal to {}.".format(upper_bound))
            # If it is then exit the loop
            else:
                invalid_number = False
        except ValueError:
            print("Input given was not an integer. Try again.")

    return response


# Function to create username
# Should consist of 10 alphabetic characters
# Returns username created in a string format
def create_username(min_username_size: int = 1, max_username_size: int = 10) -> str:
    invalid_username = True
    response = ""

    while invalid_username:
        try:
            response = input("\nPlease enter an username with valid characters (Alphabet a-z): ")

            # Will be reset if any character does not match
            invalid_username = False  # Temporarily negate condition
            invalid_length = False

            # Check if wrong length, upper bound can be equal to
            if not(min_username_size < len(response) <= max_username_size):
                print("Username is an invalid length."
                      " Must be within {} and {}".format(min_username_size, max_username_size))
                invalid_length = True

            # If output contains non-alphabetic characters then print out a message to let user know
            if not response.isalpha():
                print("Invalid character found in username.")

            # Username is only valid if it is a correct length and passes alphabet test
            invalid_username = False if response.isalpha() and not invalid_length else True

        # Just in-case, should convert everything
        except ValueError:
            print("Input mismatch. Try Again.")

    return response


# Function to create password
# Only numbers 0-9 should be used to make cracking easier
# Returns password created in a string format
def create_password(min_password_size: int = 1, max_password_size: int = 10) -> str:
    invalid_password = True
    response = ""

    # 0-9 array currently
    # Must be in string type because inputs will be processed in strings
    valid_characters = [str(x) for x in range(10)]

    while invalid_password:
        try:
            response = input("\nPlease enter a password with valid characters (Numbers 0-9): ")

            # Will be reset if any character does not match
            invalid_password = False  # Temporarily negate condition
            invalid_length = False  # Track if valid within given range or default

            # Check if wrong length
            if not(min_password_size < len(response) < max_password_size):
                print("Password is an invalid length")
                print("Must be within {} and {}".format(min_password_size, max_password_size))
                invalid_length = True
                invalid_password = True

            # Iterate through every character to find any invalid chars
            # Won't iterate if invalid length, avoids 0 char input
            if not invalid_length:
                for char in response:
                    if char not in valid_characters:
                        # Reset if it fails the match
                        invalid_password = True

                        print("Invalid character in password.")
                        break

        # Just in-case, should convert everything
        except ValueError:
            print("Input mismatch. Try Again.")

    return response


# Function to write string to file
# To be used to write user data files
# Data should not be modified here, just written
def write_to_file(filename: str, data: str) -> ():
    try:
        with open(filename, "a") as file:
            file.write("{}\n".format(data))

    except IOError:
        print("File was unable to be opened for writing")


# Function to write to bytes
# To be used to store key
# Modifies file and returns
def write_bytes_to_file(filename: str, data: bytes) -> ():
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
            # Should only have one line since key is generated that way
            return file.readline()

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
