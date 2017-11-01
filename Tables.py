import re
import regex


def create_new_table(command):
    command_parse = re.search(r"\((?:[^{}]|(?R))*\)", command)
    table_attribs = command_parse.group()
    print(table_attribs)