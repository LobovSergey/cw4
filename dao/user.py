from dao.model.user import User


class UserDAO:

    def __init__(self, session):
        self.session = session

    def create_user(self, data):
        user = User(**data)
        self.session.add(user)
        self.session.commit()

    def get_by_name(self, name):
        return self.session.query(User).filter(User.email == name).first()
