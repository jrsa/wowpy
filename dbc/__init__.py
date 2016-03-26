import formats
from struct import Struct


class DbcFile(object):
  header = Struct('<4sIIII')

  def getstring(self, ofs):
    i = ofs; dst = ''
    while self.stringblock[i] != '\x00':
      dst += self.stringblock[i]
      i += 1
    return dst

  def __init__(self, data, format):
    self.records = []
    magic, rec_count, field_count, rec_size, string_size = DbcFile.header.unpack_from(data)
    if magic != 'WDBC':
      print 'invalid dbc file (magic == ' + magic + ')'
      return

    if format == None:
      format = ('i' * field_count, [])
    recStruct = Struct(format[0])
    stringFields = format[1]

    self.stringblock = data[-string_size:]

    for i in xrange(rec_count):
      rec = list(recStruct.unpack_from(data, DbcFile.header.size + (i * recStruct.size)))
      for f in stringFields:
        rec[f] = self.getstring(rec[f])
      self.records.append(rec)

