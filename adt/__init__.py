import file_format
import chunks


class AdtFile(object):
    def __init__(self):
        self.chunks = []
        self.doodad_refs = []
        self.mapobject_refs = []

    
    def load(self, data):
        for cc, size, contents in chunks.chunks(data):
            pass
            # print cc
    