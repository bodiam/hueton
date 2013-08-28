class HuetonApi:

    def init(self, developer_name):
        print("Hello")
        self.registered = False

    def connect(self):
        print("Connect")

        if self.registered:
            return True
        else:
            return False

    def register(self):
        print("register")

        self.registered = True




