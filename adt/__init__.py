import file_format
from .. import chunks
import struct


class AdtFile(object):
    def __init__(self):
        self.chunks = []
        self.doodad_refs = []
        self.mapobject_refs = []
        self.chunk_header = struct.Struct('')

    
    def load(self, data):
        for cc, size, contents in chunks.chunks(data):
            print cc
            if cc == 'KNCM':
                print struct.unpack('I' * 32, contents[:128])
                for cc, size, contents in chunks.chunks(contents[128:]):
                   print cc, size
    