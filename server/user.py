from dataclasses import dataclass

USERNAME_KEY = 'uname'
AUTH_KEY = 'auth_key'

@dataclass
class User:
    username: str
    auth_key: str

    def to_dict(self) -> dict:
        return {
            USERNAME_KEY: self.username,
            AUTH_KEY: self.auth_key
        } 