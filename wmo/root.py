from struct import Struct
from .. import chunks

chunk_formats = dict();

chunk_formats['REVM'] = Struct('I')
chunk_formats['DHOM'] = Struct('IIIIIIIIIffffffI')

# chunk_formats['XTOM'] = Struct('')
# chunk_formats['NGOM'] = Struct('')
# chunk_formats['BSOM'] = Struct('')
# chunk_formats['NDOM'] = Struct('')
# chunk_formats['SDOM'] = Struct('')

# chunk_formats['TMOM'] = Struct('')
# chunk_formats['IGOM'] = Struct('')
# chunk_formats['VPOM'] = Struct('')
# chunk_formats['TPOM'] = Struct('')
# chunk_formats['RPOM'] = Struct('')
# chunk_formats['VVOM'] = Struct('')
# chunk_formats['BVOM'] = Struct('')
# chunk_formats['TLOM'] = Struct('')
# chunk_formats['DDOM'] = Struct('')
# chunk_formats['GOFM'] = Struct('')


class Root(object):

    """
    holds the data found in the wmo root file, which refers
    to the group files which actually hold polygons
    """

    def __init__(self):
        self.groups = []

    def load(self, filedata):
        for cc, size, data in chunks.chunks(filedata):
            try:
                print(cc, size)
                print(chunk_formats[cc].unpack_from(data))
            except KeyError as e:
                print("format for {cc} not found".format(cc=cc))