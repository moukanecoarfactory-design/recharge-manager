"""Repository pour la caisse (cash register)."""
from typing import List, Dict
from app.db.database import get_connection
from app.db.settings_repo import get_setting, set_setting


def get_initial_cash() -> float:
    try:
        return float(get_setting("initial_cash", "0"))
    except ValueError:
        return 0.0


def set_initial_cash(amount: float):
    set_setting("initial_cash", str(amount))


def get_cash_balance() -> float:
    initial = get_initial_cash()
    conn = get_connection()
    row = conn.execute("""
        SELECT
            COALESCE(SUM(CASE WHEN type = 'in' THEN amount ELSE 0 END), 0) AS total_in,
            COALESCE(SUM(CASE WHEN type = 'out' THEN amount ELSE 0 END), 0) AS total_out
        FROM cash_register
        WHERE type IN ('in', 'out')
    """).fetchone()
    conn.close()
    return initial + row["total_in"] - row["total_out"]


def get_cash_summary_today() -> Dict:
    conn = get_connection()
    row = conn.execute("""
        SELECT
            COALESCE(SUM(CASE WHEN type = 'in' THEN amount ELSE 0 END), 0) AS total_in,
            COALESCE(SUM(CASE WHEN type = 'out' THEN amount ELSE 0 END), 0) AS total_out,
            COUNT(*) AS count
        FROM cash_register
        WHERE type IN ('in', 'out')
        AND DATE(date) = DATE('now', 'localtime')
    """).fetchone()
    conn.close()
    return {
        "in": row["total_in"],
        "out": row["total_out"],
        "net": row["total_in"] - row["total_out"],
        "count": row["count"]
    }


def add_cash_movement(movement_type: str, amount: float,
                      source: str = "", reference_id: int = None,
                      notes: str = ""):
    if amount <= 0:
        return
    current_balance = get_cash_balance()
    if movement_type == "in":
        new_balance = current_balance + amount
    else:
        new_balance = current_balance - amount
    conn = get_connection()
    conn.execute("""
        INSERT INTO cash_register (type, amount, balance_after, source, reference_id, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (movement_type, amount, new_balance, source, reference_id, notes))
    conn.commit()
    conn.close()


def get_cash_movements(limit: int = 200) -> List[Dict]:
    conn = get_connection()
    rows = conn.execute("""
        SELECT * FROM cash_register
        ORDER BY id DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def reset_cash():
    conn = get_connection()
    conn.execute("DELETE FROM cash_register")
    conn.commit()
    conn.close()