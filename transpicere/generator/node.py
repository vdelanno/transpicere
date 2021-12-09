from dataclasses import dataclass, field
from typing import Callable, Dict


@dataclass
class Field:
    data_type: str
    is_nullable: bool = field(default=True)
    is_list: bool = field(default=False)


@dataclass
class Query:
    return_type: str
    is_list: bool
    resolver: Callable
    params: Dict[str, Field] = field(default_factory=dict)


@dataclass
class Node:
    name: str
    fields: Dict[str, Field]
    queries: Dict[str, Query]
