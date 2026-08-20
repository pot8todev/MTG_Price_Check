
from dataclasses import dataclass, field
from dataclasses import dataclass

@dataclass

class Wish_card:
    quantity: int
    mana_cost: str
    price: str
    image: str
    url: str

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
    diversity: int = 0
    stock: list[Stock] = field(default_factory=list)
