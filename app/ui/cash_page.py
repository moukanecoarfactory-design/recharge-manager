"""Page Caisse — suivi du fond de caisse."""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView, QMessageBox, QGraphicsDropShadowEffect,
    QGridLayout, QDialog, QDoubleSpinBox, QDialogButtonBox, QFormLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from app.db.cash_repo import (
    get_cash_balance, get_cash_summary_today, get_cash_movements,
    get_initial_cash, set_initial_cash, reset_cash
)
from app.locales.translations import t, get_current_language
from app.ui.admin_password_dialog import AdminPasswordDialog
from app.ui.styles import (
    btn_secondary, input_style, label_title,
    WHITE, BORDER, TEXT_DARK, TEXT_LIGHT, TEXT_MEDIUM, BG_LIGHT
)


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


class InitialCashDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("✏️ Modifier le fond de caisse")
        self.setMinimumWidth(440)
        self.setStyleSheet(f"QDialog {{ background-color: {WHITE}; }}")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        title = QLabel("✏️ Modifier le fond de caisse initial")
        title.setStyleSheet(f"color: {TEXT_DARK}; font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        hint = QLabel(
            "Le fond de caisse est le montant que tu as en caisse "
            "au démarrage (avant toute transaction)."
        )
        hint.setWordWrap(True)
        hint.setStyleSheet(f"color: {TEXT_LIGHT}; font-size: 12px;")
        layout.addWidget(hint)

        form = QFormLayout()
        form.setSpacing(10)

        self.amount_input = QDoubleSpinBox()
        self.amount_input.setRange(0, 1000000)
        self.amount_input.setDecimals(2)
        self.amount_input.setSuffix(" DH")
        self.amount_input.setValue(get_initial_cash())
        self.amount_input.setMinimumHeight(42)
        self.amount_input.setStyleSheet(input_style())
        form.addRow("Fond de caisse :", self.amount_input)

        layout.addLayout(form)

        self.preview_lbl = QLabel("")
        self.preview_lbl.setStyleSheet(f"""
            background-color: {BG_LIGHT};
            border-radius: 8px;
            padding: 10px;
            color: {TEXT_DARK};
            font-weight: bold;
            font-size: 13px;
        """)
        self.preview_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.preview_lbl)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText("✓ Enregistrer")
        buttons.button(QDialogButtonBox.Cancel).setText("Annuler")
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.amount_input.valueChanged.connect(self._update_preview)
        self._update_preview()

    def _update_preview(self):
        old_initial = get_initial_cash()
        new_initial = self.amount_input.value()
        diff = new_initial - old_initial
        new_balance = get_cash_balance() + diff

        self.preview_lbl.setText(
            f"💰 Nouvelle caisse : {new_balance:.2f} DH"
        )


class CashPage(QWidget):
    def __init__(self):
        super().__init__()
        self.lang = get_current_language()
        L = lambda key: t(key, self.lang)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 24, 24, 24)
        outer.setSpacing(14)

        # Header
        header = QHBoxLayout()
        title = QLabel("💵 Caisse")
        title.setStyleSheet(label_title())
        header.addWidget(title)
        header.addStretch()

        refresh_btn = QPushButton("🔄 " + L("refresh"))
        refresh_btn.setMinimumHeight(40)
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.setStyleSheet(btn_secondary())
        refresh_btn.clicked.connect(self.refresh)
        header.addWidget(refresh_btn)
        outer.addLayout(header)

        # Carte principale
        main_card = QFrame()
        main_card.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0ea5e9, stop:1 #6366f1
                );
                border-radius: 16px;
                border: none;
            }
        """)
        main_card.setMinimumHeight(140)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(24)
        shadow.setColor(QColor(14, 165, 233, 80))
        shadow.setOffset(0, 4)
        main_card.setGraphicsEffect(shadow)

        main_layout = QHBoxLayout(main_card)
        main_layout.setContentsMargins(28, 24, 28, 24)
        main_layout.setSpacing(20)

        left = QVBoxLayout()
        left.setSpacing(4)

        label_lbl = QLabel("💰 CAISSE ACTUELLE")
        label_lbl.setStyleSheet("""
            color: rgba(255, 255, 255, 0.85);
            font-size: 13px;
            font-weight: bold;
            background: transparent;
        """)
        left.addWidget(label_lbl)

        self.balance_lbl = QLabel("0.00 DH")
        self.balance_lbl.setStyleSheet("""
            color: white;
            font-size: 42px;
            font-weight: bold;
            background: transparent;
        """)
        left.addWidget(self.balance_lbl)

        self.sub_lbl = QLabel("")
        self.sub_lbl.setStyleSheet("""
            color: rgba(255, 255, 255, 0.85);
            font-size: 12px;
            background: transparent;
        """)
        left.addWidget(self.sub_lbl)

        main_layout.addLayout(left)
        main_layout.addStretch()

        btn_col = QVBoxLayout()
        btn_col.setSpacing(8)

        edit_btn = QPushButton("✏️ Modifier le fond")
        edit_btn.setMinimumHeight(38)
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                border: 1.5px solid rgba(255, 255, 255, 0.4);
                border-radius: 10px;
                font-weight: bold;
                font-size: 12px;
                padding: 6px 14px;
            }
            QPushButton:hover { background-color: rgba(255, 255, 255, 0.3); }
        """)
        edit_btn.clicked.connect(self.on_edit_initial)
        btn_col.addWidget(edit_btn)

        reset_btn = QPushButton("🗑️ Réinitialiser")
        reset_btn.setMinimumHeight(38)
        reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.15);
                color: white;
                border: 1.5px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                font-weight: bold;
                font-size: 12px;
                padding: 6px 14px;
            }
            QPushButton:hover { background-color: rgba(255, 255, 255, 0.25); }
        """)
        reset_btn.clicked.connect(self.on_reset)
        btn_col.addWidget(reset_btn)

        main_layout.addLayout(btn_col)
        outer.addWidget(main_card)

        self.stats_grid = QGridLayout()
        self.stats_grid.setSpacing(14)
        outer.addLayout(self.stats_grid)

        table_title = QLabel("📋 Derniers mouvements")
        table_title.setStyleSheet(f"color: {TEXT_DARK}; font-size: 15px; font-weight: bold;")
        outer.addWidget(table_title)

        table_card = QFrame()
        table_card.setStyleSheet(f"""
            QFrame {{
                background-color: {WHITE};
                border-radius: 14px;
                border: 1px solid {BORDER};
            }}
        """)
        tl = QVBoxLayout(table_card)
        tl.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Date", "Type", "Détail", "Montant", "Caisse après"
        ])
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {WHITE};
                border: none;
                border-radius: 14px;
                font-size: 13px;
                padding: 4px;
            }}
            QHeaderView::section {{
                background-color: #f8fafc;
                color: {TEXT_LIGHT};
                padding: 12px 10px;
                border: none;
                border-bottom: 2px solid {BORDER};
                font-weight: bold;
                font-size: 11px;
            }}
            QTableWidget::item {{
                padding: 10px 8px;
                border-bottom: 1px solid #f1f5f9;
            }}
        """)

        hh = self.table.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.table.verticalHeader().setDefaultSectionSize(48)

        tl.addWidget(self.table)
        outer.addWidget(table_card, 1)

        self.refresh()

    def refresh(self):
        balance = get_cash_balance()
        initial = get_initial_cash()

        self.balance_lbl.setText(f"{balance:,.2f} DH".replace(",", " "))
        self.sub_lbl.setText(f"Fond initial : {initial:.2f} DH")

        while self.stats_grid.count():
            item = self.stats_grid.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        summary = get_cash_summary_today()

        self.stats_grid.addWidget(StatCard(
            "📥", "Entrées du jour", f"+{summary['in']:.2f} DH",
            "#16a34a", "ventes délaire + cartes"
        ), 0, 0)
        self.stats_grid.addWidget(StatCard(
            "📤", "Sorties du jour", f"-{summary['out']:.2f} DH",
            "#dc2626", "recharges + achats"
        ), 0, 1)
        self.stats_grid.addWidget(StatCard(
            "📊", "Solde net du jour", f"{summary['net']:+.2f} DH",
            "#0ea5e9" if summary['net'] >= 0 else "#dc2626",
            f"{summary['count']} mouvement(s)"
        ), 0, 2)

        movements = get_cash_movements(200)
        self.table.setRowCount(len(movements))

        source_map = {
            "credit_sell": "Vente délaire",
            "credit_buy": "Recharge délaire",
            "card_sell": "Vente carte",
            "card_buy": "Achat carte",
            "manual": "Manuel",
        }

        for row, m in enumerate(movements):
            date_str = str(m["date"])[5:16]
            date_item = QTableWidgetItem(date_str)
            date_item.setToolTip(str(m["date"]))
            self.table.setItem(row, 0, date_item)

            if m["type"] == "in":
                type_item = QTableWidgetItem("📥 Entrée")
                type_item.setForeground(QColor("#16a34a"))
            else:
                type_item = QTableWidgetItem("📤 Sortie")
                type_item.setForeground(QColor("#dc2626"))
            self.table.setItem(row, 1, type_item)

            detail = source_map.get(m["source"], m["source"] or "—")
            self.table.setItem(row, 2, QTableWidgetItem(detail))

            if m["type"] == "in":
                amt = QTableWidgetItem(f"+{m['amount']:.2f} DH")
                amt.setForeground(QColor("#16a34a"))
            else:
                amt = QTableWidgetItem(f"-{m['amount']:.2f} DH")
                amt.setForeground(QColor("#dc2626"))
            amt.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row, 3, amt)

            bal = QTableWidgetItem(f"{m['balance_after']:.2f} DH")
            bal.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row, 4, bal)

    def on_edit_initial(self):
        dlg = AdminPasswordDialog(self, action_text="Modifier le fond de caisse")
        if not dlg.exec():
            return

        edit_dlg = InitialCashDialog(self)
        if not edit_dlg.exec():
            return

        try:
            set_initial_cash(edit_dlg.amount_input.value())
            QMessageBox.information(self, "✅", "Fond de caisse modifié !")
            self.refresh()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def on_reset(self):
        dlg = AdminPasswordDialog(self, action_text="Réinitialiser la caisse")
        if not dlg.exec():
            return

        confirm = QMessageBox.question(
            self, "⚠️ Réinitialiser la caisse",
            "Cette action va SUPPRIMER tous les mouvements de caisse.\n\n"
            "Le fond initial sera conservé.\n\nContinuer ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        try:
            reset_cash()
            QMessageBox.information(self, "✅", "Caisse réinitialisée !")
            self.refresh()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))