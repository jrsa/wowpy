
import logging
from os.path import dirname, join
from lxml import etree
from .. import simple_file

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
            "uint64": "Q"
        }

    def get_format(self, dbc_name):
        if dbc_name[-4:] == '.dbc':
            dbc_name = dbc_name[:-4]

        format_string = ''
        string_fields = []

        file_element = self.root.find(dbc_name)

        if file_element is None:
            logging.warning(
                "couldnt find {name} in format file".format(name=dbc_name))
            return None

        fields = file_element.getchildren()

        idx = 0

        for field in fields:
            name = field.find("name").text
            type_id = field.find("type").text

            format_string += self.typetable[type_id]

            if type_id == "string":
                string_fields.append(idx)

            idx += 1

        return format_string, string_fields
