import re
import regex
from prettytable import PrettyTable


def create_new_table(command):
    table_name_parse = re.search(r"create\s*?table\s(.*)", command)
    table_name = table_name_parse.group(1)
    command = command.replace("create table test", "")
    table_info_parse = regex.search(r"\((?:[^{}]|(?R))*\)", command)
    table_infos = table_info_parse.group()
    table_infos = str(table_infos)[1:-1].split(",")
    table_field = table_infos[0].split(" ")[0]


    show_table = PrettyTable(["Field", "Type"])
    print(table_infos)
    print(show_table)
    print(table_field)

if __name__ == "__main__":
    command = "create table test(name varchar(20), id int)"
    create_new_table(command)