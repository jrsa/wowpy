from . import file_format
from .. import chunks
import struct

from collections import namedtuple

from . import file_format

SMChunk = namedtuple('SMChunk', ['flags', 'indexX', 'indexY', 'nLayers', 'nDoodadRefs',
                                 'ofsHeight', 'ofsNormal', 'ofsLayer', 'ofsRefs', 'ofsAlpha',
                                 'sizeAlpha', 'ofsShadow', 'sizeShadow', 'areaId', 'nWmoRefs',
                                 'holesAndUnk', 'map1', 'map2', 'map3', 'map4', 'nEffectDoodadHi',
                                 'nEffectDoodadLo', 'ofsSoundEmitters', 'nSoundEmitters',
                                 'ofsLiquid', 'sizeLiquid', 'xpos', 'ypos', 'zpos', 'ofsMccv',
                                 'ofsMclv', 'unused'])


class MapChunk(object):
    def __init__(self):
        self.areaId = None

        # dont really need this except to debug/analyze files
        self.chunknames = []

    def load(self, header, data):
        header_data = SMChunk._make(header)
        self.areaId = header_data.areaId
        for cc, size, contents in chunks.chunks(data):
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
                header = file_format.mcnk_header.unpack(contents[:128])
                data = contents[128:]
                c.load(header, data)
                self.chunks.append(c)
            elif cc == b'OMWM':
                self.wmo_names = contents.split(b'\000')

            elif cc == b'XDMM':
                self.doodad_names = contents.split(b'\000')
