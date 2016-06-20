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
        def process_string_fields(rec):
            """
            returns a copy of the record where the strings replaced 
            with offsets into the string pool
            """
            rec_copy = list(rec)
            for fi in self.string_fields:
                rec_copy[fi] = stringblock_out.lookup(rec_copy[fi])

            return rec_copy

        stringblock_out = stringpool.StringPool()
        datablock = bytearray()
        result = bytearray()

        for r in self.records:
            strung = process_string_fields(r)
            rowdata = self.record_struct.pack(*strung)
            datablock += rowdata

        result = result.join(DbcFile.HEADER.pack(
            DbcFile.CIGAM,
            len(self.records),
            len(self.records[0]),  # TODO: how bout fucking not
            self.record_struct.size,
            len(stringblock_out.block)))

        result += datablock
        result += stringblock_out.block
        return result