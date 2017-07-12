from struct import Struct


chunk = Struct('<4si')

"""
chunks which contain unidentified bytes (headerless) and
fuck up the loading
"""
badchunks = {b'RNCM': 13}


def chunks(data):
    """
    generator giving all off the IFF chunks in a buffer
    does not handle bad input :(
    """
    counter, filesize = 0, len(data)
    while counter < filesize:
        magic, size = chunk.unpack_from(data, counter)
        if magic in badchunks:
            counter += badchunks[magic] # seek past extra bytes
        counter += chunk.size
        contents = data[counter:counter+size]
        yield magic, size, contents
        counter += size


def makechunk(cc, data):
    assert type(cc) == str
    assert type(data) == str
    return cc + str(len(data)) + data
