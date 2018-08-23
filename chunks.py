from struct import Struct
from struct import error as struct_error

from .namedstruct import NamedStruct


chunk = Struct('<4si')


def chunks(data, overrides = {}):
    """
    generator giving all off the IFF chunks in a buffer
    does not handle bad input :(
    """
    counter, filesize = 0, len(data)
    last = None
    while counter < filesize:
        try:
            magic, size = chunk.unpack_from(data, counter)
        except struct_error as e:
            print('failed loading chunk from', data[:counter])
            print('last chunk:', last)
            raise e

        counter += chunk.size
        contents = data[counter:counter+size]

        if magic[3] != 0x4D:
            raise Exception('bad magic', magic, 'last chunk:', last)

        if magic in overrides:
            size = overrides[magic]

        yield magic, size, contents
        counter += size

        last = (magic, size, contents)

def parse(data, cnkformat):
    result = {}
    for id, size, data in chunks(data):
        magic_as_str = id[::-1].decode()

        if magic_as_str in cnkformat:
            strukt = NamedStruct(cnkformat[magic_as_str], f'{magic_as_str}_struct')

            if len(data) % strukt.size():
                raise Exception(f'len(data) ({len(data)}) not even multiple of strukt.size() ({strukt.size()})')

            recsize = strukt.size()

            count = len(data) // recsize
            records = []
            for i in range(count):
                records.append(strukt.unpack(data[(i * recsize):(i * recsize) + recsize]))

            result[magic_as_str] = records

        else:
            result[magic_as_str] = data.split(b'\000')

    return result


def makechunk(cc, data):
    assert type(cc) == str
    assert type(data) == str
    return cc + str( len(data) ) + data