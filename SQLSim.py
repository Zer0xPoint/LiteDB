import Database
import Tables


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
            "use": use_database,
            "show": show_database_or_table,
            "desc": show_table_desc,
            "insert": insert_into_table
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
            "database": drop_database,
            "table": delete_table
        }.get(command_split[1], error_info)(command)
    except TypeError:
        print("TypeError1")
    except IndexError:
        print("IndexError1")


def show_database_or_table(command):
    command = command.strip()
    command_split = command.split()
    try:
        return {
            "databases": show_databases,
            "tables": show_table_name
        }.get(command_split[1], error_info)(command)
    except TypeError:
        print("TypeError1")
    except IndexError:
        print("IndexError1")


def create_database(command):
    Database.create_new_database(command)


def drop_database(command):
    Database.drop_new_database(command)


def show_databases(command):
    Database.show_current_databases()


def use_database(command):
    Database.use_new_database_name(command)


def show_table_name(command):
    if not Database.use_new_database_name.has_been_called:
        print("No database selected")
        get_command("")
    else:
        Tables.show_table_name(command)


def create_table(command):
    if not Database.use_new_database_name.has_been_called:
        print("No database selected")
        get_command("")
    else:
        Tables.create_new_table(command)


def delete_table(command):
    print("delete Table")


def show_table_desc(command):
    if not Database.use_new_database_name.has_been_called:
        print("No database selected")
        get_command("")
    else:
        Tables.show_table_desc(command)


def insert_into_table(command):
    # if not Database.use_new_database_name.has_been_called:
    #     print("No database selected")
    #     get_command("")
    # else:
    #     Tables.insert_table_info(command)
    if is_use_database():
        Tables.insert_table_info(command)
    else:
        get_command("")


# def update_table():
#
# def show_table():
#
# def search_table():
def is_use_database():
    if not Database.use_new_database_name.has_been_called:
        print("No database selected")
        return False
    else:
        return True


def error_info():
    print("Syntax Error")
