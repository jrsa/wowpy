"""
import an xml file and provide the record format
for each dbc file given it's name
"""

from lxml import etree

import simple_file


class FormatImport:
    def __init__(self, fn):
        self.root = etree.fromstring(simple_file.load(fn))
        self.typetable = {
            "string": "I",  # 'string' is really an offset
            "uint32": "I",
            "int32": "i",
            "float": "f"
        }

    def get_format(self, dbc_name):
        if dbc_name[-4:] == '.dbc':
            dbc_name = dbc_name[:-4]

        file_element = self.root.find(dbc_name)
        fields = file_element.getchildren()

        for field in fields:
            name = field.find("name").text
            type = field.find("type").text
