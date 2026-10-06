"""Repository pour les ajustements manuels de solde."""
from app.db.database import get_connection


def set_operator_balance(operator_id: int, new_balance: float,
                         old_balance: float, notes: str = "") -> int:
    """
    Modifie le solde d'un opérateur manuellement.
    Enregistre aussi l'ajustement dans l'historique et la caisse.
    """
    diff = new_balance - old_balance

    conn = get_connection()

    # 1. Mettre à jour le solde
    conn.execute("""
        UPDATE credit_balances
        SET balance = ?, updated_at = CURRENT_TIMESTAMP
        WHERE operator_id = ?
    """, (new_balance, operator_id))

    # 2. Enregistrer une transaction dans l'historique
    # type = 'adjust' (ni sell ni buy)
    cur = conn.execute("""
        INSERT INTO credit_transactions
        (operator_id, type, amount, paid_amount, profit, notes)
        VALUES (?, 'adjust', ?, ?, 0, ?)
    """, (operator_id, abs(diff), new_balance, notes or f"Ajustement {old_balance:.2f} → {new_balance:.2f}"))
    trans_id = cur.lastrowid

    conn.commit()
    conn.close()

    # 3. Enregistrer dans la caisse (si diff ≠ 0)
    if abs(diff) > 0.01:
        from app.db.cash_repo import add_cash_movement
        if diff > 0:
            # Solde augmenté → tu as "reçu" du délaire gratuit ? Non, c'est juste une correction
            add_cash_movement("out", 0, source="adjust", reference_id=trans_id,
                              notes=f"Ajustement solde {old_balance:.2f} → {new_balance:.2f}")
        else:
            add_cash_movement("in", 0, source="adjust", reference_id=trans_id,
                              notes=f"Ajustement solde {old_balance:.2f} → {new_balance:.2f}")

    return trans_id