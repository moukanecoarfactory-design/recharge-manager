"""Repository pour les cartes de recharge."""
from typing import List, Optional
from app.db.database import get_connection
from app.core.models import CardProduct


def get_all_cards() -> List[CardProduct]:
    conn = get_connection()
    rows = conn.execute("""
        SELECT cp.id, cp.operator_id, cp.denomination, cp.stock,
               o.name AS operator_name, o.color AS operator_color
        FROM card_products cp
        JOIN operators o ON cp.operator_id = o.id
        ORDER BY o.id, cp.denomination
    """).fetchall()
    conn.close()
    return [CardProduct(
        id=r["id"], operator_id=r["operator_id"],
        operator_name=r["operator_name"], operator_color=r["operator_color"],
        denomination=r["denomination"], stock=r["stock"]
    ) for r in rows]


def get_cards_by_operator(operator_id: int) -> List[CardProduct]:
    conn = get_connection()
    rows = conn.execute("""
        SELECT cp.id, cp.operator_id, cp.denomination, cp.stock,
               o.name AS operator_name, o.color AS operator_color
        FROM card_products cp
        JOIN operators o ON cp.operator_id = o.id
        WHERE cp.operator_id = ?
        ORDER BY cp.denomination
    """, (operator_id,)).fetchall()
    conn.close()
    return [CardProduct(
        id=r["id"], operator_id=r["operator_id"],
        operator_name=r["operator_name"], operator_color=r["operator_color"],
        denomination=r["denomination"], stock=r["stock"]
    ) for r in rows]


def get_card_product(card_id: int) -> Optional[CardProduct]:
    conn = get_connection()
    row = conn.execute("""
        SELECT cp.id, cp.operator_id, cp.denomination, cp.stock,
               o.name AS operator_name, o.color AS operator_color
        FROM card_products cp
        JOIN operators o ON cp.operator_id = o.id
        WHERE cp.id = ?
    """, (card_id,)).fetchone()
    conn.close()
    if not row:
        return None
    return CardProduct(
        id=row["id"], operator_id=row["operator_id"],
        operator_name=row["operator_name"], operator_color=row["operator_color"],
        denomination=row["denomination"], stock=row["stock"]
    )


def add_stock(card_id: int, quantity: int) -> None:
    conn = get_connection()
    conn.execute("UPDATE card_products SET stock = stock + ? WHERE id = ?",
                 (quantity, card_id))
    conn.commit()
    conn.close()


def remove_stock(card_id: int, quantity: int) -> bool:
    conn = get_connection()
    row = conn.execute("SELECT stock FROM card_products WHERE id = ?",
                       (card_id,)).fetchone()
    if not row or row["stock"] < quantity:
        conn.close()
        return False
    conn.execute("UPDATE card_products SET stock = stock - ? WHERE id = ?",
                 (quantity, card_id))
    conn.commit()
    conn.close()
    return True


def set_stock(card_id: int, new_stock: int) -> None:
    """Définit le stock à une valeur précise (modification manuelle)."""
    conn = get_connection()
    conn.execute("UPDATE card_products SET stock = ? WHERE id = ?",
                 (new_stock, card_id))
    conn.commit()
    conn.close()


def clear_stock(card_id: int) -> None:
    """Remet le stock à 0 pour une carte."""
    set_stock(card_id, 0)


def clear_all_stocks() -> None:
    """Remet TOUS les stocks à 0."""
    conn = get_connection()
    conn.execute("UPDATE card_products SET stock = 0")
    conn.commit()
    conn.close()


def get_low_stock_cards(threshold: int = 5) -> List[CardProduct]:
    conn = get_connection()
    rows = conn.execute("""
        SELECT cp.id, cp.operator_id, cp.denomination, cp.stock,
               o.name AS operator_name, o.color AS operator_color
        FROM card_products cp
        JOIN operators o ON cp.operator_id = o.id
        WHERE cp.stock <= ?
        ORDER BY cp.stock ASC
    """, (threshold,)).fetchall()
    conn.close()
    return [CardProduct(
        id=r["id"], operator_id=r["operator_id"],
        operator_name=r["operator_name"], operator_color=r["operator_color"],
        denomination=r["denomination"], stock=r["stock"]
    ) for r in rows]


def get_total_stock() -> int:
    conn = get_connection()
    row = conn.execute("SELECT COALESCE(SUM(stock), 0) AS total FROM card_products").fetchone()
    conn.close()
    return row["total"] if row else 0