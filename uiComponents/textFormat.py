from dataclasses import dataclass
from enum import Enum


class Format(Enum):
    NONE: int = -1
    
    BOLD: int = 0
    BOLD_OFF: int = 1
    
    ITALIC: int = 2
    ITALIC_OFF: int = 3
    
    COLOR: int = 4
    COLOR_OFF: int = 5
    
    NEW_LINE: int = 6
    
    EFFECT_NAME: int = 7
    EFFECT_NAME_OFF: int = 8
    
@dataclass
class FormatData():
    format_type: Format
    data: str
    
    def __init__(self, format_type: Format, data: str) -> None:
        self.format_type = format_type
        self.data = data
    
    def __repr__(self) -> str:
        return f'FormatData: type: {self.format_type}, data: {self.data}'