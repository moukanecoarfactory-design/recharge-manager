from dataclasses import dataclass
from typing import Optional


@dataclass
class Operator:
    id: Optional[int] = None
    code: str = ""
    name: str = ""
    commission: float = 0.0
    color: str = "#0ea5e9"
    balance: float = 0.0   # Récupéré depuis credit_balances


@dataclass
class CardProduct:
    id: Optional[int] = None
    operator_id: Optional[int] = None
    operator_name: str = ""      # Pour l'affichage
    operator_color: str = ""     # Pour l'affichage
    denomination: float = 0.0    # 5 DH ou 10 DH
    stock: int = 0


@dataclass
class CardPurchase:
    id: Optional[int] = None
    card_product_id: Optional[int] = None
    quantity: int = 0
    unit_price: float = 0.0
    total: float = 0.0
    purchase_date: str = ""
    notes: str = ""


@dataclass
class CardSale:
    id: Optional[int] = None
    card_product_id: Optional[int] = None
    quantity: int = 0
    unit_price: float = 0.0
    total: float = 0.0
    sale_date: str = ""


@dataclass
class CreditTransaction:
    id: Optional[int] = None
    operator_id: Optional[int] = None
    operator_name: str = ""      # Pour l'affichage
    operator_color: str = ""     # Pour l'affichage
    type: str = "sell"           # "sell" (vendre) ou "buy" (recharger)
    amount: float = 0.0
    paid_amount: float = 0.0
    profit: float = 0.0
    transaction_date: str = ""
    notes: str = ""