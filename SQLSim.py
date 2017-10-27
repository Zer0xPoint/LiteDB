import Database

def split_command(command):
    command = command.strip()
    return {
        "create": create_database
    }.get(command.split()[0], error_info())(command)


def get_command():
    while True:
        command = input("LiteDB >").lower()
        if command == "exit":
            print("Bye")
            break
        # elif len(command) <= 3:
        #     error_info()
        #     continue
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
    print("\nsyntax Error\n")
