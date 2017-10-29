import OperatFile
import re
import Time
try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et


def create_new_database(command):
    command_parse = re.search(r'create\s*?database\s(.*)', command)

    if command_parse:
        tree = OperatFile.read_xml("database_index.xml")
        root = tree.getroot()
        # database_count = len(tree.findall("database"))
        new_database = et.SubElement(root, "database", attrib={"name": command_parse.group(1).strip()})
        new_db_date = et.SubElement(new_database, "date")
        new_db_date.text = Time.local_time()

        OperatFile.write_xml(tree, "database_index.xml")


def drop_database(command):
    command_parse = re.search(r'drop\s*?database\s(.*)', command)

    if command_parse:
        tree = et.parse("database_index.xml")
        root = tree.getroot()
        drop_node = tree.find("database")


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
