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
            # Use old format for gdb online
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


def get_username() -> str:
    invalid_username = True
    response = ""

    while invalid_username:
        try:
            # Use old format for gdb online
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


# Sign-up function
def user_signup():
    print("You have chosen to create an account.")

    print("\nPlease")

# Main Loop
def main():
    # Prompt for user option, 1-3
    print_menu()
    menu_option = get_valid_integer("Please select a menu optio", 1, 3)

# Init function
if __name__ == '__main__':
    main()
