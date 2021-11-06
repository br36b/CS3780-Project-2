# CS3780
# Name: Bryan Rojas
# Date: 11/8/2021
# Purpose: Experiment with cracking of passwords


import itertools
import timeit

from os.path import exists

from crypt_manager import generate_hashed_key, is_correct_password

from input_functions import *
from file_functions import *
# from string import


# Display menu of options
def print_menu() -> ():
    print('''
    Which file would you like to crack:
        1) Hashed file (.hash)
        2) Salt + Hash file (.hasalt)
        0) Exit
    ''')


def brute_force_guess(user_data: [], max_size: int, is_salted: bool):
    cracked_users = []

    # Passwords can only contain numbers 0-9, upper bound excluded in Python
    password_chars = "".join([str(x) for x in range(10)])

    is_cracked = False

    for user in user_data:
        pass_crack_start = timeit.default_timer()
        is_cracked = False
        # Must offset to support valid ranges [1, x]
        # Try every combination from 1 char to up the max given

        for size in range(1, max_size + 1):
            if is_cracked:
                break

            possible_passwords = itertools.product(password_chars, repeat=size)

            salt_index = 0
            for password in possible_passwords:
                current_password = "".join(password)

                # print(user, current_password)

                if is_salted:
                    if is_cracked:
                        break

                    for salt_char in SALT_CHARS:
                        salt = salt_char

                        if is_correct_password(current_password, user[1], salt):
                            pass_crack_end = timeit.default_timer()
                            time_to_crack = pass_crack_end - pass_crack_start
                            time_to_crack = round(time_to_crack, 5)

                            print("Username: {} | Brute-Password: {} | Brute-Salt: {}, Total Time to Crack: {} (s)"
                                  .format(user[0], current_password, salt, time_to_crack))

                            is_cracked = True
                            break
                else:
                    if is_correct_password(current_password, user[1]):
                        pass_crack_end = timeit.default_timer()
                        time_to_crack = pass_crack_end - pass_crack_start
                        time_to_crack = round(time_to_crack, 5)

                        print("Username: {} | Brute-Password: {} | Total Time to Crack: {} (s)"
                              .format(user[0], current_password, time_to_crack))

                        # print(user, current_password)
                        is_cracked = True
                        break

        else:
            continue


def crack_users(message: str, is_salted=False):
    print("{}".format(message))

    filename = HASH_TEXT_FILENAME

    if is_salted:
        filename = HASH_SALT_TEXT_FILENAME

    users = file_lines_to_users(filename)

    if not users:
        print("Error: Could not find any user data in: {}", filename)
        return

    print("\nPlease specify a max password size")
    print("Largest password size: ")
    password_max = get_valid_size()

    crack_all_time_start = timeit.default_timer()
    brute_force_guess(users, password_max, is_salted)
    crack_all_time_end = timeit.default_timer()

    total_crack_time = crack_all_time_end - crack_all_time_start
    total_crack_time = round(total_crack_time, 5)

    print("Execution time for entire file: {:f} (s)".format(total_crack_time))


def main():
    is_running = True

    while is_running:
        # Display options to user for action choice
        print_menu()
        menu_option = get_valid_integer("Please select a menu option", 0, 2)

        if menu_option == 1:  # Option 1 to crack hashed accounts
            crack_users("Cracking hashed file...")
        elif menu_option == 2:  # Option 2 to crack salt + hash accounts
            crack_users("Cracking salted + hashed file...", is_salted=True)
        elif menu_option == 0:  # Option 0 to exit the program
            print("Exiting...")
            is_running = False
        else:  # Input for menu should be locked and this line should not be reached
            print("Error with menu options. Exiting.")
            is_running = False


# Init function
if __name__ == '__main__':
    main()
