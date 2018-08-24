
class StructArray:
    """
    for serialization of arrays of either struct.Struct or wow.namedstruct
    """
    def __init__(self, strukt):
        self.strukt = strukt

    def unpack(self, data):
        recsize = self.strukt.size
        count = len(data) // recsize
        records = []
        for i in range(count):
            records.append(self.strukt.unpack(data[(i * recsize):(i * recsize) + recsize]))

        return records
