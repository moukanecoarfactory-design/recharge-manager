"""Repository pour les opérateurs et soldes délaire."""
from typing import List, Optional
from app.db.database import get_connection
from app.core.models import Operator


def get_all_operators() -> List[Operator]:
    """Récupère tous les opérateurs avec leur solde."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT o.id, o.code, o.name, o.commission, o.color,
               COALESCE(cb.balance, 0) AS balance
        FROM operators o
        LEFT JOIN credit_balances cb ON cb.operator_id = o.id
        ORDER BY o.id
    """).fetchall()
    conn.close()
    return [Operator(
        id=r["id"], code=r["code"], name=r["name"],
        commission=r["commission"], color=r["color"],
        balance=r["balance"]
    ) for r in rows]


def get_operator(operator_id: int) -> Optional[Operator]:
    conn = get_connection()
    row = conn.execute("""
        SELECT o.id, o.code, o.name, o.commission, o.color,
               COALESCE(cb.balance, 0) AS balance
        FROM operators o
        LEFT JOIN credit_balances cb ON cb.operator_id = o.id
        WHERE o.id = ?
    """, (operator_id,)).fetchone()
    conn.close()
    if not row:
        return None
    return Operator(
        id=row["id"], code=row["code"], name=row["name"],
        commission=row["commission"], color=row["color"],
        balance=row["balance"]
    )


def update_balance(operator_id: int, new_balance: float) -> None:
    conn = get_connection()
    conn.execute("""
        UPDATE credit_balances SET balance = ?, updated_at = CURRENT_TIMESTAMP
        WHERE operator_id = ?
    """, (new_balance, operator_id))
    conn.commit()
    conn.close()


def add_to_balance(operator_id: int, amount: float) -> None:
    """Ajoute au solde (recharge)."""
    conn = get_connection()
    conn.execute("""
        UPDATE credit_balances
        SET balance = balance + ?, updated_at = CURRENT_TIMESTAMP
        WHERE operator_id = ?
    """, (amount, operator_id))
    conn.commit()
    conn.close()


def subtract_from_balance(operator_id: int, amount: float) -> None:
    """Retire du solde (vente)."""
    conn = get_connection()
    conn.execute("""
        UPDATE credit_balances
        SET balance = balance - ?, updated_at = CURRENT_TIMESTAMP
        WHERE operator_id = ?
    """, (amount, operator_id))
    conn.commit()
    conn.close()


def get_total_balance() -> float:
    """Somme de tous les soldes."""
    conn = get_connection()
    row = conn.execute("SELECT COALESCE(SUM(balance), 0) AS total FROM credit_balances").fetchone()
    conn.close()
    return row["total"] if row else 0.0


def set_balance(operator_id: int, new_balance: float) -> None:
    """Définit le solde à une valeur précise (modification manuelle)."""
    conn = get_connection()
    conn.execute("""
        UPDATE credit_balances
        SET balance = ?, updated_at = CURRENT_TIMESTAMP
        WHERE operator_id = ?
    """, (new_balance, operator_id))
    conn.commit()
    conn.close()