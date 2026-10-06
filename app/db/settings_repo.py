"""Repository pour les paramètres."""
import hashlib
from app.db.database import get_connection


def get_setting(key: str, default: str = "") -> str:
    conn = get_connection()
    row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
    conn.close()
    return row["value"] if row else default


def set_setting(key: str, value: str) -> None:
    conn = get_connection()
    conn.execute("""
        INSERT INTO settings (key, value) VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
    """, (key, value))
    conn.commit()
    conn.close()


def get_low_balance_alert() -> float:
    try:
        return float(get_setting("low_balance_alert", "50"))
    except ValueError:
        return 50.0


def get_low_stock_alert() -> int:
    try:
        return int(get_setting("low_stock_alert", "5"))
    except ValueError:
        return 5


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_admin_password(password: str) -> bool:
    stored = get_setting("admin_password", "")
    if not stored:
        return False
    return stored == hash_password(password)


def set_admin_password(new_password: str) -> None:
    set_setting("admin_password", hash_password(new_password))