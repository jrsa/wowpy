from struct import Struct
from ..namedstruct import NamedStruct
from ..stringblock import StringBlock
from ..structarray import StructArray


root_chunks = {
    'MVER': Struct('I'),
    'MOHD': Struct('IIIIIIIIIffffffI'),

    'MOGN': StringBlock(),
    'MOTX': StringBlock(),
    'MODN': StringBlock(),
    'MOSB': StringBlock(),

    # from CMapObj::GetGroupBounds in 5875 IDB
    'MOGI': StructArray(NamedStruct(
            (('flags', 'I'),
             ('extents_b_x', 'f'),
             ('extents_b_y', 'f'),
             ('extents_b_z', 'f'),
             ('extents_t_x', 'f'),
             ('extents_t_y', 'f'),
             ('extents_t_z', 'f'),
             ('nameIndex', 'I'),), 'SMOGroupInfo'),)
}