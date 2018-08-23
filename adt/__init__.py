from .. import chunks
from .file_format import mcnk_header


class MapChunk(object):
    def __init__(self):
        self.areaId = None

        # dont really need this except to debug/analyze files
        self.chunknames = []

    def load(self, data):
        header = mcnk_header.unpack(data[:128])
        subchunks = data[128:]

        self.areaId = header.areaId

        size_overrides = {
            b'MCAL'[::-1]: header.sizeAlpha - 8,
            b'MCLQ'[::-1]: header.sizeLiquid,
            b'MCNR'[::-1]: 448
        }

        for cc, size, contents in chunks.chunks(subchunks, size_overrides):
            self.chunknames.append(cc)


class AdtFile(object):
    def __init__(self):
        self.chunks = []
        self.doodad_refs = []
        self.mapobject_refs = []


    def load(self, data):
        for cc, size, contents in chunks.chunks(data):
            if cc == b'KNCM':
                c = MapChunk()
                c.load(contents)
                self.chunks.append(c)
