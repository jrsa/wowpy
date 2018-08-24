from .. import chunks
from .format import root_chunks


class Root(object):

    """
    holds the data found in the wmo root file, which refers
    to the group files which actually hold polygons
    """

    def __init__(self):
        self.groups = []

    def load(self, filedata):
        parsed_chunks = chunks.parse(filedata, root_chunks)
        print(f'{parsed_chunks.keys()} found in wmo root file')

        # for k in parsed_chunks:
        #     print(k, parsed_chunks[k])

        # for g in parsed_chunks['MOGI']:
        #     print(parsed_chunks['MOGN'].get(g.nameIndex))

        # print(parsed_chunks['MOTX'].as_array())
        # print(parsed_chunks['MODN'].as_array())
        print(parsed_chunks['MOSB'].as_array())
