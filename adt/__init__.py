from . import file_format
from .. import chunks
import struct


raise ImportError("borken")


class ChunkType(Enum):
    string = 1
    stringarray = 2
    struct = 3
    structarray = 4


formats = {
    b"TVCM": "f"*145,
}


class AdtFile(object):

    def load(self, data):
        for cc, size, contents in chunks.chunks(data):
            if cc == b'KNCM':
                hdr = self.chunk_header.unpack(contents[:128])
                for cc, size, contents in chunks.chunks(contents[128:]):
                    
