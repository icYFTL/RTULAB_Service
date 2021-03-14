from ..models import User
from .. import Session


class UsersMethods:
    def __init__(self):
        self.__session = Session()

    def add_user(self, user: User) -> User:
        self.__session.add(user)
        self.__session.commit()

        return user

    def get_user(self, **kwargs) -> User:
        result = [x for x in self.__session.query(User).filter_by(**kwargs)]
        return result[0] if result else None

    def remove_user(self, user: User) -> None:
        self.__session.delete(user)
        self.__session.commit()
