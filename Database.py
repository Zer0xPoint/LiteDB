import OperatFile
import re
import Time
try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et


def create_new_database(command):
    command_parse = re.search(r'create\s*?database\s(.*)', command)
    database_name = command_parse.group(1).strip()

    if command_parse:
        tree = OperatFile.read_xml("database_index.xml")
        root = tree.getroot()
        new_database = et.SubElement(root, "database", attrib={"name": database_name})
        new_db_date = et.SubElement(new_database, "date")
        new_db_date.text = Time.local_time()

        OperatFile.write_xml(tree, "database_index.xml")


def drop_database(command):
    command_parse = re.search(r'drop\s*?database\s(.*)', command)
    database_name = command_parse.group(1).strip()

    if command_parse:
        tree = OperatFile.read_xml("database_index.xml")
        # tree = et.parse("database_index.xml")
        root = tree.getroot()
        del_parent_node = OperatFile.find_nodes(tree, "databases")
        OperatFile.del_node_by_tagkeyvalue(del_parent_node, "database", {"name": database_name})

        # del_node = root.find("database")
        # if del_node.attrib["name"] == "test":
        #     root.remove(del_node)

        # for child in root():
        #     print(child.tag, child.attrib)

        OperatFile.write_xml(tree, "database_index.xml")


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
