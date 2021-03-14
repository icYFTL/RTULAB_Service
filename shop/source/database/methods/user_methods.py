from ..models import User
from . import session


class UserMethods:
    def __init__(self):
        self.__session = session

    def add_user(self, user: User) -> User:
        self.__session.add(user)
        self.__session.commit()

        return user

    def remove_user(self, user: User) -> None:
        raise NotImplemented  # Users will be life always

    def get_users(self, **kwargs) -> list:
        return [x for x in self.__session.query(User).filter_by(**kwargs)]