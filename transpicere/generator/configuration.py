from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Any


class Direction(Enum):
    SOURCE_TO_DEST = '->'
    DEST_TO_SOURCE = '<-'
    BIDIRECTIONAL = '<->'


@dataclass
class Reference:
    source_field: str
    destination_id: str
    direction: Direction


@dataclass
class ConfigImpl:
    pass


@dataclass
class Config:
    conf: ConfigImpl
    references: List[Reference]
