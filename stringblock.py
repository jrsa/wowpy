

def getstring(data, ofs):
    """
    from a bytes containing null-terminated strings,
    returns one string given its offset in the block
    """
    i = ofs
    dst = ''
    while data[i] != 0:
        dst += chr(data[i])
        i += 1
    return dst
