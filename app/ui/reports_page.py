"""Rapports — design PRO SOFT."""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QGridLayout, QGraphicsDropShadowEffect, QScrollArea, QPushButton,
    QProgressBar
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from app.db.operator_repo import get_all_operators
from app.db.card_repo import get_total_stock
from app.db.transaction_repo import (
    get_credit_transactions, get_card_sales, get_card_purchases
)
from app.locales.translations import t, get_current_language
from app.ui.styles import (
    btn_secondary,
    WHITE, BORDER, TEXT_DARK, TEXT_LIGHT, TEXT_MEDIUM, BG_LIGHT
)
from app.ui.logo_widget import OperatorLogo
from datetime import datetime, timedelta


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
        self.setMinimumHeight(110)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(18)
        shadow.setColor(QColor(0, 0, 0, 15))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(6)

        header = QHBoxLayout()
        header.setSpacing(10)

        icon_lbl = QLabel(icon)
        icon_lbl.setFixedSize(34, 34)
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setStyleSheet(f"""
            background-color: {color}18;
            border-radius: 9px;
            font-size: 17px;
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
            color: {color}; font-size: 24px;
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


class HorizontalBarChart(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {WHITE};
                border-radius: 14px;
                border: 1px solid {BORDER};
            }}
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(18)
        shadow.setColor(QColor(0, 0, 0, 15))
        self.setGraphicsEffect(shadow)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 20, 24, 20)
        self.layout.setSpacing(16)

    def set_data(self, data):
        while self.layout.count():
            item = self.layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        max_val = max((v for _, v, _, _ in data), default=0)
        if max_val == 0:
            max_val = 1

        for label, value, color, comm in data:
            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(14)

            name_lbl = QLabel(label)
            name_lbl.setFixedWidth(100)
            name_lbl.setStyleSheet(f"""
                color: {color}; font-size: 14px;
                font-weight: bold; background: transparent;
            """)
            row_layout.addWidget(name_lbl)

            bar_container = QFrame()
            bar_container.setFixedHeight(34)
            bar_container.setStyleSheet(f"""
                QFrame {{
                    background-color: {BG_LIGHT};
                    border-radius: 10px;
                    border: none;
                }}
            """)
            bar_layout = QHBoxLayout(bar_container)
            bar_layout.setContentsMargins(0, 0, 0, 0)
            bar_layout.setSpacing(0)

            fill = QFrame()
            fill.setStyleSheet(f"""
                QFrame {{
                    background-color: {color};
                    border-radius: 10px;
                }}
            """)
            fill.setFixedWidth(max(6, int((value / max_val) * 300)))
            bar_layout.addWidget(fill)
            bar_layout.addStretch()

            row_layout.addWidget(bar_container, 1)

            value_lbl = QLabel(f"{value:.2f} DH")
            value_lbl.setFixedWidth(110)
            value_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            value_lbl.setStyleSheet(f"""
                color: {TEXT_DARK}; font-size: 14px;
                font-weight: bold; background: transparent;
            """)
            row_layout.addWidget(value_lbl)

            self.layout.addWidget(row)


class OperatorDetailCard(QFrame):
    def __init__(self, op, ventes, total_ventes):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {WHITE};
                border-radius: 16px;
                border: 1px solid {BORDER};
            }}
        """)
        self.setMinimumHeight(240)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(18)
        shadow.setColor(QColor(0, 0, 0, 18))
        shadow.setOffset(0, 3)
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 14, 20, 18)   # 🆕 marge haut réduite
        layout.setSpacing(8)                         # 🆕 spacing réduit

        header = QHBoxLayout()
        header.setSpacing(14)

        logo = OperatorLogo(
            code=op.code, name=op.name,
            color=op.color, size=52
        )
        header.addWidget(logo, 0, Qt.AlignmentFlag.AlignTop)   # 🆕 logo aligné en haut

        name_col = QVBoxLayout()
        name_col.setSpacing(2)
        name_col.setAlignment(Qt.AlignmentFlag.AlignTop)       # 🆕 texte aligné en haut

        name_lbl = QLabel(op.name)
        name_lbl.setStyleSheet(f"""
            color: {op.color}; font-size: 18px;
            font-weight: bold; background: transparent;
        """)
        name_col.addWidget(name_lbl)

        comm_badge = QLabel(f"Commission : {op.commission}%")
        comm_badge.setStyleSheet(f"""
            color: {op.color}; font-size: 11px;
            font-weight: bold; background: transparent;
        """)
        name_col.addWidget(comm_badge)

        header.addLayout(name_col)
        header.addStretch()
        layout.addLayout(header)
        layout.addSpacing(4)                                   # 🆕 espace après header

        balance_lbl = QLabel(f"{op.balance:.2f} DH")
        balance_lbl.setStyleSheet(f"""
            color: {TEXT_DARK}; font-size: 26px;
            font-weight: bold; background: transparent;
        """)
        layout.addWidget(balance_lbl)

        sub_lbl = QLabel("💰 Solde actuel")
        sub_lbl.setStyleSheet(f"""
            color: {TEXT_LIGHT}; font-size: 11px;
            background: transparent;
        """)
        layout.addWidget(sub_lbl)

        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet(f"background-color: {BORDER};")
        layout.addWidget(sep)

        v_layout = QHBoxLayout()
        v_lbl = QLabel("📈 Ventes")
        v_lbl.setStyleSheet(f"color: {TEXT_MEDIUM}; font-size: 13px; background: transparent;")
        v_layout.addWidget(v_lbl)
        v_layout.addStretch()
        v_val = QLabel(f"{ventes:.2f} DH")
        v_val.setStyleSheet(f"color: {TEXT_DARK}; font-size: 13px; font-weight: bold; background: transparent;")
        v_layout.addWidget(v_val)
        layout.addLayout(v_layout)

        p_layout = QHBoxLayout()
        p_lbl = QLabel("🏆 Part de marché")
        p_lbl.setStyleSheet(f"color: {TEXT_MEDIUM}; font-size: 13px; background: transparent;")
        p_layout.addWidget(p_lbl)
        p_layout.addStretch()
        percent = int((ventes / total_ventes * 100)) if total_ventes > 0 else 0
        p_val = QLabel(f"{percent}%")
        p_val.setStyleSheet(f"color: {op.color}; font-size: 13px; font-weight: bold; background: transparent;")
        p_layout.addWidget(p_val)
        layout.addLayout(p_layout)

        bar = QProgressBar()
        bar.setRange(0, 100)
        bar.setValue(percent)
        bar.setTextVisible(False)
        bar.setFixedHeight(10)
        bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: {BG_LIGHT};
                border-radius: 5px;
                border: none;
            }}
            QProgressBar::chunk {{
                background-color: {op.color};
                border-radius: 5px;
            }}
        """)
        layout.addWidget(bar)
        layout.addStretch()


class ReportsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.lang = get_current_language()
        self.current_period = "today"
        L = lambda key: t(key, self.lang)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 24, 24, 24)
        outer.setSpacing(14)

        header = QHBoxLayout()
        title = QLabel("📊 " + L("reports_title"))
        title.setStyleSheet("color: #0f172a; font-size: 26px; font-weight: bold;")
        header.addWidget(title)
        header.addStretch()

        refresh_btn = QPushButton("🔄 " + L("refresh"))
        refresh_btn.setMinimumHeight(40)
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.setStyleSheet(btn_secondary())
        refresh_btn.clicked.connect(self.refresh)
        header.addWidget(refresh_btn)
        outer.addLayout(header)

        periods_row = QHBoxLayout()
        periods_row.setSpacing(8)

        self.period_buttons = {}
        periods = [
            ("📅 " + L("today"), "today"),
            ("📅 7 jours", "7d"),
            ("📅 30 jours", "30d"),
            ("📅 " + L("all"), "all"),
        ]
        for label, pid in periods:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setMinimumHeight(38)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #ffffff;
                    color: #334155;
                    border: 1px solid #e2e8f0;
                    border-radius: 10px;
                    padding: 8px 18px;
                    font-weight: bold;
                    font-size: 13px;
                }
                QPushButton:hover { background-color: #f1f5f9; }
                QPushButton:checked {
                    background-color: #0ea5e915;
                    color: #0ea5e9;
                    border: 1.5px solid #0ea5e9;
                }
            """)
            btn.clicked.connect(lambda _, p=pid: self.on_period_change(p))
            self.period_buttons[pid] = btn
            periods_row.addWidget(btn)

        self.period_buttons["today"].setChecked(True)
        periods_row.addStretch()
        outer.addLayout(periods_row)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        content = QWidget()
        content.setStyleSheet("background: transparent;")
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(18)

        self.stats_grid = QGridLayout()
        self.stats_grid.setSpacing(14)
        self.content_layout.addLayout(self.stats_grid)

        chart_title = QLabel("📊 " + L("sold_credit") + " par opérateur")
        chart_title.setStyleSheet("color: #0f172a; font-size: 15px; font-weight: bold;")
        self.content_layout.addWidget(chart_title)

        self.chart = HorizontalBarChart()
        self.content_layout.addWidget(self.chart)

        detail_title = QLabel("📱 " + L("operator_detail"))
        detail_title.setStyleSheet("color: #0f172a; font-size: 15px; font-weight: bold;")
        self.content_layout.addWidget(detail_title)

        self.operators_grid = QGridLayout()
        self.operators_grid.setSpacing(14)
        self.content_layout.addLayout(self.operators_grid)

        self.content_layout.addStretch()
        scroll.setWidget(content)
        outer.addWidget(scroll)

        self.refresh()

    def on_period_change(self, period):
        self.current_period = period
        for pid, btn in self.period_buttons.items():
            btn.setChecked(pid == period)
        self.refresh()

    def _filter_by_period(self, transactions, date_key):
        if self.current_period == "all":
            return transactions
        now = datetime.now()
        if self.current_period == "today":
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif self.current_period == "7d":
            start = now - timedelta(days=7)
        elif self.current_period == "30d":
            start = now - timedelta(days=30)
        else:
            return transactions
        start_str = start.strftime("%Y-%m-%d %H:%M:%S")
        return [tr for tr in transactions if tr[date_key] >= start_str]

    def refresh(self):
        L = lambda key: t(key, self.lang)
        operators = get_all_operators()
        credit_tr = self._filter_by_period(get_credit_transactions(2000), "transaction_date")
        card_sales = self._filter_by_period(get_card_sales(2000), "sale_date")
        card_purchases = self._filter_by_period(get_card_purchases(2000), "purchase_date")

        total_ca = 0.0
        total_profit = 0.0
        nb_trans = len(credit_tr) + len(card_sales) + len(card_purchases)
        ventes_by_op = {op.id: 0.0 for op in operators}

        for tr in credit_tr:
            total_ca += tr["amount"]
            total_profit += tr["profit"]
            if tr["type"] == "sell":
                ventes_by_op[tr["operator_id"]] += tr["amount"]

        for s in card_sales:
            total_ca += s["total"]

        stock = get_total_stock()

        while self.stats_grid.count():
            item = self.stats_grid.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        self.stats_grid.addWidget(StatCard("💰", "Chiffre d'affaires", f"{total_ca:.2f} DH", "#0ea5e9", f"{nb_trans} transactions"), 0, 0)
        self.stats_grid.addWidget(StatCard("💚", "Bénéfice net", f"+{total_profit:.2f} DH", "#16a34a", "commissions gagnées"), 0, 1)
        self.stats_grid.addWidget(StatCard("📋", "Transactions", f"{nb_trans}", "#6366f1", "toutes opérations"), 0, 2)
        self.stats_grid.addWidget(StatCard("📦", "Stock cartes", f"{stock}", "#f97316", "unités disponibles"), 0, 3)

        chart_data = [(op.name, ventes_by_op[op.id], op.color, op.commission) for op in operators]
        self.chart.set_data(chart_data)

        while self.operators_grid.count():
            item = self.operators_grid.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        total_ventes = sum(ventes_by_op.values())
        for i, op in enumerate(operators):
            card = OperatorDetailCard(op, ventes_by_op[op.id], total_ventes)
            self.operators_grid.addWidget(card, 0, i)