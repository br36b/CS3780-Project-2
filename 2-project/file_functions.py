import os


def write_to_file(filename: str, data: str) -> ():
    """
    Function to write string to file
    To be used to write user data files, will create one if it doesn't exist
    Data should not be modified here, just written
    """
    try:
        path = os.path.dirname(filename)

        if not os.path.exists(path):
            os.mkdir(path)

        with open(filename, "a+") as file:
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
        # Hiding output since it is accounted for and handled as a return result
        # print("FLTA: File was unable to be opened for reading")

        # In the case of an error just return empty array
        return []
