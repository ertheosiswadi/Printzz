from typing import Optional
from print_settings import PrintSettings
from dataclasses import dataclass

DOCUMENT_NAME_KEY = 'document'
USER_AUTH_KEY = 'auth_key'
SETTINGS_KEY = 'settings'

@dataclass
class AddDocRequest:
    '''
    Represents the data received from an add doc request
    '''
    document_name: str
    auth_key: str
    settings: PrintSettings

    @staticmethod
    def from_dict(document_dict: dict):
        keys = [DOCUMENT_NAME_KEY, USER_AUTH_KEY, SETTINGS_KEY]

        for key in keys:
            if not key in document_dict:
                return None

        name = document_dict[DOCUMENT_NAME_KEY]
        auth_key = document_dict[USER_AUTH_KEY]
        settings = PrintSettings.from_dict(document_dict[SETTINGS_KEY])

        if settings is None:
            return None

        return AddDocRequest(name, auth_key, settings)
