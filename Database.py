import OperatFile
import re

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def create_new_database(command):
    print("Create new Database")
    command_parse = re.search(r'create\s*?database\s(.*?)', command)
    # print(command_parse.group(1))
    if (command_parse):
        tree = ET.parse("database_index.xml")
        root = tree.getroot()
        database_count = len(tree.findall("database"))
        new_database = ET.SubElement(root, "database", attrib={"id": str(database_count + 1)})
        new_db_name = ET.SubElement(new_database, "name")
        new_db_name.text = command_parse.group(1)
        tree.write("database_index.xml")


class Database(object):
    def __init__(self, *args):
        self.name = args[0]
        self.createDate = args[1]
        self.allinfo = ",".join(args)

    def display_all_info(self, info):
        info = info.split(",")
        res = []
        for i in info:
            if hasattr(self, i.strip()):
                res.append(str(getattr(self, i.strip())))


if __name__ == "__main__":
    command = input("Input")
    create_new_database(command)
