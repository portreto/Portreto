from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals #This is a method is advised be documentation to avoid side effects that import have