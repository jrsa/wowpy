from struct import Struct
from struct import error as struct_error


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

def makechunk(cc, data):
    assert type(cc) == str
    assert type(data) == str
    return cc + str( len(data) ) + data