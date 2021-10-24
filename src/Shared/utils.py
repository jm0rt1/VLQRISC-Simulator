

def convert_int_bin_str(integer: int, width: int):

    return bin(integer)[2:].zfill(width)
