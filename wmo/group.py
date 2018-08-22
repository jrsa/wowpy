import struct

from .. import chunks

class Group(object):
    def load(self, filename):
        for c, sz, d in chunks.chunks(simple_file.load(fn)):
            print(c[::-1], sz) # prints chunk ID backwards
            if c == b'PGOM':
                print('\tgroup header:')
                hdr = struct.unpack(17 * 'I', d[:68])
                print(hdr)

                print('\tgroup subchunks:')
                for subchunkid, subchunksize, subchunkdata in chunks.chunks(d[68:]):
                    print('\t', subchunkid[::-1], subchunksize)