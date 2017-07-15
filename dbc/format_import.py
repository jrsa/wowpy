
import logging
from os.path import dirname, join
from lxml import etree
from .. import simple_file

packaged_xml_filename = join(dirname(__file__), "map2.xml")


def find_by_name(list, name):
    return [x for x in list if x.attrib['Name'] == name][0]

def field_is_array(field):
    return field.attrib.has_key('ArraySize')

def field_array_size(field):
    return int(field.attrib['ArraySize'])


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
            "loc": "I" * 17,
            "uint32": "I",
            "uint": "I",
            "int32": "i",
            "int": "i",
            "float": "f",
            "Float": "f",
            "uint8": "B",
            "byte": "B",
            "ulong": "Q",
            "uint64": "Q"
        }

    def get_format(self, dbc_name):
        if dbc_name[-4:] == '.dbc':
            dbc_name = dbc_name[:-4]

        format_string = ''
        string_fields = []

        # file_element = self.root.find(dbc_name)
        table_definition = find_by_name(self.root, dbc_name)

        if table_definition is None:
            logging.warning(
                "couldnt find {name} in format file".format(name=dbc_name))
            return None

        fields = table_definition.getchildren()

        idx = 0

        for field in fields:
            name = field.attrib['Name']
            type_id = field.attrib['Type']

            try:
                type_token = self.typetable[type_id]
                
            except KeyError as e:
                raise RuntimeError("{} not found in type table".format(type_id))

            if field_is_array(field):
                type_token *= field_array_size(field)

            format_string += type_token

            if type_id == "string":
                string_fields.append(idx)
            elif type_id == "loc":
                for n in range(16):
                    string_fields.append(idx)
                    idx += 1
                idx += 1

            if type_id != "loc":
                idx += 1

        return format_string, string_fields
