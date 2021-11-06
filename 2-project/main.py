# CS3780
# Name: Bryan Rojas
# Date: 11/8/2021
# Purpose: Experiment with storage and authentication of passwords

import random
import itertools

from crypt_manager import generate_hashed_key, is_correct_password
from string import ascii_lowercase

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

    # Use compiled data to check for users
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

    # Output user data into a file
    write_to_file(PLAIN_TEXT_FILENAME, user_data_format(username, password))
    write_to_file(HASH_TEXT_FILENAME, user_data_format(username, *hash_password))
    write_to_file(HASH_SALT_TEXT_FILENAME, user_data_format(username, *salt_hash_password))

    print("Account for", username, "successfully created")


# Sign-up function
def create_account(is_automated: bool = False, username: str = "", password: str = "",
                   min_password_size: int = MIN_PASSWORD_SIZE, max_password_size: int = MAX_PASSWORD_SIZE) -> ():
    print("\nYou have chosen to create an account.")

    # If user should input, then use previously built methods
    if not is_automated:
        username = validate_username()
        password = validate_password()
    # For mass generation, use different function, since no chance to automate prompts without os.system
    else:
        username = automated_validate_username(username)
        password = automated_validate_password(password, min_password_size, max_password_size)

    # Make sure username doesn't already have an entry
    if not check_if_user_exists(username):
        generate_files(username, password)
    else:
        print("Error: Account could not be created. Reason: Username is taken.")


# Function to verify a match between input user and password
# This is only for manual input
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


# Generate many accounts based on user input
def generate_random_accounts() -> ():
    print("Generating Random Accounts")

    print("\nPlease specify password size")

    # Get password sizes from a range of numbers
    print("Shortest bound size: ")
    lower_bound = get_valid_size()

    print("Largest bound size: ")
    upper_bound = get_valid_size()

    # Re-order them if they were inputted in the wrong order
    password_min = min(lower_bound, upper_bound)
    password_max = max(lower_bound, upper_bound)

    # Get the number of accounts wanted
    print("\nPlease enter the number of accounts desired")
    number_of_accounts = get_valid_size()

    # 10 char account example from spec sheet
    # itertools used to keep the letters wrapping around
    # Error should only occur if massive massive number is input
    # Credit to https://stackoverflow.com/questions/37956212/incrementing-string-in-python for iterable format
    account_prefix = "usr"
    account_suffix = itertools.cycle(itertools.product(*[ascii_lowercase]*7))
    account_username = account_prefix + "".join(next(account_suffix, "Out of letters"))

    password_chars = [str(x) for x in range(0, 10)]

    # Randomize a password and get the next available account
    for account in range(number_of_accounts):
        # Make sure account is unique before trying to use username
        while check_if_user_exists(account_username):
            # Up to ten chars for usernames, but must offset for prefix
            # Change from 'aaz' to 'aza' and so on
            account_username = account_prefix + "".join(next(account_suffix, "Out of letters"))

        # Get a length for this password
        password_length = random.randint(password_min, password_max)
        account_password = ""

        # Randomize password by picking out chars
        for x in range(password_length):
            account_password += random.choice(password_chars)

        if account_username and account_password:
            create_account(is_automated=True, username=account_username, password=account_password,
                           min_password_size=password_min, max_password_size=password_max)
        else:
            print("Generator: Unable to generate valid account data")


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
