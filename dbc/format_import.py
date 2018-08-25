
import logging
from os.path import dirname, join
from lxml import etree
from .. import simple_file

from ..namedstruct import NamedStruct

packaged_xml_filename = join(dirname(__file__), "map.xml")


class FormatImport:

    """
    import an xml file and provide the record format
    for each dbc file given it's name
    """

    def __init__(self, fn=packaged_xml_filename):
        xml_contents = simple_file.load(fn)
        self.root = etree.fromstring(xml_contents)
        self.typetable = {
            "string": "I",  # 'string' is really an offset
            "uint32": "I",
            "int32": "i",
            "float": "f",
            "Float": "f",
            "uint8": "B",
            "uint64": "Q"
        }
        self.mysql_typetable = {
            "string": "TEXT",
            "uint32": "INT UNSIGNED",
            "int32": "INT",
            "float": "FLOAT",
            "Float": "FLOAT",
            "uint8": "TINYINT UNSIGNED",
            "uint64": "BIGINT"
        }

    def load_format(self, name):
        file_element = self.root.find(name)

        if file_element is not None:
            return file_element.getchildren()
        else:
            logging.warning(
                "couldnt find {name} in format file".format(name=dbc_name))
            return None

    def get_format(self, dbc_name):
        if dbc_name[-4:] == '.dbc':
            dbc_name = dbc_name[:-4]

        format_string = ''
        string_fields = []

        fields = self.load_format(dbc_name)

        idx = 0

        for field in fields:
            type_id = field.find("type").text

            format_string += self.typetable[type_id]

            if type_id == "string":
                string_fields.append(idx)

            idx += 1

        record_struct = NamedStruct(tuple(zip(self.get_field_names(dbc_name), format_string)))
        return record_struct, string_fields

    def get_field_names(self, dbc_name):
        if dbc_name[-4:] == '.dbc':
            dbc_name = dbc_name[:-4]

        fields = self.load_format(dbc_name)

        return [field.find("name").text for field in fields]

    def get_mysql_columns(self, table_name):
        """
        this provides a tuple (name, sql datatype) for every column. an
        index-based default name is provided if there is no defined name
        for the column. the first field is always an id in dbc files,
        and it is named as such so that it can be specified as the
        primary key of the mysql table.
        """
        if table_name[-4:] == '.dbc':
            table_name = table_name[:-4]

        mysql_columns = []

        fields = self.load_format(table_name)

        for i, field in enumerate(fields):
            name = field.find("name").text
            if not name:
                if i == 0:
                    name = "id"
                else:
                    name = "col{}".format(i)

            type_id = field.find("type").text
            mysql_columns.append((name, self.mysql_typetable[type_id]))

        return mysql_columns
