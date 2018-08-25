from collections import namedtuple
from struct import Struct, calcsize


class NamedStruct():
    def __init__(self, decl, name='UnnamedStruct'):
        fmt = ''
        fields = []
        for field in decl:
            fmt += field[1]
            if field[0]:
                fields.append(field[0])
            else:
                fields.append(f'field_{calcsize(fmt)}')

        self.nt = namedtuple(name, fields)
        self.strukt = Struct(fmt)
        self.size = self.strukt.size

    def __repr__(self):
        return f'{self.strukt.__repr__()}: {self.nt._fields}'

    def unpack(self, data):
        return self.nt._make(self.strukt.unpack(data))

    def pack(self, *s):
        return self.strukt.pack(*s)

    def unpack_from(self, data, offset):
        return self.nt._make(self.strukt.unpack_from(data, offset))
