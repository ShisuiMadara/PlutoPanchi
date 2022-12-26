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

def packetCRC(type_: int, payload: bytes) -> bytes:
    checksum = b'\x00'
    checksum = (checksum[0] ^ len(payload).to_bytes(1, 'little')[0]).to_bytes(1, 'little')
    checksum = (checksum[0] ^ type_.to_bytes(1, 'little')[0]).to_bytes(1, 'little')
    for i in payload:
        checksum = (checksum[0] ^ i).to_bytes(1, 'little')
    return checksum        

def encodePacket(type_: int, payload: bytes) -> bytes|bool:
    if (type_.bit_length() > 8):
        return False
    packet = bytes(b'')
    try:
        packet += b'M$<' + len(payload).to_bytes(1, 'little') + type_.to_bytes(1, 'little')
    except OverflowError:
        print ('Packet Type or Payload length cannot be stored in 1 byte') 
        return False
    packet += payload
    packet += payloadCRC(type_, payload)
    return packet

    
    