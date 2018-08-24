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

        if not magic_as_str in cnkformat:
            print(f'format for {magic_as_str} not specified')
            continue

        format_decl = cnkformat[magic_as_str]
        result[magic_as_str] = format_decl.unpack(data)

    return result


def makechunk(cc, data):
    assert type(cc) == str
    assert type(data) == str
    return cc + str( len(data) ) + data