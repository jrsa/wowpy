

class StringBlockResult:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"<StringBlock:{len(self.data.split(b'/x000'))} entries>"

    def get(self, offs):
        try:
            return getstring(self.data, offs)
        except IndexError:
            print(f"offset out of range {offs}")

    def as_array(self):
        return self.data.split(b'\x00')


class StringBlock:
    def unpack(self, data):
        return StringBlockResult(data)

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
