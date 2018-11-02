from dataclasses import dataclass
from typing import Optional

DOUBLE_SIDED_KEY = 'double_sided'
COLOR_KEY = 'color'
COPIES_KEY = 'copies'

@dataclass
class PrintSettings:
    '''Class for keeping track of an item in inventory.'''
    double_sided: bool = True
    copies: int = 1
    color: bool = False

    @staticmethod
    def from_dict(settings_dict: dict):
        if not DOUBLE_SIDED_KEY in settings_dict:
            return None

        if not COLOR_KEY in settings_dict:
            return None

        if not COPIES_KEY in COPIES_KEY:
            return None

        double_sided = settings_dict[DOUBLE_SIDED_KEY]
        color = settings_dict[COLOR_KEY]
        copies = settings_dict[COPIES_KEY]

        return PrintSettings(double_sided, copies, color)

    def to_dict(self) -> dict:
        return {
            DOUBLE_SIDED_KEY: self.double_sided,
            COPIES_KEY: self.copies,
            COLOR_KEY: self.color
        }

    def validate(self) -> bool:
        if not type(self.double_sided) is bool:
            return False

        if not type(self.copies) is int:
            return False

        if self.copies <= 0:
            return False

        if not type(self.color) is bool:
            return False

        return True
