import re
import regex
import os
from prettytable import PrettyTable
import Database
import xlrd
import xlwt
from xlutils.copy import copy
import SQLSim


def create_new_table(command):
    table_name_parse = re.search(r".*?(?=\()", command)
    table_name = table_name_parse.group().split(" ")[2]
    replace_parse = "create table " + str(table_name)
    command = command.replace(replace_parse, "")

    table_info_parse = regex.search(r"\((?:[^{}]|(?R))*\)", command)
    table_info_group = table_info_parse.group()
    table_info_list = str(table_info_group)[1:-1].split(",")
    table_info_list = remove_space_in_list(table_info_list)

    primary_key = table_info_list[-1].split()[2]
    del table_info_list[-1]

    table_field, table_type, table_key = [], [], []

    show_table = PrettyTable()

    for i in range(len(table_info_list)):
        table_attrib_list = str(table_info_list[i]).split(" ")

        table_field.append(table_attrib_list[0])
        table_type.append(table_attrib_list[1])
        if table_attrib_list[0] == primary_key:
            table_key.append("pri")
        else:
            table_key.append("")

    show_table.add_column("Field", table_field)
    show_table.add_column("Type", table_type)
    show_table.add_column("Key", table_key)

    print(show_table)
    write_to_excel(table_name, table_field, table_type, table_key)


def write_to_excel(table_name, table_field, table_type, table_key):
    try:
        excel_file = xlwt.Workbook()
        sheet = excel_file.add_sheet(table_name)

        for field_index, field_item in enumerate(table_field):
            sheet.write(field_index, 0, field_item)
        for type_index, type_item in enumerate(table_type):
            sheet.write(type_index, 1, type_item)
        for key_index, key_item in enumerate(table_key):
            sheet.write(key_index, 2, key_item)

        table_index_dic = get_table_index_dic(table_name)

        excel_file.save(table_index_dic)
        print("create table success")
    except IOError:
        print("Can't create/write to file '%s'." % table_name)


def read_from_excel(table_index_dic, table_name):
    excel_file = xlrd.open_workbook(table_index_dic)
    sheet = excel_file.sheet_by_name(table_name)
    nrows = sheet.nrows

    table_field, table_type, table_key = [], [], []

    for i in range(nrows):
        row_values = sheet.row_values(i)
        table_field.append(row_values[0])
        table_type.append(row_values[1])
        table_key.append(row_values[2])

    return table_field, table_type, table_key


def insert_table_info(command):
    table_name_parse = re.search(r".*?(?=\()", command)
    table_name = table_name_parse.group().split(" ")[2]
    replace_parse = "insert into" + str(table_name)
    command = command.replace(replace_parse, "")

    table_info_parse = regex.search(r"\((?:[^{}]|(?R))*\)", command)
    table_info_group = table_info_parse.group()
    table_info_list = str(table_info_group)[1:-1].split(",")
    table_info_list = remove_space_in_list(table_info_list)

    table_index_dic = get_table_index_dic(table_name)

    table_field, table_type, table_key = read_from_excel(table_index_dic, table_name)

    # check the type of attrib
    if is_attrib_match_type(table_type, table_info_list):
        # check if item in list can match item in field
        if len(table_info_list) == len(table_field):
            show_table = PrettyTable(table_field)
            show_table.add_row(table_info_list)
            print(show_table)
            print(table_index_dic)

            read_excel_file = xlrd.open_workbook(table_index_dic, formatting_info=True)
            write_excel_file = copy(read_excel_file)

            sheets_list = read_excel_file.sheet_names()
            if "infos" in sheets_list:
                print("sheet exist")
            else:
                sheet = write_excel_file.add_sheet("infos")

                for field_index, field_item in enumerate(table_field):
                    sheet.write(0, field_index, field_item)
                for info_index, info_item in enumerate(table_info_list):
                    sheet.write(1, info_index, info_item)

                write_excel_file.save(table_index_dic)

        else:
            print("Column count doesn't match value count")
    else:
        print("Column doesn't match value type")


# def delete_table_info():
# def search_table_info():
def show_table_desc(command):
    command_parse = re.search(r"desc\s*?table\s(.*)", command)
    try:
        table_name = command_parse.group(1).strip()
        table_index_dic = get_table_index_dic(table_name)

        table_field, table_type, table_key = read_from_excel(table_index_dic, table_name)
        show_table = PrettyTable()

        show_table.add_column("Field", table_field)
        show_table.add_column("Type", table_type)
        show_table.add_column("Key", table_key)

        print(show_table)
    except AttributeError:
        SQLSim.error_info()


def show_table_name(command):
    file_dir = "/Users/rileylee/Documents/PyCharmProjects/LiteDB/Databases/" + Database.now_use_database
    file_list = os.listdir(file_dir)
    new_line = "\n"
    new_line = new_line.join(file_list)
    new_line = new_line.replace(".xls", "")
    show_table = PrettyTable(["Tables_in_%s" % Database.now_use_database])
    show_table.add_row([new_line])
    print(show_table)
    return file_list


# def show_table_info():

def get_table_index_dic(table_name):
    database_name = Database.now_use_database
    # database_name = "first"
    database_dic = "/Users/rileylee/Documents/PyCharmProjects/LiteDB/Databases/" + database_name
    table_dic = database_dic + "/"
    excel_file_name = table_name + ".xls"
    table_index_dic = table_dic + excel_file_name

    return table_index_dic


def table_is_exist(table_name):
    node_count = 0
    exist_table_name_list = show_table_name(table_name)
    for name in exist_table_name_list:
        if table_name == name:
            node_count = node_count + 1
        else:
            continue
    if node_count == 0:
        return False
    else:
        return True


def is_attrib_match_type(table_type, table_info_list):
    flag = 0
    for type_index, type_item in enumerate(table_type):
        for info_index, info_item in enumerate(table_info_list):
            if type_index == info_index:
                if (info_item.isalnum() and type_item == "int") or (info_item.isalpha() and type_item == "char"):
                    flag = flag
                else:
                    flag = flag + 1
                    continue
    if flag == 0:
        return True
    else:
        return False


def remove_space_in_list(some_list):
    some_list = [item.strip(" ") for item in some_list]
    return some_list


if __name__ == "__main__":
    # command = "create table test01 (name char,id int,birth int,salary int,primary key id)"
    # command = "desc table test"
    command = "insert into test01 (Lee,1,19950612,3000)"
    # create_new_table(command)
    # Test2("/Users/rileylee/Documents/PyCharmProjects/LiteDB/Databases/first")
    insert_table_info(command)
    # show_table_name(command)
