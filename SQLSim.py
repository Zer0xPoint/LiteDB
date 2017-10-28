import Database


def get_command():
    while True:
        command = input("LiteDB >").lower()
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


def create_database(command):
    Database.create_new_database(command)


# def delete_database():
#
# def show_databases():
#
# def use_database():
#
def create_table(command):
    print("create Table")


# def delete_table():
#
# def update_table():
#
# def show_table():
#
# def serach_table():

def error_info():
    print("Syntax Error")
