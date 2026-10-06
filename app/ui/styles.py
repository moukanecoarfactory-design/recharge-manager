"""Styles centralisés pour toutes les pages."""

# Couleurs principales
PRIMARY = "#0ea5e9"
PRIMARY_DARK = "#0284c7"
SECONDARY = "#6366f1"
SECONDARY_DARK = "#4f46e5"
SUCCESS = "#16a34a"
SUCCESS_DARK = "#15803d"
DANGER = "#dc2626"
DANGER_DARK = "#b91c1c"
WARNING = "#f59e0b"

# Couleurs neutres
TEXT_DARK = "#0f172a"
TEXT_MEDIUM = "#334155"
TEXT_LIGHT = "#64748b"
TEXT_LIGHTER = "#94a3b8"
BG_LIGHT = "#f1f5f9"
BORDER = "#e2e8f0"
WHITE = "#ffffff"


# ============================================================
# BOUTONS
# ============================================================

def btn_primary(text_color="#ffffff"):
    """Bouton principal : gradient bleu-vert."""
    return f"""
        QPushButton {{
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 {PRIMARY}, stop:1 {SECONDARY}
            );
            color: {text_color};
            border: none;
            padding: 10px 22px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 13px;
        }}
        QPushButton:hover {{
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 {PRIMARY_DARK}, stop:1 {SECONDARY_DARK}
            );
        }}
        QPushButton:pressed {{
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #0369a1, stop:1 #4338ca
            );
        }}
    """


def btn_success():
    """Bouton vert (valider, vendre)."""
    return f"""
        QPushButton {{
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 {SUCCESS}, stop:1 #22c55e
            );
            color: white;
            border: none;
            padding: 10px 22px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 13px;
        }}
        QPushButton:hover {{
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 {SUCCESS_DARK}, stop:1 {SUCCESS}
            );
        }}
    """


def btn_danger():
    """Bouton rouge (supprimer)."""
    return f"""
        QPushButton {{
            background: {WHITE};
            color: {DANGER};
            border: 2px solid {DANGER};
            padding: 8px 20px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 13px;
        }}
        QPushButton:hover {{
            background: #fef2f2;
        }}
    """


def btn_secondary():
    """Bouton neutre (annuler, retour)."""
    return f"""
        QPushButton {{
            background: {WHITE};
            color: {TEXT_MEDIUM};
            border: 1px solid {BORDER};
            padding: 10px 22px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 13px;
        }}
        QPushButton:hover {{
            background: {BG_LIGHT};
            border: 1px solid #cbd5e1;
        }}
    """


# ============================================================
# INPUTS
# ============================================================

def input_style():
    """Style pour QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox."""
    return f"""
        QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
            background-color: {WHITE};
            color: {TEXT_DARK};
            border: 2px solid {BORDER};
            border-radius: 10px;
            padding: 8px 14px;
            font-size: 14px;
        }}
        QLineEdit:hover, QComboBox:hover,
        QSpinBox:hover, QDoubleSpinBox:hover {{
            border: 2px solid #cbd5e1;
        }}
        QLineEdit:focus, QComboBox:focus,
        QSpinBox:focus, QDoubleSpinBox:focus {{
            border: 2px solid {SECONDARY};
            background-color: {WHITE};
        }}
    """


# ============================================================
# CARTES
# ============================================================

def card_style(border_left_color=None, elevated=False):
    """Style pour les QFrame cartes."""
    border_left = f"border-left: 4px solid {border_left_color};" if border_left_color else ""
    return f"""
        QFrame {{
            background-color: {WHITE};
            border-radius: 14px;
            border: 1px solid {BORDER};
            {border_left}
        }}
    """


def card_style_alert():
    """Carte en alerte (rouge)."""
    return f"""
        QFrame {{
            background-color: #fef2f2;
            border-radius: 14px;
            border: 2px solid {DANGER};
            border-left: 5px solid {DANGER};
        }}
    """


# ============================================================
# TABLEAUX
# ============================================================

def table_style():
    """Style moderne pour QTableWidget."""
    return f"""
        QTableWidget {{
            background-color: {WHITE};
            border: none;
            border-radius: 12px;
            font-size: 13px;
            padding: 4px;
            gridline-color: transparent;
        }}
        QHeaderView::section {{
            background-color: #f8fafc;
            color: {TEXT_LIGHT};
            padding: 12px 10px;
            border: none;
            border-bottom: 2px solid {BORDER};
            font-weight: bold;
            font-size: 11px;
            text-transform: uppercase;
        }}
        QTableWidget::item {{
            padding: 10px 8px;
            border-bottom: 1px solid #f1f5f9;
        }}
        QTableWidget::item:hover {{
            background-color: #f8fafc;
        }}
        QTableWidget::item:selected {{
            background-color: #eef2ff;
            color: {TEXT_DARK};
        }}
    """


# ============================================================
# LABELS
# ============================================================

def label_title():
    return f"color: {TEXT_DARK}; font-size: 26px; font-weight: bold; background: transparent;"


def label_subtitle():
    return f"color: {TEXT_LIGHT}; font-size: 14px; font-weight: bold; background: transparent;"


def label_field():
    return f"color: {TEXT_MEDIUM}; font-size: 13px; font-weight: bold; background: transparent;"


def label_value(color=None):
    c = color or TEXT_DARK
    return f"color: {c}; font-size: 20px; font-weight: bold; background: transparent;"


# ============================================================
# SECTION HEADER
# ============================================================

def section_header_style():
    return f"""
        color: {TEXT_DARK};
        font-size: 16px;
        font-weight: bold;
        background: transparent;
    """