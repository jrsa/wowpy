from struct import Struct
from .. import chunks

chunk_formats = dict();

chunk_formats['REVM'] = Struct('I')
chunk_formats['DHOM'] = Struct('IIIIIIIIIffffffIIIIII')

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
            if cc == 'DHOM':
                header = chunk_formats['DHOM'].unpack_from(data)

                print header

                ntextures, ngroups, nportals, nlights, ndoodadnames, ndoodaddefs, \
                    ndoodadsets, r, g, b, a, wmoid, x1, y1, z1, x2, y2, z2, flag1, \
                    flag2, flag3, flag4, flag5 = header

