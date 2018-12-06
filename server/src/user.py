from .constants import (USERNAME_KEY, USER_ID_KEY,)

from dataclasses import dataclass

@dataclass
class User:
    '''
    Class which contains the username and user_id for a valid user
    '''
    username: str
    user_id: str

    def to_dict(self) -> dict:
        return {
            USERNAME_KEY: self.username,
            USER_ID_KEY: self.user_id
        }
