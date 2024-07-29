from .models import User
from src.interfaces import RepositoryInterface


class UserRepository(RepositoryInterface[User]):

    def get_by_username(self, username: str) -> User | None:
        return self.query.filter(User.username == username).first()
