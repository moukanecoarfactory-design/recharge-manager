import sqlite3
import hashlib
from pathlib import Path


# Base de données
DB_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "recharge.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_database():
    """Crée les tables + insère les opérateurs par défaut."""
    conn = get_connection()
    cur = conn.cursor()

    # ---------- Operators ----------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS operators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            commission REAL NOT NULL DEFAULT 0,
            color TEXT DEFAULT '#0ea5e9'
        )
    """)

    # ---------- Credit Balances ----------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS credit_balances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operator_id INTEGER UNIQUE NOT NULL,
            balance REAL NOT NULL DEFAULT 0,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (operator_id) REFERENCES operators(id) ON DELETE CASCADE
        )
    """)

    # ---------- Card Products ----------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS card_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operator_id INTEGER NOT NULL,
            denomination REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            UNIQUE (operator_id, denomination),
            FOREIGN KEY (operator_id) REFERENCES operators(id) ON DELETE CASCADE
        )
    """)

    # ---------- Card Purchases ----------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS card_purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL DEFAULT 0,
            total REAL NOT NULL DEFAULT 0,
            purchase_date TEXT DEFAULT CURRENT_TIMESTAMP,
            notes TEXT,
            FOREIGN KEY (card_product_id) REFERENCES card_products(id) ON DELETE CASCADE
        )
    """)

    # ---------- Card Sales ----------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS card_sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL DEFAULT 0,
            total REAL NOT NULL DEFAULT 0,
            sale_date TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (card_product_id) REFERENCES card_products(id) ON DELETE CASCADE
        )
    """)

    # ---------- Credit Transactions ----------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS credit_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operator_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            paid_amount REAL NOT NULL DEFAULT 0,
            profit REAL NOT NULL DEFAULT 0,
            transaction_date TEXT DEFAULT CURRENT_TIMESTAMP,
            notes TEXT,
            FOREIGN KEY (operator_id) REFERENCES operators(id) ON DELETE CASCADE
        )
    """)

    # ---------- Cash Register ----------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cash_register (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT DEFAULT CURRENT_TIMESTAMP,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            balance_after REAL NOT NULL,
            source TEXT,
            reference_id INTEGER,
            notes TEXT
        )
    """)

    # ---------- Settings ----------
    cur.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)

    # ---------- Default data ----------
    cur.execute("SELECT COUNT(*) FROM operators")
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO operators (code, name, commission, color)
            VALUES (?, ?, ?, ?)
        """, ("inwi", "Inwi", 6.5, "#8b5cf6"))
        inwi_id = cur.lastrowid

        cur.execute("""
            INSERT INTO operators (code, name, commission, color)
            VALUES (?, ?, ?, ?)
        """, ("iam", "IAM", 6.0, "#e30613"))
        iam_id = cur.lastrowid

        cur.execute("""
            INSERT INTO operators (code, name, commission, color)
            VALUES (?, ?, ?, ?)
        """, ("orange", "Orange", 6.5, "#f97316"))
        orange_id = cur.lastrowid

        for op_id in (inwi_id, iam_id, orange_id):
            cur.execute("INSERT INTO credit_balances (operator_id, balance) VALUES (?, 0)", (op_id,))

        for op_id in (inwi_id, iam_id, orange_id):
            cur.execute("INSERT INTO card_products (operator_id, denomination, stock) VALUES (?, 5, 0)", (op_id,))
            cur.execute("INSERT INTO card_products (operator_id, denomination, stock) VALUES (?, 10, 0)", (op_id,))

        cur.execute("INSERT INTO settings (key, value) VALUES ('low_stock_alert', '5')")
        cur.execute("INSERT INTO settings (key, value) VALUES ('low_balance_alert', '50')")
        admin_pw = hashlib.sha256("admin".encode()).hexdigest()
        cur.execute("INSERT INTO settings (key, value) VALUES ('admin_password', ?)", (admin_pw,))
        cur.execute("INSERT INTO settings (key, value) VALUES ('language', 'fr')")
        cur.execute("INSERT INTO settings (key, value) VALUES ('initial_cash', '0')")

        print("✅ Opérateurs, soldes, cartes, caisse et paramètres créés")

    cur.execute("UPDATE operators SET color = '#8b5cf6' WHERE code = 'inwi'")
    cur.execute("UPDATE operators SET color = '#e30613' WHERE code = 'iam'")
    cur.execute("UPDATE operators SET color = '#f97316' WHERE code = 'orange'")

    # 🆕 Migration : force le fond de caisse à 0 si nouveau setting
    cur.execute("SELECT COUNT(*) FROM settings WHERE key = 'initial_cash'")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO settings (key, value) VALUES ('initial_cash', '0')")
        print("✅ Setting 'initial_cash' ajouté (0 DH)")

    conn.commit()
    conn.close()
    print(f"✅ Base prête : {DB_PATH}")


if __name__ == "__main__":
    init_database()