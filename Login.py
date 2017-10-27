class Login():
    def __init__(self):
        self.password = "password"

    def checkPassword(self, *args):
        while True:
            password = input("password: ")
            if password == self.password:
                return True
            else:
                return False