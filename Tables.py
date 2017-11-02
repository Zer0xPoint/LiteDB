import re
import regex


def create_new_table(command):
    tables_name_parse = re.search(r"create\s*?table\s(.*)", command)
    tables_name = tables_name_parse.group().strip()
    tables_info_parse = regex.search(r"\((?:[^{}]|(?R))*\)", command)
    table_infos = tables_info_parse.group()
