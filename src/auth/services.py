from .models import User
from src.abc import Service


class UserService(Service[User]):

    def get_by_username(self, username: str) -> User | None:
        return self.query.filter(User.username == username).first()
