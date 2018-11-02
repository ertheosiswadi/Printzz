from typing import Optional, Tuple
from print_settings import PrintSettings
from add_doc_request import AddDocRequest
from dataclasses import dataclass
from werkzeug.utils import secure_filename
import user_auth
import uuid
import os

USERNAME_KEY = 'owner'
USER_ID_KEY = 'auth_key'
DOC_NAME_KEY = 'doc_title'
EXTENSION_KEY = 'ext'
DOC_ID_KEY = 'uuid'
PROGRESS_KEY = 'progress'
SETTINGS_KEY = 'settings'

valid_extensions = ['doc', 'docx', 'txt', 'pdf']

def validate_file(filename) -> Optional[Tuple[str, str]]:
    filename = secure_filename(filename)
    _, extension = os.path.splitext(filename)
    extension = extension[1:]
    if not extension in valid_extensions:
        return None

    return (filename, extension,)

@dataclass
class Document:
    username: str
    user_id: str
    name: str
    ext: str
    doc_id: str
    settings: PrintSettings
    progress: float = 0

    @staticmethod
    def from_add_doc_request(request: AddDocRequest):
        file_tuple = validate_file(request.document_name)

        if file_tuple is None:
            return None
        filename, extension = file_tuple

        user = user_auth.get_user(request.auth_key)
        if user is None:
            return None


        return Document(user.username, user.auth_key, filename, extension, \
                        str(uuid.uuid4()), request.settings)

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
        return self.doc_id + '.' + self.ext
