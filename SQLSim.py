import Database


def get_command(last_command):
    while True:
        command = last_command + input("LiteDB >").lower()
        if command == "":
            get_command(command)
            continue
        if command == "exit":
            print("Bye")
            break
        split_command(command)


def split_command(command):
    command = command.strip()
    command_split = command.split()
    try:
        return {
            "create": create_database_or_table,
            "drop": drop_database_or_table,
            "use": use_database
        }.get(command_split[0], error_info)(command)
    except TypeError:
        print("TypeError")
    except IndexError:
        print("IndexError")


def create_database_or_table(command):
    command = command.strip()
    command_split = command.split()
    try:
        return {
            "database": create_database,
            "table": create_table
        }.get(command_split[1], error_info)(command)
    except TypeError:
        print("TypeError1")
    except IndexError:
        print("IndexError1")


def drop_database_or_table(command):
    command = command.strip()
    command_split = command.split()
    try:
        return {
            "database": delete_database,
            "table": delete_table
        }.get(command_split[1], error_info)(command)
    except TypeError:
        print("TypeError1")
    except IndexError:
        print("IndexError1")


def create_database(command):
    Database.create_new_database(command)


def delete_database(command):
    Database.drop_database(command)


# def show_databases():
#
def use_database():
    print("use database")


def create_table(command):
    print("create Table")


def delete_table(command):
    print("delete Table")


# def update_table():
#
# def show_table():
#
# def serach_table():

def error_info():
    print("Syntax Error")
