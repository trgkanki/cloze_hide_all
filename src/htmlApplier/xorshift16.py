# xorshift based counter
# This generates 65535-period series


def xorshift16Step(x: int):
    x = (x ^ (x << 7)) & 0xFFFF
    x = (x ^ (x >> 9)) & 0xFFFF
    x = (x ^ (x << 8)) & 0xFFFF
    return x
