from struct import Struct


chunk = Struct('<4si')


def chunks(data):
    """
    generator giving all off the IFF chunks in a buffer
    does not handle bad input :(
    """
    counter, filesize = 0, len(data)
    while counter < filesize:
        magic, size = chunk.unpack_from(data, counter)
        counter += chunk.size
        contents = data[counter:counter+size]
        if magic == b'RNCM':
            size = 448
        yield magic, size, contents
        counter += size

def makechunk(cc, data):
    assert type(cc) == str
    assert type(data) == str
    return cc + str( len(data) ) + data