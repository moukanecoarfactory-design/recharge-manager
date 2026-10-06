from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QGridLayout, QPushButton, QGraphicsDropShadowEffect,
    QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QBrush

from app.db.operator_repo import get_all_operators, get_total_balance
from app.db.card_repo import get_all_cards, get_total_stock
from app.db.transaction_repo import (
    get_credit_summary_today, get_card_summary_today,
    get_credit_transactions
)
from app.db.cash_repo import get_cash_balance, get_cash_summary_today
from app.locales.translations import t, get_current_language
from app.ui.logo_widget import OperatorLogo
from app.ui.operator_card import OperatorCard
from app.ui.styles import (
    btn_primary, label_title,
    WHITE, BORDER, TEXT_DARK, TEXT_LIGHT, TEXT_MEDIUM, BG_LIGHT
)


# ============================================================
# BAR CHART avec vraies barres
# ============================================================
class BarChart(QFrame):
    def __init__(self, data: list):
        super().__init__()
        self.data = data
        self.setMinimumHeight(260)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {WHITE};
                border-radius: 14px;
                border: 1px solid {BORDER};
            }}
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 15))
        self.setGraphicsEffect(shadow)

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.data:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        margin_left = 60
        margin_right = 40
        margin_top = 50
        margin_bottom = 70
        w = self.width() - margin_left - margin_right
        h = self.height() - margin_top - margin_bottom

        max_val = max((v for _, v, _ in self.data), default=0)
        if max_val == 0:
            max_val = 1

        n = len(self.data)
        slot_w = w // n
        bar_w = int(slot_w * 0.5)
        min_bar_h = 40

        for i, (label, value, color) in enumerate(self.data):
            if value > 0:
                bar_h = max(min_bar_h, int((value / max_val) * h))
            else:
                bar_h = min_bar_h

            x = margin_left + i * slot_w + (slot_w - bar_w) // 2
            y = margin_top + h - bar_h

            if value > 0:
                painter.setBrush(QBrush(QColor(color)))
            else:
                painter.setBrush(QBrush(QColor("#e2e8f0")))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(x, y, bar_w, bar_h, 10, 10)

            painter.setPen(QColor(color if value > 0 else "#94a3b8"))
            font = painter.font()
            font.setBold(True)
            font.setPointSize(11)
            painter.setFont(font)
            painter.drawText(
                x - 20, y - 30, bar_w + 40, 22,
                Qt.AlignmentFlag.AlignCenter, f"{value:.0f}"
            )

            painter.setPen(QColor(TEXT_MEDIUM))
            font.setPointSize(12)
            painter.setFont(font)
            painter.drawText(
                x - 20, margin_top + h + 15, bar_w + 40, 25,
                Qt.AlignmentFlag.AlignCenter, label
            )


# ============================================================
# STAT CARD
# ============================================================
class StatCard(QFrame):
    def __init__(self, icon, title, value, color="#0ea5e9", subtitle=""):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {WHITE};
                border-radius: 14px;
                border: 1px solid {BORDER};
            }}
        """)
        self.setMinimumHeight(120)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(18)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 15))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(8)

        header = QHBoxLayout()
        header.setSpacing(10)

        icon_lbl = QLabel(icon)
        icon_lbl.setFixedSize(38, 38)
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setStyleSheet(f"""
            background-color: {color}18;
            border-radius: 11px;
            font-size: 18px;
        """)
        header.addWidget(icon_lbl)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"""
            color: {TEXT_LIGHT}; font-size: 12px;
            font-weight: bold; background: transparent;
        """)
        header.addWidget(title_lbl)
        header.addStretch()
        layout.addLayout(header)

        value_lbl = QLabel(value)
        value_lbl.setStyleSheet(f"""
            color: {color}; font-size: 22px;
            font-weight: bold; background: transparent;
        """)
        layout.addWidget(value_lbl)

        if subtitle:
            sub_lbl = QLabel(subtitle)
            sub_lbl.setStyleSheet(f"""
                color: {TEXT_LIGHT}; font-size: 11px;
                background: transparent;
            """)
            layout.addWidget(sub_lbl)


def make_section_header(icon, text):
    container = QWidget()
    container.setStyleSheet("background: transparent;")
    layout = QHBoxLayout(container)
    layout.setContentsMargins(0, 16, 0, 6)
    layout.setSpacing(10)

    icon_lbl = QLabel(icon)
    icon_lbl.setFixedSize(34, 34)
    icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
    icon_lbl.setStyleSheet(f"""
        background-color: {WHITE};
        border-radius: 10px;
        font-size: 16px;
        border: 1px solid {BORDER};
    """)
    layout.addWidget(icon_lbl)

    text_lbl = QLabel(text)
    text_lbl.setStyleSheet(f"""
        color: {TEXT_DARK};
        font-size: 16px;
        font-weight: bold;
        background: transparent;
    """)
    layout.addWidget(text_lbl)

    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFixedHeight(1)
    line.setStyleSheet(f"background-color: {BORDER}; border: none;")
    layout.addWidget(line, 1)
    return container


# ============================================================
# LIGNE STOCK CARTES
# ============================================================
class CardStockRow(QFrame):
    def __init__(self, operator_code, operator_name, color, cards):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {WHITE};
                border-radius: 14px;
                border: 1px solid {BORDER};
            }}
        """)
        self.setMinimumHeight(80)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 12))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(14)

        logo = OperatorLogo(
            code=operator_code, name=operator_name,
            color=color, size=52
        )
        layout.addWidget(logo)

        name_lbl = QLabel(operator_name)
        name_lbl.setStyleSheet(f"""
            color: {TEXT_DARK}; font-size: 15px;
            font-weight: bold; background: transparent;
            min-width: 90px;
        """)
        layout.addWidget(name_lbl)
        layout.addStretch()

        for c in cards:
            denom = int(c.denomination)
            stock = c.stock

            if stock <= 0:
                bg = "#fef2f2"; fg = "#dc2626"; border = "#fecaca"
            elif stock <= 5:
                bg = "#fef3c7"; fg = "#92400e"; border = "#fde68a"
            else:
                bg = "#f0fdf4"; fg = "#166534"; border = "#bbf7d0"

            card_lbl = QLabel(f"{denom} DH : {stock}")
            card_lbl.setStyleSheet(f"""
                color: {fg};
                font-size: 13px;
                font-weight: bold;
                background-color: {bg};
                border: 1px solid {border};
                border-radius: 10px;
                padding: 8px 14px;
                min-width: 80px;
            """)
            card_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(card_lbl)


# ============================================================
# PAGE DASHBOARD
# ============================================================
class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.lang = get_current_language()
        L = lambda key: t(key, self.lang)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 24, 24, 24)
        outer.setSpacing(14)

        header = QHBoxLayout()
        title = QLabel("🏠 " + L("dashboard"))
        title.setStyleSheet(label_title())
        header.addWidget(title)
        header.addStretch()

        refresh_btn = QPushButton("🔄 " + L("refresh"))
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.setMinimumHeight(42)
        refresh_btn.setStyleSheet(btn_primary())
        refresh_btn.clicked.connect(self.refresh)
        header.addWidget(refresh_btn)
        outer.addLayout(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        content = QWidget()
        content.setStyleSheet("background: transparent;")
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(10)

        # ============================================================
        # 🆕 CARTE CAISSE EN HAUT
        # ============================================================
        cash_card = QFrame()
        cash_card.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0ea5e9, stop:1 #6366f1
                );
                border-radius: 16px;
                border: none;
            }
        """)
        cash_card.setMinimumHeight(110)

        cash_shadow = QGraphicsDropShadowEffect()
        cash_shadow.setBlurRadius(20)
        cash_shadow.setColor(QColor(14, 165, 233, 80))
        cash_shadow.setOffset(0, 4)
        cash_card.setGraphicsEffect(cash_shadow)

        cash_layout = QHBoxLayout(cash_card)
        cash_layout.setContentsMargins(24, 18, 24, 18)
        cash_layout.setSpacing(16)

        cash_icon = QLabel("💰")
        cash_icon.setStyleSheet("font-size: 40px; background: transparent;")
        cash_layout.addWidget(cash_icon)

        cash_text_col = QVBoxLayout()
        cash_text_col.setSpacing(2)

        cash_title = QLabel("CAISSE ACTUELLE")
        cash_title.setStyleSheet("""
            color: rgba(255, 255, 255, 0.85);
            font-size: 12px;
            font-weight: bold;
            background: transparent;
        """)
        cash_text_col.addWidget(cash_title)

        self.cash_balance_lbl = QLabel("0.00 DH")
        self.cash_balance_lbl.setStyleSheet("""
            color: white;
            font-size: 34px;
            font-weight: bold;
            background: transparent;
        """)
        cash_text_col.addWidget(self.cash_balance_lbl)

        cash_layout.addLayout(cash_text_col)
        cash_layout.addStretch()

        self.cash_today_lbl = QLabel("")
        self.cash_today_lbl.setStyleSheet("""
            color: white;
            font-size: 15px;
            font-weight: bold;
            background: transparent;
        """)
        self.cash_today_lbl.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        cash_layout.addWidget(self.cash_today_lbl)

        self.content_layout.addWidget(cash_card)

        # ============================================================
        # Cartes opérateurs
        # ============================================================
        self.operators_grid = QGridLayout()
        self.operators_grid.setSpacing(16)
        self.content_layout.addLayout(self.operators_grid)

        self.content_layout.addWidget(make_section_header("📊", L("chart_today")))
        self.chart_container = QVBoxLayout()
        self.chart_container.setSpacing(6)
        self.content_layout.addLayout(self.chart_container)

        self.content_layout.addWidget(make_section_header("🎫", L("cards_in_stock")))
        self.cards_container = QVBoxLayout()
        self.cards_container.setSpacing(10)
        self.content_layout.addLayout(self.cards_container)

        self.content_layout.addWidget(make_section_header("📊", L("today")))
        self.today_grid = QGridLayout()
        self.today_grid.setSpacing(16)
        self.content_layout.addLayout(self.today_grid)

        self.content_layout.addStretch()
        scroll.setWidget(content)
        outer.addWidget(scroll)

        self.refresh()

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

    def refresh(self):
        L = lambda key: t(key, self.lang)

        # ============================================================
        # 🆕 MISE À JOUR CAISSE
        # ============================================================
        try:
            cash_balance = get_cash_balance()
            cash_sum = get_cash_summary_today()
            self.cash_balance_lbl.setText(
                f"{cash_balance:,.2f} DH".replace(",", " ")
            )
            sign = "+" if cash_sum["net"] >= 0 else ""
            self.cash_today_lbl.setText(
                f"Aujourd'hui\n{sign}{cash_sum['net']:.2f} DH"
            )
        except Exception:
            pass

        # ============================================================
        # Cartes opérateurs
        # ============================================================
        self._clear_layout(self.operators_grid)
        operators = get_all_operators()
        for col, op in enumerate(operators):
            card = OperatorCard(op, self.lang, show_recharge=True)
            card.clicked.connect(lambda _: self.refresh())
            self.operators_grid.addWidget(card, 0, col)

        # ============================================================
        # Graphique
        # ============================================================
        self._clear_layout(self.chart_container)
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        today_transactions = get_credit_transactions(500)
        sales_by_op = {}
        for tr in today_transactions:
            if tr["type"] == "sell" and tr["transaction_date"].startswith(today):
                name = tr["operator_name"]
                sales_by_op[name] = sales_by_op.get(name, 0) + tr["amount"]

        chart_data = [(op.name, sales_by_op.get(op.name, 0), op.color)
                      for op in operators]
        chart = BarChart(chart_data)
        self.chart_container.addWidget(chart)

        # ============================================================
        # Cartes en stock
        # ============================================================
        self._clear_layout(self.cards_container)
        cards = get_all_cards()
        by_op = {}
        for c in cards:
            if c.operator_name not in by_op:
                code = "inwi" if "inwi" in c.operator_name.lower() else \
                       "iam" if "iam" in c.operator_name.lower() else "orange"
                by_op[c.operator_name] = {
                    "code": code,
                    "color": c.operator_color,
                    "cards": []
                }
            by_op[c.operator_name]["cards"].append(c)

        for op_name, data in by_op.items():
            self.cards_container.addWidget(
                CardStockRow(data["code"], op_name, data["color"], data["cards"])
            )

        # ============================================================
        # Stats du jour
        # ============================================================
        self._clear_layout(self.today_grid)
        credit = get_credit_summary_today()
        card_sum = get_card_summary_today()
        total_balance = get_total_balance()
        total_stock = get_total_stock()

        cards_data = [
            ("💰", L("sold_credit"), f"{credit['sold']:.2f} DH", "#0ea5e9",
             f"{credit['count']} {L('transactions')}"),
            ("📥", L("bought_credit"), f"{credit['bought']:.2f} DH", "#6366f1",
             L("recharges_today")),
            ("🎫", L("sold_cards"), f"{card_sum['sold']:.2f} DH", "#f97316",
             f"{int(card_sum['sold_qty'])} {L('cards_sold')}"),
            ("💚", L("profit_today"), f"{credit['profit']:.2f} DH", "#16a34a",
             L("net_profit")),
        ]

        for col, (icon, title, value, color, sub) in enumerate(cards_data):
            self.today_grid.addWidget(StatCard(icon, title, value, color, sub), 0, col)

        cards2 = [
            ("💵", L("total_balance"), f"{total_balance:.2f} DH", "#0ea5e9",
             L("on_3_operators")),
            ("📦", L("total_stock"), f"{total_stock}", "#8b5cf6",
             L("all_denominations")),
        ]
        for col, (icon, title, value, color, sub) in enumerate(cards2):
            self.today_grid.addWidget(StatCard(icon, title, value, color, sub), 1, col)