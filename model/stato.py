from dataclasses import dataclass

@dataclass()
class Stato:
    id : str
    name : str
    capital : str
    lat : float
    lng : float
    area : float
    population : int
    neighbors : str
