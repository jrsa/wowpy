"""
wdt file parsing
"""

import struct
from chunks import chunks, makechunk


MAP_SIZE = 64


class Wdt(object):
  def __init__(self, version=18):
    self.version = version
    self.extant_tiles = []
    self.flags = 0
    self.main_rec = struct.Struct('II')
    self.objdef_rec = struct.Struct('IIffffffffffffHHHH')
    self.object_filename = None

  def parse_modf(self, data):
    self.obj = self.objdef_rec.unpack(data)

  def read(self, file):
    """takes file as a string"""
    if file[:4] != 'REVM' or file[0x34:0x38] != 'NIAM':
      raise RuntimeError('not a wdt file')

    for id, size, data in chunks(file):
      if id == 'REVM':
        self.version = struct.unpack('I', data)[0]

      if id == 'NIAM':
        if len(data) != 32768:
          raise RuntimeError('invalid MAIN sect')

        for i in range(64):
          for j in range(64):
              idx = (j * 64 + i) * self.main_rec.size
              flag = self.main_rec.unpack_from(data, idx)[0]
              if flag & 1 == 1:
                self.extant_tiles.append((i, j))

      elif id == 'DHPM':
        self.flags = struct.unpack('iiiiiiii', data)[0]

      if id == 'OMWM':
        self.object_filename = data[:-1]
      elif id == 'FDOM':
        self.parse_modf(data)

  def write(self):
    """returns a string to be written to file"""
    result = bytearray()

    result += makechunk('REVM', struct.pack('i', self.version))


    result += struct.pack('I')


    return result
