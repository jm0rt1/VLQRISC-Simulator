

def convert_int_bin_str(integer: int, width: int) -> str:
    """Convert integer to a binary string

    Args:
        integer (int): to convert
        width (int): width of binary number

    Returns:
        str: binary string
    """
    return bin(integer)[2:].zfill(width)


def int_to_sign_extended_bin_str(integer: int, width: int) -> str:
    """converts an integer to a sign extended binary string

    Args:
        integer (int): int to convert
        width (int): width of binary number

    Returns:
        str: signed binary string
    """
    if integer < 0:
        s = bin(integer & int("1"*width, 2))[2:]
        return ("{0:0>%s}" % (width)).format(s)
    else:
        return convert_int_bin_str(integer, width)


def twos_complement_of_bin_str(string: str):
    """
    Found at:
    https://www.geeksforgeeks.org/efficient-method-2s-complement-binary-string/
    -- changed some variable names
    """
    length = len(string)

    # Traverse the string to get first
    # '1' from the last of string
    i = length - 1
    while(i >= 0):
        if (string[i] == '1'):
            break

        i -= 1

    # If there exists no '1' concatenate 1
    # at the starting of string
    if (i == -1):
        return '1'+string

    # Continue traversal after the
    # position of first '1'
    k = i - 1
    while(k >= 0):

        # Just flip the values
        if (string[k] == '1'):
            string_list = list(string)
            string_list[k] = '0'
            string = ''.join(string_list)
        else:
            string_list = list(string)
            string_list[k] = '1'
            string = ''.join(string_list)

        k -= 1

    # return the modified string
    return string


def signed_bin_str_to_int(string: str) -> int:
    """convert a signed binary string to an integer

    Args:
        string (str): binary string to convert

    Returns:
        int: signed integer
    """
    if string[0] == "1":
        # negative
        twos_comp_str = twos_complement_of_bin_str(string)

        return -int(twos_comp_str, 2)

    else:
        # positive
        return int(string, 2)

def unsigned_bin_str_to_int(string:str)->int:

    # positive
    return int(string, 2)


def int_twos_complement(integer: int, n: int):
    """compute the 2's complement of int value val"""
    if (integer & (1 << (n - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
        integer = integer - (1 << n)        # compute negative value
    return integer                         # return positive value as is
