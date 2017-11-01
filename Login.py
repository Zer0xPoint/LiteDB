import getpass


class Login:
    def __init__(self):
        self.password = "password"

    def checkPassword(self):
        while True:
            # password = getpass.getpass("Enter password: ")
            password = input("Enter password: ")

            if password == self.password:
                return True
            else:
                return False
