from Login import Login
import SQLSim

if __name__ == '__main__':
    login = Login()
    isAuthored = login.checkPassword()
    while True:
        if isAuthored:
            print("Welcome to LiteDB, a Lite Databases")
            SQLSim.get_command("")
            break
        else:
            print("login failed, Please check your password and Renter")
            isAuthored = login.checkPassword()