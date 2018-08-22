from collections import namedtuple
from struct import Struct


class NamedStruct():
    def __init__(self, decl, name='UnnamedStruct'):
        fmt = ''
        fields = []
        for field in decl:
            fmt += field[1]
            fields.append(field[0])

        self.nt = namedtuple(name, fields)
        self.strukt = Struct(fmt)

    def unpack(self, data):
        return self.nt._make(self.strukt.unpack(data))

    def pack(self, s):
        return self.strukt.pack(s)
