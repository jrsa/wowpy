from zlib import adler32


class StringPool:

    """
    stores strings from the records in a contiguous block,
    separated by null terminators. provides the offset.
    if an already extant string is pushed in, the offset to
    the existing version is given and a new copy is NOT stored.
    """

    def __init__(self):
        self.block = bytearray()
        self.table = dict()

    def lookup(self, string):

        hshstr = adler32(string)

        try:
            offset = self.table[hshstr]
        except KeyError as e:
            offset = len(self.block)
            self.block.extend(string.encode("utf-8"))
            self.block.append('\x00')
            self.table[hshstr] = offset

        return offset
