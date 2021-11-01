# CS3780
# Name: Bryan Rojas
# Date: 11/8/2021
# Purpose: Experiment with storage and cracking of passwords

import random
# from typing import Boolean

# Constants


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
def create_username(min_username_size=1, max_username_size=10) -> str:
    invalid_username = True
    response = ""

    while invalid_username:
        try:
            response = input("\nPlease enter an username with valid characters (Alphabet a-z): ")

            # Will be reset if any character does not match
            invalid_username = False  # Temporarily negate condition
            invalid_length = False

            # Check if wrong length
            if not(min_username_size < len(response) < max_username_size):
                print("Username is an invalid length")
                print("Must be within {} and {}".format(min_username_size, max_username_size))
                invalid_length = True
                invalid_username = True

            # Iterate through every character to find any invalid chars
            if not response.isalpha():
                print("Invalid character found in username.")
                invalid_username = False
            else:
                # Username is only valid if it is a correct length and passes alphabet test
                invalid_username = False

        # Just in-case, should convert everything
        except ValueError:
            print("Input mismatch. Try Again.")

    return response


# Function to create password
# Only numbers 0-9 should be used to make cracking easier
def create_password(min_password_size=1, max_password_size=10) -> str:
    invalid_password = True
    response = ""

    # 0-9 array currently
    valid_characters = [x for x in range(10)]

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
            if not invalid_length:
                for char in response:
                    if char not in valid_characters:
                        invalid_password = True

                        print("Invalid character in password.")
                        break

        # Just in-case, should convert everything
        except ValueError:
            print("Input mismatch. Try Again.")

    return response


# Sign-up function
def create_account():
    print("\nYou have chosen to create an account.")

    username = create_username()
    password = create_password()

    print("Username:", username, "Password:", password)


def authenticate_account():
    print("\nYou have chosen to authenticate your account.")


# Main Loop
def main():
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
