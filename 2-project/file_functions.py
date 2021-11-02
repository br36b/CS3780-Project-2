def write_bytes_to_file(filename: str, data: bytes) -> ():
    """
    Function to write to bytes
    To be used to store key
    Modifies file and returns
    """
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
            # Read bytes from file, binary
            return file.read()

    except IOError:
        print("File was unable to be opened for writing")


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
        print("File was unable to be opened for writing")



