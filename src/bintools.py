def in_situ_ebcdic_to_ascii(s):
    etoa = (
        "                                "
        "                                "
        "           .<(+|&         !$*); "
        "-/         ,%_>?         `:#@'=\""
        " abcdefghi       jklmnopqr      "
        "  stuvwxyz                      "
        " ABCDEFGHI       JKLMNOPQR      "
        "  STUVWXYZ      0123456789      "
    )

    # Convert the input bytes to a mutable list of characters
    s_list = list(s)

    for i in range(len(s_list)):
        s_list[i] = etoa[s_list[i]]

    return ''.join(s_list)

def access_4bits(data, num):
    # access 4 bits from num-th position in data
    return bin(int(data, 2) >> num & 0b1111)

def read_raw(filename):
    return open(filename, "rb", buffering=0, ).read()
