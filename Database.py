import OperatFile
import re
import Time
import os
from prettytable import PrettyTable

try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

now_use_database = ""


def create_new_database(commands):
    command_parse = re.search(r'create\s*?database\s(.*)', commands)
    database_name = command_parse.group(1).strip()

    if command_parse:
        tree = OperatFile.read_xml("database_index.xml")
        root = tree.getroot()

        if not database_is_exist(root, database_name):
            new_database = et.SubElement(root, "database", attrib={"name": database_name})
            new_db_date = et.SubElement(new_database, "date")
            new_db_date.text = Time.local_time()

            os.mkdir("/Users/rileylee/Documents/PyCharmProjects/LiteDB/Databases/%s" % database_name)

        else:
            print("Can't create database '%s'; database exists" % database_name)

        OperatFile.write_xml(tree, "database_index.xml")


def drop_new_database(commands):
    command_parse = re.search(r'drop\s*?database\s(.*)', commands)
    database_name = command_parse.group(1).strip()

    if command_parse:
        tree = OperatFile.read_xml("database_index.xml")
        root = tree.getroot()

        try:
            os.rmdir("/Users/rileylee/Documents/PyCharmProjects/LiteDB/Databases/%s" % database_name)

            if database_is_exist(root, database_name):
                for child in root:
                    if child.attrib == {"name": database_name}:
                        root.remove(child)
            OperatFile.write_xml(tree, "database_index.xml")

        except OSError:
            print("Database is not empty")
        else:
            print("Can't drop database '%s'; database doesn't exist" % database_name)


def use_new_database_name(commands):
    global now_use_database
    command_parse = re.search(r'use\s*?(.*)', commands)
    now_use_database = command_parse.group(1).strip()
    if command_parse:
        tree = OperatFile.read_xml("database_index.xml")
        root = tree.getroot()

        if database_is_exist(root, now_use_database):
            for child in root:
                if child.attrib == {"name": now_use_database}:
                    print("Database changed to %s" % now_use_database)
                    use_new_database_name.has_been_called = True
        else:
            print("Unknown database '%s'" % now_use_database)
            now_use_database = ""

    return now_use_database


def show_current_databases():
    table = PrettyTable(["Database"])
    tree = OperatFile.read_xml("database_index.xml")
    root = tree.getroot()

    for child in root:
        attrib_values = str(child.attrib.values())
        show_parse = re.search(r"dict_values\W+'(.*)'\W+", attrib_values)
        table.add_row([show_parse.group(1)])

    print(table)


def database_is_exist(root, database_name):
    node_count = 0
    for child in root.iter("database"):
        if child.attrib["name"] == database_name:
            node_count = node_count + 1
        else:
            continue
    if node_count == 0:
        return False
    else:
        return True


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
    command = input("Input ")

    # drop_database(command)
    # create_new_database(command)
