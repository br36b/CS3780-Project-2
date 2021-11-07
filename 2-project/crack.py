# CS3780
# Name: Bryan Rojas
# Date: 11/8/2021
# Purpose: Experiment with cracking of passwords


import itertools
import timeit

from crypt_manager import is_correct_password

from input_functions import *
from file_functions import *
# from string import


average_of_length_time: list
count_of_password_size: list


# Display menu of options
def print_menu() -> ():
    print('''
    Which file would you like to crack:
        1) Hashed file (.hash)
        2) Salt + Hash file (.hasalt)
        0) Exit
    ''')


def brute_force_guess(user_data: [], max_size: int, is_salted: bool):
    # Store the total times for
    global average_of_length_time, count_of_password_size
    average_of_length_time = [0 for _ in range(max_size + 1)]
    count_of_password_size = [0 for _ in range(max_size + 1)]

    cracked_users: dict = {}

    # Passwords can only contain numbers 0-9, upper bound excluded in Python
    password_chars = "".join([str(x) for x in range(10)])

    # Go through each user and try every combination up to the max_size of characters
    for user in user_data:
        pass_crack_start = timeit.default_timer()
        is_cracked = False
        salt = ""

        # Must offset to support valid ranges [1, x]
        # Try every combination from 1 char to up the max given
        # Try each potential password length
        for size in range(1, max_size + 1):
            # Early exit when multiple loops are used
            if is_cracked:
                break

            # Stores an iteration tool that goes from 0 -> 9 ... 0000000->9999999
            # Expands with current password length in outer loop
            possible_passwords = itertools.product(password_chars, repeat=size)

            # Take a potential password from the iterator tool
            for password in possible_passwords:
                # Convert password from iterator tuple to string
                current_password = "".join(password)

                # print(user, current_password)

                # Only use configured salts if file is salted
                if is_salted:
                    try:
                        salt = user[2]
                    except IndexError:
                        print("Error: Missing salt for user")
                else:
                    if cracked_users:
                        for key, value in cracked_users.items():
                            if key == user[1]:
                                current_password = value
                                size = len(current_password)

                # Check if the combination is right
                # Store any time of storage
                if is_correct_password(current_password, user[1], salt):
                    pass_crack_end = timeit.default_timer()
                    time_to_crack = pass_crack_end - pass_crack_start
                    time_to_crack = round(time_to_crack, 6)

                    print("\nUsername: {} | Key: {} | Brute-Password: {} \n\t| Salt: {} "
                          "| Length: {} | Total Time to Crack: {:f} (s)"
                          .format(user[0], user[1], current_password, salt,
                                  len(current_password), time_to_crack))

                    # Store length of password and time
                    average_of_length_time[size] += time_to_crack
                    count_of_password_size[size] += 1

                    # Append cracked user for unsalted comparisons
                    cracked_users[user[1]] = current_password
                    # print(cracked_users)

                    is_cracked = True
                    break
        else:
            continue


# Initiate the password cracking process by getting relevant data
def crack_users(message: str, is_salted=False):
    print("{}".format(message))

    # Dynamically set filename based on salt var
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

    # Measure the time to crack all passwords
    crack_all_time_start = timeit.default_timer()
    brute_force_guess(users, password_max, is_salted)
    crack_all_time_end = timeit.default_timer()

    # Calculate final time it took to crack passwords
    total_crack_time = crack_all_time_end - crack_all_time_start
    total_crack_time = round(total_crack_time, 6)

    # print(average_of_length_time)
    # print(count_of_password_size)

    print("")

    # Output summary of time
    entry = 0
    while entry < len(count_of_password_size):
        # Print every entry and their averages
        # Entry == length, no offsets
        if not count_of_password_size[entry] == 0:
            average = round(average_of_length_time[entry] / count_of_password_size[entry], 6)
            print("Avg. Time of Size [{}]: {:f} (s)".format(entry, average))

        entry += 1

    print("\nExecution time for entire file: {:f} (s)".format(total_crack_time))


# Main Function
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
