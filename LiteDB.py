from Login import Login
import SQLSim
import Database

if __name__ == '__main__':
    login = Login()
    # is_authored = login.checkPassword()
    is_authored = False
    Database.use_new_database_name.has_been_called = False

    while True:
        is_authored = login.checkPassword()
        if not is_authored:
            print("login failed, Please check your password and try again")
        else:
            print("Welcome to LiteDB, a Lite Databases")
            SQLSim.get_command("")
            break
