from dataclasses import dataclass

USERNAME_KEY = 'username'
USER_ID_KEY = 'user_id'

@dataclass
class User:
    username: str
    user_id: str

    def to_dict(self) -> dict:
        return {
            USERNAME_KEY: self.username,
            USER_ID_KEY: self.user_id
        }
