class Login():
    def __init__(self):
        self.password = "password"

    def checkPassword(self):
        while True:
            password = input("password: ")
            if password == self.password:
                return True
            else:
                return False
