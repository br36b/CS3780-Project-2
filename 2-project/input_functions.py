# Input functions

from constants import *


def get_valid_integer(prompt: str, lower_bound: int, upper_bound: int) -> int:
    """
    Function to get a valid int within specified range
    Will be INCLUSIVE of both bounds
    returns validated int
    """
    # Print out passed prompt
    print(prompt)

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


# Get input, validate for pos ints
# returns integer for usage in given process
def get_valid_size() -> int:
    invalid_number = True
    response = -1

    # Loop until user gives valid input
    while invalid_number:
        try:
            # Int cast will force error if non-int chars
            response = int(input("Please enter a positive integer: "))

            # Must be positive
            if response < 1:
                print("Please enter a number 1 or greater.")
            else:
                invalid_number = False
        # Covers any alpha/symbol
        except ValueError:
            print("Input was not a positive integer. Try again.")

    # Return response only after it is valid
    return response


def validate_username(min_username_size: int = MIN_USERNAME_SIZE, max_username_size: int = MAX_USERNAME_SIZE) -> str:
    """
    Function to create username
    Should consist of 10 alphabetic characters
    Returns username created in a string format
    """
    invalid_username = True
    response = ""

    while invalid_username:
        try:
            response = input("\nPlease enter an username with valid characters (Alphabet a-z): ")

            # Will be reset if any character does not match
            invalid_username = False  # Temporarily negate condition
            invalid_length = False

            # Check if wrong length, upper bound can be equal to
            if not(min_username_size <= len(response) <= max_username_size):
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


def validate_password(min_password_size: int = MIN_PASSWORD_SIZE, max_password_size: int = MAX_PASSWORD_SIZE) -> str:
    """
    Function to create password
    Only numbers 0-9 should be used to make cracking easier
    Returns password created in a string format
    """
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
            if not(min_password_size <= len(response) <= max_password_size):
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


def automated_validate_username(username: str, min_username_size: int = MIN_USERNAME_SIZE, max_username_size: int = MAX_USERNAME_SIZE) -> str:
    """
    Function to create username from automated data
    Should consist of 10 alphabetic characters
    Returns username created in a string format, empty string returned for errors
    """
    invalid_username = True
    response = username

    try:
        # Check if wrong length, upper bound can be equal to
        if not(min_username_size <= len(response) <= max_username_size):
            print("Automated: Username is an invalid length."
                  " Must be within {} and {} for {}".format(min_username_size, max_username_size, username))

            return ""

        # If output contains non-alphabetic characters then print out a message to let user know
        if not response.isalpha():
            # For debugging it is easier to print this information out on offending data
            print("Automated: Invalid character found in username: {}", username)
            return ""

    # Just in-case, should convert everything
    except ValueError:
        # For debugging it is easier to print this information out on offending data
        print("Automated: Input mismatch. Username rejected: {}".format(username))
        return ""

    return response


def automated_validate_password(password: str, min_password_size: int = MIN_PASSWORD_SIZE,
                                max_password_size: int = MAX_PASSWORD_SIZE) -> str:
    """
    Function to create password in automation
    Only numbers 0-9 should be used to make cracking easier
    Returns password created in a string format, returns empty string on error
    """
    response = password

    # 0-9 array currently
    # Must be in string type because inputs will be processed in strings
    valid_characters = [str(x) for x in range(10)]

    try:
        # Check if wrong length
        if not(min_password_size <= len(response) <= max_password_size):
            print("Automated: Password is an invalid length")
            print("Automated: Must be within {} and {} for {}".format(min_password_size, max_password_size, password))
            return ""

        # Make sure all characters are valid
        for char in response:
            if char not in valid_characters:
                # Reset if it fails the match
                invalid_password = True

                # For debugging it is easier to print this information out on offending data
                print("Automated: Invalid character in password: {}".format(password))
                break

    # Just in-case, should convert everything
    except ValueError:
        # For debugging it is easier to print this information out on offending data
        print("Automated: Input mismatch. Password Rejected: {}".format(password))
        return ""

    return response
