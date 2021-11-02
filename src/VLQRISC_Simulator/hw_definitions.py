

class NotARegister(Exception):
    pass


REGISTER_NAMES = ["$zero",
                  "$t0",
                  "$t1",
                  "$t2",
                  "$t3",
                  "$t4",
                  "$s0",
                  "$s1",
                  "$s2",
                  "$s3",
                  "$s4",
                  "$a0",
                  "$a1",
                  "$a2",
                  "$v0",
                  "$ra",
                  "$sp",
                  "$pc"]

MEMORY_SIZE = 2 ** 16  # 2^16 Bytes


def convert_reg_common_name_to_number(common_name: str):
    for i, name in enumerate(REGISTER_NAMES):
        if name == common_name:
            return i
    else:
        raise NotARegister(f"'{common_name}' is not a valid register")
