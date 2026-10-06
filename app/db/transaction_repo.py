"""Repository pour les transactions (délaire + cartes)."""
from typing import List, Dict
from app.db.database import get_connection


# ============================================================
# DÉLAIRE
# ============================================================

def sell_credit(operator_id: int, amount: float, notes: str = "") -> int:
    conn = get_connection()
    op = conn.execute("SELECT commission FROM operators WHERE id = ?", (operator_id,)).fetchone()
    if not op:
        conn.close()
        raise ValueError("Opérateur introuvable")
    commission = op["commission"]
    profit = amount * (commission / 100)

    cur = conn.execute("""
        INSERT INTO credit_transactions
        (operator_id, type, amount, paid_amount, profit, notes)
        VALUES (?, 'sell', ?, ?, ?, ?)
    """, (operator_id, amount, amount, profit, notes))
    sale_id = cur.lastrowid

    conn.execute("""
        UPDATE credit_balances SET balance = balance - ?, updated_at = CURRENT_TIMESTAMP
        WHERE operator_id = ?
    """, (amount, operator_id))

    conn.commit()
    conn.close()

    # Caisse : ENTRÉE (client paye)
    from app.db.cash_repo import add_cash_movement
    add_cash_movement("in", amount, source="credit_sell",
                      reference_id=sale_id, notes=notes)
    return sale_id


def buy_credit(operator_id: int, amount: float, notes: str = "") -> int:
    conn = get_connection()
    op = conn.execute("SELECT commission FROM operators WHERE id = ?", (operator_id,)).fetchone()
    if not op:
        conn.close()
        raise ValueError("Opérateur introuvable")
    commission = op["commission"]
    profit = amount * (commission / 100)
    paid = amount - profit

    cur = conn.execute("""
        INSERT INTO credit_transactions
        (operator_id, type, amount, paid_amount, profit, notes)
        VALUES (?, 'buy', ?, ?, ?, ?)
    """, (operator_id, amount, paid, profit, notes))
    purchase_id = cur.lastrowid

    conn.execute("""
        UPDATE credit_balances SET balance = balance + ?, updated_at = CURRENT_TIMESTAMP
        WHERE operator_id = ?
    """, (amount, operator_id))

    conn.commit()
    conn.close()

    # Caisse : SORTIE (tu payes l'opérateur, hors commission)
    from app.db.cash_repo import add_cash_movement
    add_cash_movement("out", paid, source="credit_buy",
                      reference_id=purchase_id, notes=notes)
    return purchase_id


def get_credit_transactions(limit: int = 100) -> List[Dict]:
    conn = get_connection()
    rows = conn.execute("""
        SELECT ct.*, o.name AS operator_name, o.color AS operator_color
        FROM credit_transactions ct
        JOIN operators o ON ct.operator_id = o.id
        ORDER BY ct.id DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_credit_summary_today() -> Dict:
    conn = get_connection()
    row = conn.execute("""
        SELECT
            COALESCE(SUM(CASE WHEN type = 'sell' THEN amount ELSE 0 END), 0) AS sold,
            COALESCE(SUM(CASE WHEN type = 'buy' THEN amount ELSE 0 END), 0) AS bought,
            COALESCE(SUM(profit), 0) AS profit,
            COUNT(*) AS count
        FROM credit_transactions
        WHERE DATE(transaction_date) = DATE('now', 'localtime')
    """).fetchone()
    conn.close()
    return {"sold": row["sold"], "bought": row["bought"],
            "profit": row["profit"], "count": row["count"]}


# ============================================================
# CARTES
# ============================================================

def buy_cards(card_product_id: int, quantity: int,
              unit_price: float = 0, notes: str = "") -> int:
    conn = get_connection()
    if unit_price <= 0:
        prod = conn.execute(
            "SELECT denomination FROM card_products WHERE id = ?", (card_product_id,)
        ).fetchone()
        unit_price = prod["denomination"] if prod else 0

    total = quantity * unit_price
    cur = conn.execute("""
        INSERT INTO card_purchases
        (card_product_id, quantity, unit_price, total, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (card_product_id, quantity, unit_price, total, notes))
    purchase_id = cur.lastrowid

    conn.execute("UPDATE card_products SET stock = stock + ? WHERE id = ?",
                 (quantity, card_product_id))
    conn.commit()
    conn.close()

    # Caisse : SORTIE (tu payes le fournisseur)
    from app.db.cash_repo import add_cash_movement
    add_cash_movement("out", total, source="card_buy",
                      reference_id=purchase_id, notes=notes)
    return purchase_id


def sell_cards(card_product_id: int, quantity: int) -> int:
    conn = get_connection()
    prod = conn.execute(
        "SELECT stock, denomination FROM card_products WHERE id = ?",
        (card_product_id,)
    ).fetchone()
    if not prod:
        conn.close()
        raise ValueError("Carte introuvable")
    if prod["stock"] < quantity:
        conn.close()
        raise ValueError(f"Stock insuffisant ({prod['stock']} restantes)")

    unit_price = prod["denomination"]
    total = quantity * unit_price

    cur = conn.execute("""
        INSERT INTO card_sales
        (card_product_id, quantity, unit_price, total)
        VALUES (?, ?, ?, ?)
    """, (card_product_id, quantity, unit_price, total))
    sale_id = cur.lastrowid

    conn.execute("UPDATE card_products SET stock = stock - ? WHERE id = ?",
                 (quantity, card_product_id))
    conn.commit()
    conn.close()

    # Caisse : ENTRÉE (client paye)
    from app.db.cash_repo import add_cash_movement
    add_cash_movement("in", total, source="card_sell",
                      reference_id=sale_id)
    return sale_id


def get_card_sales(limit: int = 100) -> List[Dict]:
    conn = get_connection()
    rows = conn.execute("""
        SELECT cs.*, cp.denomination, cp.operator_id, o.name AS operator_name
        FROM card_sales cs
        JOIN card_products cp ON cs.card_product_id = cp.id
        JOIN operators o ON cp.operator_id = o.id
        ORDER BY cs.id DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_card_purchases(limit: int = 100) -> List[Dict]:
    conn = get_connection()
    rows = conn.execute("""
        SELECT cp.*, c.denomination, o.name AS operator_name
        FROM card_purchases cp
        JOIN card_products c ON cp.card_product_id = c.id
        JOIN operators o ON c.operator_id = o.id
        ORDER BY cp.id DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_card_summary_today() -> Dict:
    conn = get_connection()
    sold_row = conn.execute("""
        SELECT COALESCE(SUM(total), 0) AS total, COALESCE(SUM(quantity), 0) AS qty
        FROM card_sales
        WHERE DATE(sale_date) = DATE('now', 'localtime')
    """).fetchone()
    bought_row = conn.execute("""
        SELECT COALESCE(SUM(total), 0) AS total, COALESCE(SUM(quantity), 0) AS qty
        FROM card_purchases
        WHERE DATE(purchase_date) = DATE('now', 'localtime')
    """).fetchone()
    conn.close()
    return {
        "sold": sold_row["total"], "sold_qty": sold_row["qty"],
        "bought": bought_row["total"], "bought_qty": bought_row["qty"]
    }


# ============================================================
# SUPPRESSION / MODIFICATION
# ============================================================

def delete_credit_transaction(trans_id: int) -> None:
    """Supprime une transaction délaire et annule son effet sur le solde."""
    conn = get_connection()
    tr = conn.execute(
        "SELECT operator_id, type, amount FROM credit_transactions WHERE id = ?",
        (trans_id,)
    ).fetchone()
    if not tr:
        conn.close()
        raise ValueError("Transaction introuvable")

    if tr["type"] == "buy":
        conn.execute("""
            UPDATE credit_balances SET balance = balance - ?
            WHERE operator_id = ?
        """, (tr["amount"], tr["operator_id"]))
    else:
        conn.execute("""
            UPDATE credit_balances SET balance = balance + ?
            WHERE operator_id = ?
        """, (tr["amount"], tr["operator_id"]))

    conn.execute("DELETE FROM credit_transactions WHERE id = ?", (trans_id,))
    conn.commit()
    conn.close()


def delete_card_sale(sale_id: int) -> None:
    """Supprime une vente de carte et remet le stock."""
    conn = get_connection()
    sale = conn.execute(
        "SELECT card_product_id, quantity FROM card_sales WHERE id = ?",
        (sale_id,)
    ).fetchone()
    if not sale:
        conn.close()
        raise ValueError("Vente introuvable")

    conn.execute("""
        UPDATE card_products SET stock = stock + ?
        WHERE id = ?
    """, (sale["quantity"], sale["card_product_id"]))

    conn.execute("DELETE FROM card_sales WHERE id = ?", (sale_id,))
    conn.commit()
    conn.close()


def delete_card_purchase(purchase_id: int) -> None:
    """Supprime un achat de carte et retire du stock."""
    conn = get_connection()
    purchase = conn.execute(
        "SELECT card_product_id, quantity FROM card_purchases WHERE id = ?",
        (purchase_id,)
    ).fetchone()
    if not purchase:
        conn.close()
        raise ValueError("Achat introuvable")

    conn.execute("""
        UPDATE card_products
        SET stock = MAX(0, stock - ?)
        WHERE id = ?
    """, (purchase["quantity"], purchase["card_product_id"]))

    conn.execute("DELETE FROM card_purchases WHERE id = ?", (purchase_id,))
    conn.commit()
    conn.close()


def update_credit_transaction(trans_id: int, new_amount: float) -> None:
    """Modifie le montant d'une transaction et recalcule le solde."""
    conn = get_connection()
    tr = conn.execute(
        "SELECT operator_id, type, amount FROM credit_transactions WHERE id = ?",
        (trans_id,)
    ).fetchone()
    if not tr:
        conn.close()
        raise ValueError("Transaction introuvable")

    op = conn.execute(
        "SELECT commission FROM operators WHERE id = ?", (tr["operator_id"],)
    ).fetchone()
    commission = op["commission"] if op else 0

    old_amount = tr["amount"]
    diff = new_amount - old_amount
    new_profit = new_amount * (commission / 100)
    new_paid = new_amount - new_profit if tr["type"] == "buy" else new_amount

    if tr["type"] == "buy":
        conn.execute("""
            UPDATE credit_balances SET balance = balance + ?
            WHERE operator_id = ?
        """, (diff, tr["operator_id"]))
    else:
        conn.execute("""
            UPDATE credit_balances SET balance = balance - ?
            WHERE operator_id = ?
        """, (diff, tr["operator_id"]))

    conn.execute("""
        UPDATE credit_transactions
        SET amount = ?, paid_amount = ?, profit = ?
        WHERE id = ?
    """, (new_amount, new_paid, new_profit, trans_id))

    conn.commit()
    conn.close()


# ============================================================
# AJUSTEMENT MANUEL DE SOLDE
# ============================================================

def adjust_operator_balance(operator_id: int, old_balance: float,
                             new_balance: float, notes: str = "") -> int:
    """Ajuste manuellement le solde d'un opérateur."""
    conn = get_connection()
    diff = new_balance - old_balance

    # Mettre à jour le solde
    conn.execute("""
        UPDATE credit_balances
        SET balance = ?, updated_at = CURRENT_TIMESTAMP
        WHERE operator_id = ?
    """, (new_balance, operator_id))

    # Enregistrer dans l'historique
    cur = conn.execute("""
        INSERT INTO credit_transactions
        (operator_id, type, amount, paid_amount, profit, notes)
        VALUES (?, 'adjust', ?, ?, 0, ?)
    """, (
        operator_id,
        abs(diff),
        new_balance,
        notes or f"Ajustement : {old_balance:.2f} -> {new_balance:.2f} DH"
    ))
    trans_id = cur.lastrowid

    conn.commit()
    conn.close()
    return trans_id


# ============================================================
# VIDER TOUT (RESET COMPLET)
# ============================================================

def clear_all_transactions() -> dict:
    """
    Vide TOUTES les transactions (délaire + cartes).
    - Remet tous les soldes à 0
    - Remet tous les stocks de cartes à 0
    - Supprime toutes les transactions
    - Vide aussi la caisse
    """
    conn = get_connection()
    stats = {}

    stats["credit_count"] = conn.execute(
        "SELECT COUNT(*) FROM credit_transactions"
    ).fetchone()[0]
    stats["card_sales_count"] = conn.execute(
        "SELECT COUNT(*) FROM card_sales"
    ).fetchone()[0]
    stats["card_purchases_count"] = conn.execute(
        "SELECT COUNT(*) FROM card_purchases"
    ).fetchone()[0]

    conn.execute("DELETE FROM credit_transactions")
    conn.execute("DELETE FROM card_sales")
    conn.execute("DELETE FROM card_purchases")

    conn.execute("UPDATE credit_balances SET balance = 0")
    conn.execute("UPDATE card_products SET stock = 0")

    # Vider la caisse
    conn.execute("DELETE FROM cash_register")

    conn.commit()
    conn.close()
    return stats