"""
wdt file parsing
"""

import sys, struct
from simple_file import load
from chunks import chunks


MAP_SIZE = 64

class Wdt(object):
  def __init__(self, version=0):
    self.version = version
    self.extant_tiles = []
    self.flags = 0
    self.main_rec = struct.Struct('ii')
    self.objdef_rec = struct.Struct('IIffffffffffffHHHH')

  def parse_modf(self, data):
    rec = self.objdef_rec.unpack(data)
    id, uid, posx, posy, posz,\
    rota, rotb, rotc, b0x, b0y,\
    b0z, b1z, b1y, b1z, flags, dset, nameset, null = rec

  # io

  def read(self, file):
    """takes file as a string"""
    if file[:4] != 'REVM' or file[0x34:0x38] != 'NIAM':
      raise RuntimeError('not a wdt file')
    for id, size, data in chunks(file):
      if id == 'REVM':
        self.version = struct.unpack('i', data)
      if id == 'NIAM':
        for i in xrange(4096):
          flags, null = self.main_rec.unpack_from(data, i * self.main_rec.size)
          if flags & 1: self.extant_tiles.append((i / 64, i % 64))
      elif id == 'DHPM':
        self.flags = struct.unpack('iiiiiiii', data)[0]
      if id == 'OMWM':
        self.object_filename = data[:-1]
      elif id == 'FDOM':
        self.parse_modf(data)

  def write(self):
    """returns a string to be written to file"""
    f = ''



    return f
