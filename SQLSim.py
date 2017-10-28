import Database

def split_command(command):
    command = command.strip()
    command_split = command.split()
    try:
        return {
            "create": create_database,
        }.get(command_split[0], error_info)(command)
    except TypeError:
        print("TypeError")
    except IndexError:
        print("IndexError")

def get_command():
    while True:
        command = input("LiteDB >").lower()
        if command == "exit":
            print("Bye")
            break
        split_command(command)


def create_database(command):
    print("Create new Databases")
    Database.create_new_database()


# def delete_database():
#
# def show_databases():
#
# def use_database():
#
# def create_table():
#
# def delete_table():
#
# def update_table():
#
# def show_table():
#
# def serach_table():

def error_info():
    print("Syntax Error")
