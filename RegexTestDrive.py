import re
import regex


def get_command():
    command = '''aosdfiulakwnelkfihas;dfj(name char(10) not null, ssn char(18) not null, bdate char(10) not null, address char(30) not null, sex char(2) not null, salary float not null, superssn char(18) not null, dno char(3) not null, primary key(ssn))'''
    # command_parse = re.search(r"\((?:[^{}]|(?R))*\)", command)
    # print(command_parse.group())
    # command_parse = regex.compile(r"\((?:[^{}]|(?R))*\)")
    # fnd = command_parse.findall(command)
    # for j in fnd:
    #     print(j)
    command_parse = regex.search(r"\((?:[^{}]|(?R))*\)", command)
    table_attribs = command_parse.group().split(",")
    print(table_attribs)


if __name__ == "__main__":
    get_command()
