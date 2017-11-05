import re
import regex
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

    table_field, table_type = [], []

    show_table = PrettyTable(["Field", "Type"])

    for i in range(len(table_info_list)):
        table_attrib_list = str(table_info_list[i]).split(" ")
        print(table_attrib_list)
        show_table.add_row(table_attrib_list)

        table_field.append(table_attrib_list[0])
        table_type.append(table_attrib_list[1])

    print(table_field, table_type)

    print(show_table)
    write_to_excel(table_name, database_name, table_field, table_type)


def write_to_excel(table_name, database_name, table_field, table_type):
    excel_file = xlwt.Workbook()
    sheet = excel_file.add_sheet("test")

    for field_index, field_enum in enumerate(table_field):
        sheet.write(field_index, 0, field_enum)
    for type_index, type_enum in enumerate(table_type):
        sheet.write(type_index, 1, type_enum)

    database_dic = "/Users/rileylee/Documents/PyCharmProjects/LiteDB/Databases/" + database_name
    table_dic = database_dic + "/" + table_name
    table_index_dic = table_dic + "_index.xls"
    print(table_index_dic)
    excel_file.save(table_index_dic)

# def read_from_excel():
# def insert_table():
# def delete_table():
# def search_table():
# def show_table():


if __name__ == "__main__":
    command = "create table test (name varchar(20),id int,birth int,salary int)"
    create_new_table(command)
