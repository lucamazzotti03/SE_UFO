from dataclasses import dataclass


@dataclass
class Avvistamento:
    id : int
    shape : str
    anno : int
    state : str
