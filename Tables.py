import re
import regex
from prettytable import PrettyTable


def create_new_table(command):
    table_name_parse = re.search(r"create\s*?table\s(.*)", command)
    table_name = table_name_parse.group(1)
    command = command.replace("create table test", "")

    table_info_parse = regex.search(r"\((?:[^{}]|(?R))*\)", command)
    table_info_group = table_info_parse.group()
    table_info_list = str(table_info_group)[1:-1].split(",")

    table_field, table_type = [], []

    show_table = PrettyTable(["Field", "Type"])

    for i in range(len(table_info_list)):
        table_attrib_list = str(table_info_list[i]).split(" ")
        print(table_attrib_list)
        show_table.add_row(table_attrib_list)

        # for x in range(len(table_attrib_list)):
        #     table_field.append(table_attrib_list[0])
        #     table_type.append(table_attrib_list[1])
        # show_table.add_row([table_field[x], table_type[x]])

        # print(table_field, table_type)
    # print(table_attrib_list)
    # for i in table_infos:
    #     print(table_infos[i].split(" ")[0])
    #
    # table_field = table_infos[0].split(" ")[0]
    # table_type = table_infos[0].split(" ")[1]
    #
    #
    # print(table_infos)
    print(show_table)
    # print(table_field, table_type)


if __name__ == "__main__":
    command = "create table test(name varchar(20),id int,birth int,salary int)"
    create_new_table(command)
