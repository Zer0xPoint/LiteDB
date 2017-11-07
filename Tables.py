import re
import regex
import os
from prettytable import PrettyTable
import Database
import xlrd
import xlwt


def create_new_table(command):
    table_name_parse = re.search(r".*?(?=\()", command)
    table_name = table_name_parse.group().split(" ")[2]
    database_name = Database.now_use_database
    replace_parse = "create table " + table_name
    command = command.replace(replace_parse, "")

    table_info_parse = regex.search(r"\((?:[^{}]|(?R))*\)", command)
    table_info_group = table_info_parse.group()
    table_info_list = str(table_info_group)[1:-1].split(",")

    primary_key = table_info_list[-1].split()[2]
    print(primary_key)
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

    print(table_field, table_type, table_key)

    print(show_table)
    write_to_excel(table_name, database_name, table_field, table_type, table_key)


def write_to_excel(table_name, database_name, table_field, table_type, table_key):
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
    replace_parse = "insert into" + table_name
    command = command.replace(replace_parse, "")

    table_info_parse = regex.search(r"\((?:[^{}]|(?R))*\)", command)
    table_info_group = table_info_parse.group()
    table_info_list = str(table_info_group)[1:-1].split(",")

    table_index_dic = get_table_index_dic(table_name)

    table_field, table_type, table_key = read_from_excel(table_index_dic, table_name)
    # add sheet if not exist
    # check if item in list can match item in field
    # check the type of attrib
    show_table = PrettyTable(table_field)
    print(show_table)
    print(table_info_list)
    print(table_index_dic)


# def delete_table_info():
# def search_table_info():
def show_table_desc(command):
    command_parse = re.search(r"desc\s*?table\s(.*)", command)
    table_name = command_parse.group(1).strip()
    table_index_dic = get_table_index_dic(table_name)

    table_field, table_type, table_key = read_from_excel(table_index_dic, table_name)
    show_table = PrettyTable()

    show_table.add_column("Field", table_field)
    show_table.add_column("Type", table_type)
    show_table.add_column("Key", table_key)

    print(show_table)


def show_table_name(command):
    file_dir = "/Users/rileylee/Documents/PyCharmProjects/LiteDB/Databases/" + Database.now_use_database
    file_list = os.listdir(file_dir)
    print(file_list)


# def show_table_info():

def get_table_index_dic(table_name):
    database_name = Database.now_use_database
    database_name = "first"
    database_dic = "/Users/rileylee/Documents/PyCharmProjects/LiteDB/Databases/" + database_name
    table_dic = database_dic + "/"
    excel_file_name = table_name + ".xls"
    table_index_dic = table_dic + excel_file_name

    return table_index_dic


if __name__ == "__main__":
    # command = "create table test01 (name char,id int,birth int,salary int,primary key id)"
    # command = "desc table test"
    command = "insert into test01 (Lee, 1, 19950612, 3000)"
    # create_new_table(command)
    # Test2("/Users/rileylee/Documents/PyCharmProjects/LiteDB/Databases/first")
    insert_table_info(command)
