from .database import load_data, save_data

data = load_data()

class User:
    def __init__(self, username, password, email):
        self.id = len(data['users']) + 1
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return f'<User {self.username}>'

class Crud:
    def __init__(self, title, content):
        self.id = len(data['cruds']) + 1
        self.title = title
        self.content = content

    def __repr__(self):
        return f'<Crud {self.title}>'