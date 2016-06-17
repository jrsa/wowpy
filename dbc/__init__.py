import logging
from struct import Struct
import format_import
import stringpool


class DbcFile(object):
  HEADER = Struct('<4sIIII')
  CIGAM = 'WDBC'

  def __init__(self, rec_format):
    """
    represent a dbc table, specifying the format via a
    (struct_format, [stringfield_indices]) pair
    """
    self.records = []

    if rec_format is None:
      logging.warning('no format specified')
      self.record_struct = None
      self.string_fields = []
    else:
      self.record_struct = Struct(rec_format[0])
      self.string_fields = rec_format[1]

  def load(self, data):
    """load records from string with the file contents"""

    def getstring(data, ofs):
      i = ofs
      dst = ''
      try:
        while data[i] != '\x00':
          dst += data[i]
          i += 1
        return dst
      except IndexError, e:
        logging.error('read past end of data')
        return dst

    header_data = DbcFile.HEADER.unpack_from(data)
    magic, rec_count, field_count, rec_size, string_size = header_data

    if magic != DbcFile.CIGAM:
      raise RuntimeError(
        'invalid dbc file (magic == {magic})'.format(magic=magic))

    if self.record_struct is None:
      logging.info('defaulting to unsigned ints for all fields')
      self.record_struct = Struct('I' * field_count)

    stringblock = data[-string_size:]

    for i in xrange(rec_count):
      offset = DbcFile.HEADER.size + (i * self.record_struct.size)
      rec = list(self.record_struct.unpack_from(data, offset))
      for f in self.string_fields:
        rec[f] = getstring(stringblock, rec[f])
      self.records.append(rec)

  def save(self):
    """
    turns array of records back into a binary file, returns file
    contents as a string.
    """
    nrecs = len(self.records)
    stringblock_out = stringpool.StringPool()
    datablock = bytearray()

    for i, r in enumerate(self.records):
      pass
      datablock.append(self.record_struct.pack(*r))

    hdr_data = (
      DbcFile.CIGAM, nrecs, field_count, self.record_struct.size, string_size)

    result = DbcFile.HEADER.pack()

