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
