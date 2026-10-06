"""Page de gestion des cartes V2."""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView, QDialog, QFormLayout, QComboBox,
    QSpinBox, QDoubleSpinBox, QDialogButtonBox, QMessageBox,
    QGraphicsDropShadowEffect, QGridLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QIcon

from app.db.card_repo import (
    get_all_cards, set_stock, clear_stock, clear_all_stocks
)
from app.db.operator_repo import get_all_operators
from app.db.transaction_repo import buy_cards, sell_cards
from app.locales.translations import t, get_current_language
from app.ui.admin_password_dialog import AdminPasswordDialog
from app.ui.edit_stock_dialog import EditStockDialog
from app.ui.logo_widget import get_operator_icon
from app.ui.styles import (
    btn_secondary, input_style, label_title, label_field,
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
        self.setMinimumHeight(100)

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


class BuyCardsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lang = get_current_language()
        L = lambda key: t(key, self.lang)

        self.setWindowTitle("📥 " + L("buy_cards"))
        self.setMinimumWidth(420)
        self.setStyleSheet(f"QDialog {{ background-color: {WHITE}; }}")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        title = QLabel("📥 " + L("buy_cards"))
        title.setStyleSheet(f"color: {TEXT_DARK}; font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(10)

        self.op_combo = QComboBox()
        self.op_combo.setMinimumHeight(38)
        self.op_combo.setStyleSheet(input_style())
        for op in get_all_operators():
            self.op_combo.addItem(op.name, op.id)
        form.addRow(L("operator") + " :", self.op_combo)

        self.denom_combo = QComboBox()
        self.denom_combo.setMinimumHeight(38)
        self.denom_combo.setStyleSheet(input_style())
        self.denom_combo.addItem("5 DH", 5.0)
        self.denom_combo.addItem("10 DH", 10.0)
        form.addRow(L("denomination") + " :", self.denom_combo)

        self.qty_input = QSpinBox()
        self.qty_input.setRange(1, 10000)
        self.qty_input.setValue(10)
        self.qty_input.setMinimumHeight(38)
        self.qty_input.setStyleSheet(input_style())
        form.addRow(L("quantity") + " :", self.qty_input)

        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0, 1000)
        self.price_input.setDecimals(2)
        self.price_input.setSuffix(" DH")
        self.price_input.setMinimumHeight(38)
        self.price_input.setStyleSheet(input_style())
        form.addRow(L("unit_price") + " :", self.price_input)

        layout.addLayout(form)

        self.total_lbl = QLabel("")
        self.total_lbl.setStyleSheet(f"""
            color: {TEXT_DARK};
            font-size: 15px;
            font-weight: bold;
            background-color: {BG_LIGHT};
            border-radius: 10px;
            padding: 10px;
        """)
        self.total_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.total_lbl)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText("✓ " + L("save"))
        buttons.button(QDialogButtonBox.Cancel).setText(L("cancel"))
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.denom_combo.currentIndexChanged.connect(self.update_price)
        self.qty_input.valueChanged.connect(self.update_total)
        self.price_input.valueChanged.connect(self.update_total)
        self.update_price()

    def update_price(self):
        self.price_input.setValue(self.denom_combo.currentData())
        self.update_total()

    def update_total(self):
        total = self.qty_input.value() * self.price_input.value()
        self.total_lbl.setText(f"💰 TOTAL : {total:.2f} DH")

    def get_data(self):
        return {
            "operator_id": self.op_combo.currentData(),
            "denomination": self.denom_combo.currentData(),
            "quantity": self.qty_input.value(),
            "unit_price": self.price_input.value(),
        }


class SellCardsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lang = get_current_language()
        L = lambda key: t(key, self.lang)

        self.setWindowTitle("🎫 " + L("sell_cards"))
        self.setMinimumWidth(420)
        self.setStyleSheet(f"QDialog {{ background-color: {WHITE}; }}")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        title = QLabel("🎫 " + L("sell_cards"))
        title.setStyleSheet(f"color: {TEXT_DARK}; font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(10)

        self.op_combo = QComboBox()
        self.op_combo.setMinimumHeight(38)
        self.op_combo.setStyleSheet(input_style())
        for op in get_all_operators():
            self.op_combo.addItem(op.name, op.id)
        form.addRow(L("operator") + " :", self.op_combo)

        self.denom_combo = QComboBox()
        self.denom_combo.setMinimumHeight(38)
        self.denom_combo.setStyleSheet(input_style())
        self.denom_combo.addItem("5 DH", 5.0)
        self.denom_combo.addItem("10 DH", 10.0)
        form.addRow(L("denomination") + " :", self.denom_combo)

        self.qty_input = QSpinBox()
        self.qty_input.setRange(1, 10000)
        self.qty_input.setValue(1)
        self.qty_input.setMinimumHeight(38)
        self.qty_input.setStyleSheet(input_style())
        form.addRow(L("quantity") + " :", self.qty_input)

        self.stock_lbl = QLabel("")
        self.stock_lbl.setStyleSheet(f"color: {TEXT_LIGHT}; font-size: 12px;")
        form.addRow(L("stock") + " :", self.stock_lbl)

        layout.addLayout(form)

        self.total_lbl = QLabel("")
        self.total_lbl.setStyleSheet(f"""
            color: {TEXT_DARK};
            font-size: 15px;
            font-weight: bold;
            background-color: {BG_LIGHT};
            border-radius: 10px;
            padding: 10px;
        """)
        self.total_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.total_lbl)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText("✓ " + L("confirm"))
        buttons.button(QDialogButtonBox.Cancel).setText(L("cancel"))
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.op_combo.currentIndexChanged.connect(self.update_stock)
        self.denom_combo.currentIndexChanged.connect(self.update_stock)
        self.qty_input.valueChanged.connect(self.update_total)
        self.update_stock()

    def update_stock(self):
        op_id = self.op_combo.currentData()
        denom = self.denom_combo.currentData()
        cards = get_all_cards()
        stock = 0
        for c in cards:
            if c.operator_id == op_id and c.denomination == denom:
                stock = c.stock
                break
        self.stock_lbl.setText(f"{stock} {t('available_cards', self.lang)}")
        self.update_total()

    def update_total(self):
        total = self.qty_input.value() * self.denom_combo.currentData()
        self.total_lbl.setText(f"💰 TOTAL : {total:.2f} DH")

    def get_data(self):
        return {
            "operator_id": self.op_combo.currentData(),
            "denomination": self.denom_combo.currentData(),
            "quantity": self.qty_input.value(),
        }


class CardsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.lang = get_current_language()
        L = lambda key: t(key, self.lang)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 24, 24, 24)
        outer.setSpacing(14)

        header = QHBoxLayout()
        title = QLabel("🎫 " + L("cards_title"))
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

        self.stats_grid = QGridLayout()
        self.stats_grid.setSpacing(14)
        outer.addLayout(self.stats_grid)

        actions = QHBoxLayout()
        actions.setSpacing(10)

        buy_btn = QPushButton("📥 " + L("buy_cards"))
        buy_btn.setMinimumHeight(44)
        buy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        buy_btn.setStyleSheet("""
            QPushButton {
                background-color: #6366f115;
                color: #6366f1;
                border: 1.5px solid #6366f140;
                padding: 10px 22px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #6366f125;
                border: 1.5px solid #6366f1;
            }
        """)
        buy_btn.clicked.connect(self.on_buy)
        actions.addWidget(buy_btn)

        sell_btn = QPushButton("🎫 " + L("sell_cards"))
        sell_btn.setMinimumHeight(44)
        sell_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        sell_btn.setStyleSheet("""
            QPushButton {
                background-color: #16a34a15;
                color: #16a34a;
                border: 1.5px solid #16a34a40;
                padding: 10px 22px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #16a34a25;
                border: 1.5px solid #16a34a;
            }
        """)
        sell_btn.clicked.connect(self.on_sell)
        actions.addWidget(sell_btn)

        actions.addStretch()

        clear_all_btn = QPushButton("🗑️ " + L("clear_all_stocks"))
        clear_all_btn.setMinimumHeight(44)
        clear_all_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #dc2626;
                border: 1.5px solid #fecaca;
                padding: 10px 18px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #fef2f2;
                border: 1.5px solid #dc2626;
            }
        """)
        clear_all_btn.clicked.connect(self.on_clear_all)
        actions.addWidget(clear_all_btn)

        outer.addLayout(actions)

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
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            L("operator"), L("denomination"), L("stock"), L("status"),
            L("alert"), "Actions"
        ])
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
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
            QTableWidget::item:selected {{
                background-color: #eef2ff;
                color: {TEXT_DARK};
            }}
        """)

        hh = self.table.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for col in [1, 2, 3, 4]:
            hh.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(5, 130)
        self.table.verticalHeader().setDefaultSectionSize(58)

        tl.addWidget(self.table)
        outer.addWidget(table_card, 1)

        self.refresh()

    def refresh(self):
        L = lambda key: t(key, self.lang)

        while self.stats_grid.count():
            item = self.stats_grid.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        cards = get_all_cards()
        total_stock = sum(c.stock for c in cards)
        total_value = sum(c.stock * c.denomination for c in cards)
        alerts = sum(1 for c in cards if c.stock <= 5)
        ruptures = sum(1 for c in cards if c.stock == 0)

        self.stats_grid.addWidget(StatCard("📦", "Stock total", f"{total_stock}", "#0ea5e9", f"sur {len(cards)} produits"), 0, 0)
        self.stats_grid.addWidget(StatCard("💰", "Valeur stock", f"{total_value:.2f} DH", "#16a34a", "capital immobilisé"), 0, 1)
        self.stats_grid.addWidget(StatCard("⚠️", "Alertes", f"{alerts}", "#dc2626", f"dont {ruptures} rupture(s)"), 0, 2)

        self.table.setRowCount(len(cards))

        for row, c in enumerate(cards):
            op_item = QTableWidgetItem("  " + c.operator_name)
            icon = get_operator_icon(
                "inwi" if "inwi" in c.operator_name.lower() else
                "iam" if "iam" in c.operator_name.lower() else "orange",
                32
            )
            if not icon.isNull():
                op_item.setIcon(QIcon(icon))
            op_item.setData(Qt.ItemDataRole.UserRole, c.id)
            op_item.setData(Qt.ItemDataRole.UserRole + 1, {
                "id": c.id, "operator_name": c.operator_name,
                "denomination": c.denomination, "stock": c.stock,
            })
            self.table.setItem(row, 0, op_item)

            denom_item = QTableWidgetItem(f"{int(c.denomination)} DH")
            denom_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 1, denom_item)

            stock_item = QTableWidgetItem(str(c.stock))
            stock_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if c.stock <= 5:
                stock_item.setForeground(QColor("#dc2626"))
                stock_item.setBackground(QColor("#fef2f2"))
            elif c.stock <= 10:
                stock_item.setForeground(QColor("#f59e0b"))
                stock_item.setBackground(QColor("#fef3c7"))
            else:
                stock_item.setForeground(QColor("#16a34a"))
            self.table.setItem(row, 2, stock_item)

            if c.stock <= 0:
                statut = "❌ " + L("rupture")
                color = "#dc2626"; bg = "#fef2f2"
            elif c.stock <= 5:
                statut = "⚠️ " + L("low_stock")
                color = "#f59e0b"; bg = "#fef3c7"
            else:
                statut = "✅ " + L("ok")
                color = "#16a34a"; bg = "#f0fdf4"

            statut_item = QTableWidgetItem(statut)
            statut_item.setForeground(QColor(color))
            statut_item.setBackground(QColor(bg))
            statut_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 3, statut_item)

            alerte_txt = "⚠️ " + L("restock") if c.stock <= 5 else "—"
            alerte_item = QTableWidgetItem(alerte_txt)
            alerte_item.setForeground(QColor("#dc2626" if c.stock <= 5 else "#94a3b8"))
            alerte_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 4, alerte_item)

            actions = QWidget()
            actions_layout = QHBoxLayout(actions)
            actions_layout.setContentsMargins(2, 2, 2, 2)
            actions_layout.setSpacing(4)

            edit_btn = QPushButton("✏")
            edit_btn.setFixedSize(34, 30)
            edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            edit_btn.setToolTip(L("edit_stock"))
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #f0f9ff;
                    color: #0ea5e9;
                    border: 1px solid #bae6fd;
                    border-radius: 8px;
                    font-size: 14px;
                }
                QPushButton:hover { background-color: #e0f2fe; }
            """)
            edit_btn.clicked.connect(lambda _, cid=c.id, info={
                "id": c.id, "operator_name": c.operator_name,
                "denomination": c.denomination, "stock": c.stock
            }: self.on_edit_stock(cid, info))
            actions_layout.addWidget(edit_btn)

            clear_btn = QPushButton("🗑")
            clear_btn.setFixedSize(34, 30)
            clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            clear_btn.setToolTip(L("clear_stock"))
            clear_btn.setStyleSheet("""
                QPushButton {
                    background-color: #fef2f2;
                    color: #dc2626;
                    border: 1px solid #fecaca;
                    border-radius: 8px;
                    font-size: 14px;
                }
                QPushButton:hover { background-color: #fee2e2; }
            """)
            clear_btn.clicked.connect(lambda _, cid=c.id, info={
                "id": c.id, "operator_name": c.operator_name,
                "denomination": c.denomination, "stock": c.stock
            }: self.on_clear_stock(cid, info))
            actions_layout.addWidget(clear_btn)

            self.table.setCellWidget(row, 5, actions)

    def _find_card_id(self, operator_id, denomination):
        for c in get_all_cards():
            if c.operator_id == operator_id and c.denomination == denomination:
                return c.id
        return None

    def on_buy(self):
        L = lambda key: t(key, self.lang)
        dlg = BuyCardsDialog(self)
        if dlg.exec():
            data = dlg.get_data()
            card_id = self._find_card_id(data["operator_id"], data["denomination"])
            if card_id:
                try:
                    buy_cards(card_id, data["quantity"], data["unit_price"])
                    QMessageBox.information(
                        self, "✅ " + L("success"),
                        L("buy_success").replace("{qty}", str(data["quantity"]))
                    )
                    self.refresh()
                except Exception as e:
                    QMessageBox.critical(self, L("error"), str(e))

    def on_sell(self):
        L = lambda key: t(key, self.lang)
        dlg = SellCardsDialog(self)
        if dlg.exec():
            data = dlg.get_data()
            card_id = self._find_card_id(data["operator_id"], data["denomination"])
            if card_id:
                try:
                    sell_cards(card_id, data["quantity"])
                    QMessageBox.information(
                        self, "✅ " + L("success"),
                        L("sell_success").replace("{qty}", str(data["quantity"]))
                    )
                    self.refresh()
                except Exception as e:
                    QMessageBox.critical(self, L("error"), str(e))

    def on_edit_stock(self, card_id, info):
        L = lambda key: t(key, self.lang)
        dlg = AdminPasswordDialog(self, action_text=L("edit_stock"))
        if not dlg.exec():
            return
        edit_dlg = EditStockDialog(self, card_info=info)
        if not edit_dlg.exec():
            return
        try:
            set_stock(card_id, edit_dlg.new_stock)
            QMessageBox.information(self, "✅ " + L("success"), L("stock_updated"))
            self.refresh()
        except Exception as e:
            QMessageBox.critical(self, L("error"), str(e))

    def on_clear_stock(self, card_id, info):
        L = lambda key: t(key, self.lang)
        dlg = AdminPasswordDialog(self, action_text=L("clear_stock"))
        if not dlg.exec():
            return
        confirm = QMessageBox.question(
            self, L("clear_stock"),
            f"{info['operator_name']} - {int(info['denomination'])} DH\n{L('clear_stock_confirm')}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return
        try:
            clear_stock(card_id)
            QMessageBox.information(self, "✅ " + L("success"), L("stock_updated"))
            self.refresh()
        except Exception as e:
            QMessageBox.critical(self, L("error"), str(e))

    def on_clear_all(self):
        L = lambda key: t(key, self.lang)
        dlg = AdminPasswordDialog(self, action_text=L("clear_all_stocks"))
        if not dlg.exec():
            return
        confirm = QMessageBox.question(
            self, "⚠️ " + L("clear_all_stocks"),
            L("clear_all_stocks_confirm"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return
        try:
            clear_all_stocks()
            QMessageBox.information(self, "✅ " + L("success"), L("stock_updated"))
            self.refresh()
        except Exception as e:
            QMessageBox.critical(self, L("error"), str(e))