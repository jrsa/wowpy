
chunks = {
    'MVER': (('version', 'I'),),
    'MPHD': (('flags', 'I'),
             (None, 'I'),
             (None, 'I'),
             (None, 'I'),
             (None, 'I'),
             (None, 'I'),
             (None, 'I'),
             (None, 'I')),
    'MAIN': (('flags', 'I'),
             (None, 'I')),
    'MODF': (('mmid', 'I'),
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
             (None, 'H'))
}
