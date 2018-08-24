from ..namedstruct import NamedStruct
from ..stringblock import StringBlock
from ..structarray import StructArray


chunks = {
    'MVER': NamedStruct(
        (('version', 'I'),)),

    'MPHD': NamedStruct(
        (('flags', 'I'),
         (None, 'I'),
         (None, 'I'),
         (None, 'I'),
         (None, 'I'),
         (None, 'I'),
         (None, 'I'),
         (None, 'I'))),

    'MAIN': StructArray(NamedStruct(
            (('flags', 'I'),
             (None, 'I')))),

    'MWMO': StringBlock(),

    'MODF': NamedStruct(
        (('mmid', 'I'),
         ('guid', 'I'),
         ('posx', 'f'),
         ('posy', 'f'),
         ('posz', 'f'),
         ('rotx', 'f'),
         ('roty', 'f'),
         ('rotz', 'f'),
         ('extents_top_x', 'f'),
         ('extents_top_y', 'f'),
         ('extents_top_z', 'f'),
         ('extents_bottom_x', 'f'),
         ('extents_bottom_y', 'f'),
         ('extents_bottom_z', 'f'),
         ('flags', 'H'),
         ('doodadSet', 'H'),
         ('nameSet', 'H'),
         (None, 'H')))
}
