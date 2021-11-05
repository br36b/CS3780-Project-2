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
        print("WF: File was unable to be opened for writing")


def file_lines_to_users(filename: str) -> []:
    """
    Function to get all lines from a file stored as an array
    To be used to read key file and username/password text pairs
    returns array with lines
    """
    try:
        with open(filename, "r") as file:
            # 'readlines()' returns a list containing each line in the file as a list item
            return [user.strip().split(":") for user in file.readlines()]

    except IOError:
        print("FLTA: File was unable to be opened for writing")

    # In the case of an error just return empty array
    return []
