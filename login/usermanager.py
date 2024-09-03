class UserManager:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.current_user = None

    def set_current_user(self, username):
        self.current_user = username

    def get_current_user(self):
        return self.current_user