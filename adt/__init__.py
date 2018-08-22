from .. import chunks
from ..namedstruct import NamedStruct


mcnk_header = NamedStruct((
    ('flags', 'I'),
    ('indexX', 'I'),
    ('indexY', 'I'),
    ('nLayers', 'I'),
    ('nDoodadRefs', 'I'),
    ('ofsHeight', 'I'),
    ('ofsNormal', 'I'),
    ('ofsLayer', 'I'),
    ('ofsRefs', 'I'),
    ('ofsAlpha', 'I'),
    ('sizeAlpha', 'I'),
    ('ofsShadow', 'I'),
    ('sizeShadow', 'I'),
    ('areaId', 'I'),
    ('nWmoRefs', 'I'),
    ('holesAndUnk', 'I'),
    ('map1', 'I'),
    ('map2', 'I'),
    ('map3', 'I'),
    ('map4', 'I'),
    ('nEffectDoodadHi', 'I'),
    ('nEffectDoodadLo', 'I'),
    ('ofsSoundEmitters', 'I'),
    ('nSoundEmitters', 'I'),
    ('ofsLiquid', 'I'),
    ('sizeLiquid', 'I'),
    ('xpos', 'f'),
    ('ypos', 'f'),
    ('zpos', 'f'),
    ('ofsMccv', 'I'),
    ('ofsMclv', 'I'),
    ('unused', 'I')
), 'SMChunk')


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
            elif cc == b'OMWM':
                self.wmo_names = contents.split(b'\000')

            elif cc == b'XDMM':
                self.doodad_names = contents.split(b'\000')
