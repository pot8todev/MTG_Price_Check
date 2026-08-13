
from dataclasses import dataclass, field

@dataclass
class Card:
    name: str
    price: float | None
    edition: str | None
    quality: str | None
    language: str | None
    url: str | None = None

@dataclass
class Stock:
    card: Card
    qnt: int

@dataclass
class Store:
    name: str | None
    address: str | None
    tel_num: str | None
    showcase_url: str | None
    stock: list[Stock] = field(default_factory=list)
