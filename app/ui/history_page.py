"""Historique de toutes les transactions avec design V2."""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView, QPushButton, QMessageBox,
    QGraphicsDropShadowEffect, QGridLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

from app.db.transaction_repo import (
    get_credit_transactions, get_card_sales, get_card_purchases,
    delete_credit_transaction, delete_card_sale, delete_card_purchase,
    update_credit_transaction, clear_all_transactions,
    get_credit_summary_today, get_card_summary_today
)
from app.locales.translations import t, get_current_language
from app.ui.admin_password_dialog import AdminPasswordDialog
from app.ui.edit_transaction_dialog import EditTransactionDialog
from app.ui.styles import (
    btn_primary, btn_secondary, btn_success,
    label_title, label_field,
    WHITE, BORDER, TEXT_DARK, TEXT_LIGHT, TEXT_MEDIUM, BG_LIGHT
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
                border-radius: 12px;
                border: 1px solid {BORDER};
                border-left: 5px solid {color};
            }}
        """)
        self.setMinimumHeight(95)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
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
            background-color: {color}22;
            border-radius: 9px;
            font-size: 17px;
        """)
        header.addWidget(icon_lbl)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"""
            color: {TEXT_LIGHT};
            font-size: 12px;
            font-weight: bold;
            background: transparent;
        """)
        header.addWidget(title_lbl)
        header.addStretch()
        layout.addLayout(header)

        value_lbl = QLabel(value)
        value_lbl.setStyleSheet(f"""
            color: {color};
            font-size: 22px;
            font-weight: bold;
            background: transparent;
        """)
        layout.addWidget(value_lbl)

        if subtitle:
            sub_lbl = QLabel(subtitle)
            sub_lbl.setStyleSheet(f"""
                color: {TEXT_LIGHT};
                font-size: 11px;
                background: transparent;
            """)
            layout.addWidget(sub_lbl)


# ============================================================
# BOUTON FILTRE SEGMENTÉ
# ============================================================
class FilterButton(QPushButton):
    def __init__(self, label, filter_id, on_click):
        super().__init__(label)
        self.filter_id = filter_id
        self.setCheckable(True)
        self.setMinimumHeight(38)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(lambda: on_click(filter_id))
        self._apply_style()

    def _apply_style(self):
        self.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #334155;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 18px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #f1f5f9;
                border: 1px solid #cbd5e1;
            }
            QPushButton:checked {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0ea5e9, stop:1 #6366f1
                );
                color: white;
                border: 1px solid #0ea5e9;
            }
        """)


# ============================================================
# PAGE HISTORIQUE V2
# ============================================================
class HistoryPage(QWidget):
    def __init__(self):
        super().__init__()
        self.lang = get_current_language()
        self.current_filter = "all"
        L = lambda key: t(key, self.lang)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 24, 24, 24)
        outer.setSpacing(14)

        # ============================================================
        # HEADER
        # ============================================================
        header = QHBoxLayout()
        title = QLabel("📜 " + L("history_title"))
        title.setStyleSheet(label_title())
        header.addWidget(title)
        header.addStretch()

        # Filtres segmentés
        self.filter_buttons = {}
        for label, fid in [
            ("📋 " + L("all"), "all"),
            ("💰 " + L("credit"), "credit"),
            ("🎫 " + L("card"), "card"),
        ]:
            btn = FilterButton(label, fid, self.on_filter_change)
            self.filter_buttons[fid] = btn
            header.addWidget(btn)

        self.filter_buttons["all"].setChecked(True)

        header.addSpacing(10)

        # Refresh
        refresh_btn = QPushButton("🔄 " + L("refresh"))
        refresh_btn.setMinimumHeight(40)
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.setStyleSheet(btn_secondary())
        refresh_btn.clicked.connect(self.refresh)
        header.addWidget(refresh_btn)

        # Vider tout
        clear_btn = QPushButton("🗑️ " + L("clear_all"))
        clear_btn.setMinimumHeight(40)
        clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #dc2626;
                border: 2px solid #fecaca;
                padding: 8px 16px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #fef2f2;
                border: 2px solid #dc2626;
            }
        """)
        clear_btn.clicked.connect(self.on_clear_all)
        header.addWidget(clear_btn)

        outer.addLayout(header)

        # ============================================================
        # STAT CARDS (résumé du jour)
        # ============================================================
        self.stats_grid = QGridLayout()
        self.stats_grid.setSpacing(14)
        outer.addLayout(self.stats_grid)

        # ============================================================
        # TABLEAU
        # ============================================================
        table_card = QFrame()
        table_card.setStyleSheet(f"""
            QFrame {{
                background-color: {WHITE};
                border-radius: 12px;
                border: 1px solid {BORDER};
            }}
        """)
        tl = QVBoxLayout(table_card)
        tl.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            L("date"), L("type"), L("operator"), L("details"),
            L("amount"), L("profit")
        ])
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(f"""
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
            }}
            QTableWidget::item {{
                padding: 10px 8px;
                border-bottom: 1px solid #f1f5f9;
            }}
            QTableWidget::item:selected {{
                background-color: #eef2ff;
                color: {TEXT_DARK};
            }}
        """)

        hh = self.table.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.table.verticalHeader().setDefaultSectionSize(48)

        tl.addWidget(self.table)

        # Ligne total en bas
        self.total_bar = QLabel("")
        self.total_bar.setStyleSheet(f"""
            background-color: #f8fafc;
            color: {TEXT_DARK};
            font-size: 14px;
            font-weight: bold;
            padding: 14px 20px;
            border-top: 2px solid {BORDER};
            border-bottom-left-radius: 12px;
            border-bottom-right-radius: 12px;
        """)
        self.total_bar.setAlignment(Qt.AlignmentFlag.AlignRight)
        tl.addWidget(self.total_bar)

        outer.addWidget(table_card, 1)

        # ============================================================
        # BOUTONS BAS
        # ============================================================
        bottom = QHBoxLayout()
        bottom.addStretch()

        self.edit_btn = QPushButton("✏ " + L("edit"))
        self.edit_btn.setMinimumHeight(42)
        self.edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #0ea5e9;
                border: 2px solid #bae6fd;
                padding: 10px 22px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #f0f9ff; border: 2px solid #0ea5e9; }
            QPushButton:disabled { color: #cbd5e1; border: 2px solid #e2e8f0; }
        """)
        self.edit_btn.clicked.connect(self.on_edit)
        self.edit_btn.setEnabled(False)
        bottom.addWidget(self.edit_btn)

        self.delete_btn = QPushButton("🗑 " + L("delete"))
        self.delete_btn.setMinimumHeight(42)
        self.delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #dc2626;
                border: 2px solid #fecaca;
                padding: 10px 22px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #fef2f2; border: 2px solid #dc2626; }
            QPushButton:disabled { color: #cbd5e1; border: 2px solid #e2e8f0; }
        """)
        self.delete_btn.clicked.connect(self.on_delete)
        self.delete_btn.setEnabled(False)
        bottom.addWidget(self.delete_btn)

        outer.addLayout(bottom)

        # ✅ Activer/désactiver les boutons selon la sélection
        self.table.itemSelectionChanged.connect(self._on_selection_changed)

        self.refresh()

    # ============================================================
    # FILTRE
    # ============================================================
    def on_filter_change(self, filter_id):
        self.current_filter = filter_id
        for fid, btn in self.filter_buttons.items():
            btn.setChecked(fid == filter_id)
        self.refresh()

    # ============================================================
    # SELECTION → ACTIVER BOUTONS
    # ============================================================
    def _on_selection_changed(self):
        has_selection = len(self.table.selectionModel().selectedRows()) > 0
        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)

    # ============================================================
    # REFRESH
    # ============================================================
    def refresh(self):
        L = lambda key: t(key, self.lang)
        self.current_filter = next(
            (fid for fid, b in self.filter_buttons.items() if b.isChecked()),
            "all"
        )

        # ---------- STAT CARDS ----------
        while self.stats_grid.count():
            item = self.stats_grid.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        credit = get_credit_summary_today()
        cards = get_card_summary_today()

        self.stats_grid.addWidget(StatCard(
            "💰", L("sold_credit"), f"{credit['sold']:.2f} DH",
            "#0ea5e9", f"{credit['count']} {L('transactions')}"
        ), 0, 0)
        self.stats_grid.addWidget(StatCard(
            "📥", L("bought_credit"), f"{credit['bought']:.2f} DH",
            "#6366f1", L("recharges_today")
        ), 0, 1)
        self.stats_grid.addWidget(StatCard(
            "🎫", L("sold_cards"), f"{cards['sold']:.2f} DH",
            "#f97316", f"{int(cards['sold_qty'])} {L('cards_sold')}"
        ), 0, 2)
        self.stats_grid.addWidget(StatCard(
            "💚", L("profit_today"), f"{credit['profit']:.2f} DH",
            "#16a34a", L("net_profit")
        ), 0, 3)

        # ---------- TABLEAU ----------
        history = []

        if self.current_filter in ("all", "credit"):
            for tr in get_credit_transactions(500):
                history.append({
                    "id": tr["id"],
                    "source": "credit",
                    "date": tr["transaction_date"],
                    "type": "💰 " + (L("sale") if tr["type"] == "sell" else L("recharge")),
                    "type_raw": tr["type"],
                    "operator": tr["operator_name"],
                    "color": tr["operator_color"],
                    "details": L("credit"),
                    "amount": tr["amount"],
                    "profit": tr["profit"],
                })

        if self.current_filter in ("all", "card"):
            for s in get_card_sales(500):
                history.append({
                    "id": s["id"],
                    "source": "card_sale",
                    "date": s["sale_date"],
                    "type": "🎫 " + L("sale"),
                    "type_raw": "card_sell",
                    "operator": s["operator_name"],
                    "color": "#0ea5e9",
                    "details": f"{s['quantity']} × {int(s['denomination'])} DH",
                    "amount": s["total"],
                    "profit": 0,
                })
            for p in get_card_purchases(500):
                history.append({
                    "id": p["id"],
                    "source": "card_purchase",
                    "date": p["purchase_date"],
                    "type": "📥 " + L("buy_cards"),
                    "type_raw": "card_buy",
                    "operator": p["operator_name"],
                    "color": "#8b5cf6",
                    "details": f"{p['quantity']} × {int(p['denomination'])} DH",
                    "amount": p["total"],
                    "profit": 0,
                })

        history.sort(key=lambda x: x["date"], reverse=True)

        self.table.setRowCount(len(history))
        total_amount = 0.0
        total_profit = 0.0

        for row, h in enumerate(history):
            total_amount += h["amount"]
            total_profit += h["profit"]

            # Date (format court + tooltip full)
            date_short = str(h["date"])[5:16]  # MM-DD HH:MM
            date_item = QTableWidgetItem(date_short)
            date_item.setToolTip(str(h["date"]))
            date_item.setData(Qt.ItemDataRole.UserRole, h["id"])
            date_item.setData(Qt.ItemDataRole.UserRole + 1, h["source"])
            date_item.setData(Qt.ItemDataRole.UserRole + 2, h)
            self.table.setItem(row, 0, date_item)

            # Type (avec emoji + badge)
            type_item = QTableWidgetItem(h["type"])
            if h["type_raw"] == "sell":
                type_item.setForeground(QColor("#16a34a"))
            elif h["type_raw"] == "buy":
                type_item.setForeground(QColor("#6366f1"))
            elif h["type_raw"] == "card_sell":
                type_item.setForeground(QColor("#0ea5e9"))
            else:
                type_item.setForeground(QColor("#8b5cf6"))
            self.table.setItem(row, 1, type_item)

            # Opérateur coloré
            op_item = QTableWidgetItem(h["operator"])
            op_item.setForeground(QColor(h["color"]))
            f = QFont()
            f.setBold(True)
            op_item.setFont(f)
            self.table.setItem(row, 2, op_item)

            # Détails
            self.table.setItem(row, 3, QTableWidgetItem(h["details"]))

            # Montant
            amt = QTableWidgetItem(f"{h['amount']:.2f} DH")
            amt.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            f2 = QFont()
            f2.setBold(True)
            amt.setFont(f2)
            self.table.setItem(row, 4, amt)

            # Profit
            if h["profit"]:
                prof = QTableWidgetItem(f"+{h['profit']:.2f} DH")
                prof.setForeground(QColor("#16a34a"))
                f3 = QFont()
                f3.setBold(True)
                prof.setFont(f3)
            else:
                prof = QTableWidgetItem("—")
                prof.setForeground(QColor("#94a3b8"))
            prof.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row, 5, prof)

        # ---------- TOTAL ----------
        self.total_bar.setText(
            f"📊 TOTAL : {total_amount:.2f} DH   |   "
            f"💚 PROFIT : +{total_profit:.2f} DH   |   "
            f"📋 {len(history)} transaction(s)"
        )

    # ============================================================
    # SÉLECTION
    # ============================================================
    def _selected_transaction(self):
        rows = self.table.selectionModel().selectedRows()
        if not rows:
            return None
        row = rows[0].row()
        item = self.table.item(row, 0)
        if not item:
            return None
        trans_id = item.data(Qt.ItemDataRole.UserRole)
        source = item.data(Qt.ItemDataRole.UserRole + 1)
        data = item.data(Qt.ItemDataRole.UserRole + 2)
        return trans_id, source, data

    # ============================================================
    # SUPPRIMER
    # ============================================================
    def on_delete(self):
        L = lambda key: t(key, self.lang)
        selected = self._selected_transaction()
        if not selected:
            QMessageBox.information(self, L("warning"), L("no_selection"))
            return

        trans_id, source, data = selected

        dlg = AdminPasswordDialog(self, action_text=L("delete_transaction"))
        if not dlg.exec():
            return

        confirm = QMessageBox.question(
            self, L("delete_transaction"),
            L("confirm_delete_transaction"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        try:
            if source == "credit":
                delete_credit_transaction(trans_id)
            elif source == "card_sale":
                delete_card_sale(trans_id)
            elif source == "card_purchase":
                delete_card_purchase(trans_id)
            QMessageBox.information(self, "✅ " + L("success"),
                                    "Transaction supprimée ✓")
            self.refresh()
        except Exception as e:
            QMessageBox.critical(self, L("error"), str(e))

    # ============================================================
    # MODIFIER
    # ============================================================
    def on_edit(self):
        L = lambda key: t(key, self.lang)
        selected = self._selected_transaction()
        if not selected:
            QMessageBox.information(self, L("warning"), L("no_selection"))
            return

        trans_id, source, data = selected

        if source != "credit":
            QMessageBox.information(
                self, L("warning"),
                "Seules les transactions délaire peuvent être modifiées.\n"
                "Pour les cartes, supprime et refais la vente."
            )
            return

        dlg = AdminPasswordDialog(self, action_text=L("edit_transaction"))
        if not dlg.exec():
            return

        edit_dlg = EditTransactionDialog(self, transaction=data)
        if not edit_dlg.exec():
            return

        try:
            update_credit_transaction(trans_id, edit_dlg.new_amount)
            QMessageBox.information(self, "✅ " + L("success"),
                                    "Transaction modifiée ✓")
            self.refresh()
        except Exception as e:
            QMessageBox.critical(self, L("error"), str(e))

    # ============================================================
    # VIDER TOUT
    # ============================================================
    def on_clear_all(self):
        L = lambda key: t(key, self.lang)

        dlg = AdminPasswordDialog(self, action_text=L("clear_all"))
        if not dlg.exec():
            return

        confirm = QMessageBox.question(
            self, "⚠️ " + L("clear_all"),
            L("clear_all_confirm"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        confirm2 = QMessageBox.warning(
            self, "⚠️⚠️ " + L("clear_all"),
            L("clear_all_confirm2"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm2 != QMessageBox.StandardButton.Yes:
            return

        try:
            stats = clear_all_transactions()
            QMessageBox.information(
                self, "✅ " + L("success"),
                f"{L('clear_all_done')}\n\n"
                f"💰 Délaire : {stats['credit_count']}\n"
                f"🎫 Ventes cartes : {stats['card_sales_count']}\n"
                f"📥 Achats cartes : {stats['card_purchases_count']}"
            )
            self.refresh()
        except Exception as e:
            QMessageBox.critical(self, L("error"), str(e))