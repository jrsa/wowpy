"""
wdt file parsing
"""

import struct
from ..chunks import parse

from .format import chunks as wdt_chunk_formats

from itertools import product


MAP_SIZE = 64


class Wdt(object):
  def read(self, data):
    """takes file as bytes"""
    parsed_chunks = parse(data, wdt_chunk_formats)

    self.version = parsed_chunks['MVER'].version
    self.flags = parsed_chunks['MPHD'].flags
    self.object_filename = parsed_chunks['MWMO'].get(0)

    try:
      self.obj = parsed_chunks['MODF']
    except KeyError: pass

    self.extant_tiles = []

    for x, y in product(range(MAP_SIZE), range(MAP_SIZE)):
      if parsed_chunks['MAIN'][x + (y * MAP_SIZE)].flags & 1:
        self.extant_tiles.append((x, y),)

  def write(self):
    """returns a string to be written to file"""
    result = bytearray()

    result += makechunk('REVM', struct.pack('i', self.version))


    result += struct.pack('I')


    return result
