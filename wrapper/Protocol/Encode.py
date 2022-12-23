def encodeUINT8(num: int):
    if (num.bit_length() > 8):
        return False
    else:
        return num.to_bytes(1, 'little')

def encodeUINT16(num: int):
    if (num.bit_length() > 16):
        return False
    else:
        return num.to_bytes(2, 'little')