from typing import Optional, Tuple
from print_settings import PrintSettings
from dataclasses import dataclass
from werkzeug.utils import secure_filename
from user import User
from constants import  (USERNAME_KEY, USER_ID_KEY, DOC_NAME_KEY, EXTENSION_KEY, DOC_ID_KEY, PROGRESS_KEY, SETTINGS_KEY,)
import user_auth
import uuid
import os

def get_doc_name(doc_id: str, ext: str) -> str:
    return doc_id + '.' + ext

@dataclass
class Document:
    username: str
    user_id: str
    name: str
    ext: str
    doc_id: str
    settings: PrintSettings
    progress: float = 0

    def to_dict(self) -> dict:
        return {
            USERNAME_KEY: self.username,
            USER_ID_KEY: self.user_id,
            DOC_NAME_KEY: self.name,
            EXTENSION_KEY: self.ext,
            DOC_ID_KEY: self.doc_id,
            SETTINGS_KEY: self.settings.to_dict(),
            PROGRESS_KEY: self.progress
        }

    def get_saved_name(self) -> str:
        return get_doc_name(self.doc_id, self.ext)
