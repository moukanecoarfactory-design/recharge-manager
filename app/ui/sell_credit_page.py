"""Vendre du délaire à un client."""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QDoubleSpinBox, QMessageBox, QGraphicsDropShadowEffect,
    QGridLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from app.db.operator_repo import get_all_operators, get_operator
from app.db.transaction_repo import sell_credit, adjust_operator_balance
from app.locales.translations import t, get_current_language
from app.ui.logo_widget import OperatorLogo
from app.ui.admin_password_dialog import AdminPasswordDialog
from app.ui.edit_balance_dialog import EditBalanceDialog
from app.ui.styles import (
    btn_secondary, btn_success, input_style,
    label_title, label_field,
    WHITE, BORDER, TEXT_DARK, TEXT_LIGHT, TEXT_MEDIUM, BG_LIGHT
)


def hex_to_rgb(hex_color: str):
    c = hex_color.lstrip("#")
    return int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)


class OperatorSelectButton(QFrame):
    def __init__(self, operator, on_select, on_edit_balance, lang="fr"):
        super().__init__()
        self.operator = operator
        self.on_select = on_select
        self.on_edit_balance = on_edit_balance
        self.lang = lang
        self.selected = False

        self.setMinimumHeight(140)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 16, 20, 16)
        self.main_layout.setSpacing(10)

        # Header
        header = QHBoxLayout()
        header.setSpacing(14)

        self.logo = OperatorLogo(
            code=operator.code, name=operator.name,
            color=operator.color, size=56
        )
        header.addWidget(self.logo)

        name_col = QVBoxLayout()
        name_col.setSpacing(2)

        self.name_lbl = QLabel(operator.name)
        name_col.addWidget(self.name_lbl)

        self.comm_lbl = QLabel(f"{t('commission', self.lang)} : {operator.commission}%")
        name_col.addWidget(self.comm_lbl)

        header.addLayout(name_col)
        header.addStretch()

        self.edit_btn = QPushButton("✏️")
        self.edit_btn.setFixedSize(34, 34)
        self.edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.edit_btn.setToolTip("Modifier le solde")
        self.edit_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.8);
                color: #0ea5e9;
                border: 1.5px solid #0ea5e9;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #0ea5e9; color: white; }
        """)
        self.edit_btn.clicked.connect(self._on_edit_click)
        self.edit_btn.setVisible(False)
        header.addWidget(self.edit_btn)

        self.check_lbl = QLabel("✓")
        self.check_lbl.setFixedSize(30, 30)
        self.check_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.addWidget(self.check_lbl)

        self.main_layout.addLayout(header)

        # Bloc Ancien/Nouveau
        self.balance_block = QFrame()
        self.balance_block.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.5);
                border-radius: 8px;
            }
        """)
        block_layout = QVBoxLayout(self.balance_block)
        block_layout.setContentsMargins(12, 8, 12, 8)
        block_layout.setSpacing(4)

        self.old_lbl = QLabel("")
        self.old_lbl.setStyleSheet("""
            color: #334155; font-size: 12px;
            background: transparent;
        """)
        block_layout.addWidget(self.old_lbl)

        self.new_lbl = QLabel("")
        self.new_lbl.setStyleSheet("""
            font-size: 14px; font-weight: bold;
            background: transparent;
        """)
        block_layout.addWidget(self.new_lbl)

        self.balance_block.setVisible(False)
        self.main_layout.addWidget(self.balance_block)

        self._apply_style()

    def _apply_style(self):
        color = self.operator.color
        r, g, b = hex_to_rgb(color)

        if self.selected:
            self.setStyleSheet(f"""
                OperatorSelectButton {{
                    background-color: rgba({r}, {g}, {b}, 0.1);
                    border-radius: 14px;
                    border: 2px solid {color};
                }}
            """)
            self.name_lbl.setStyleSheet(f"""
                color: {color};
                font-size: 17px;
                font-weight: bold;
                background: transparent;
            """)
            self.comm_lbl.setStyleSheet(f"""
                color: {color};
                font-size: 12px;
                font-weight: bold;
                background: transparent;
            """)
            self.check_lbl.setStyleSheet(f"""
                color: white;
                background-color: {color};
                border-radius: 15px;
                font-size: 18px;
                font-weight: bold;
            """)
            self.check_lbl.setVisible(True)
            self.edit_btn.setVisible(True)
            self.balance_block.setVisible(True)
        else:
            self.setStyleSheet(f"""
                OperatorSelectButton {{
                    background-color: #ffffff;
                    border-radius: 14px;
                    border: 1px solid {BORDER};
                }}
                OperatorSelectButton:hover {{
                    border: 1.5px solid {color};
                    background-color: rgba({r}, {g}, {b}, 0.05);
                }}
            """)
            self.name_lbl.setStyleSheet(f"""
                color: {TEXT_DARK};
                font-size: 16px;
                font-weight: bold;
                background: transparent;
            """)
            self.comm_lbl.setStyleSheet(f"""
                color: {color};
                font-size: 11px;
                font-weight: bold;
                background: transparent;
            """)
            self.check_lbl.setStyleSheet("")
            self.check_lbl.setVisible(False)
            self.edit_btn.setVisible(False)
            self.balance_block.setVisible(False)

    def set_selected(self, selected):
        self.selected = selected
        self._apply_style()

    def update_preview(self, amount):
        if not self.selected:
            return
        old = self.operator.balance
        new = old - amount
        self.old_lbl.setText(f"💰 Ancien : {old:.2f} DH")
        self.new_lbl.setText(f"💸 Nouveau : {new:.2f} DH")
        self.new_lbl.setStyleSheet(f"""
            color: {self.operator.color};
            font-size: 14px;
            font-weight: bold;
            background: transparent;
        """)

    def _on_edit_click(self):
        self.on_edit_balance(self.operator)

    def mousePressEvent(self, event):
        self.on_select(self.operator)
        super().mousePressEvent(event)


class SellCreditPage(QWidget):
    def __init__(self):
        super().__init__()
        self.lang = get_current_language()
        L = lambda key: t(key, self.lang)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 24, 24, 24)
        outer.setSpacing(14)

        header = QHBoxLayout()
        title = QLabel("💰 " + L("sell_credit_title"))
        title.setStyleSheet(label_title())
        header.addWidget(title)
        header.addStretch()
        outer.addLayout(header)

        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {WHITE};
                border-radius: 16px;
                border: 1px solid {BORDER};
            }}
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 20))
        card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(28, 24, 28, 24)
        card_layout.setSpacing(16)

        op_lbl = QLabel(L("operator"))
        op_lbl.setStyleSheet(label_field())
        card_layout.addWidget(op_lbl)

        self.operator_buttons = {}
        op_grid = QGridLayout()
        op_grid.setSpacing(12)

        self.operators = get_all_operators()
        for i, op in enumerate(self.operators):
            btn = OperatorSelectButton(
                op, self.select_operator, self.on_edit_balance, lang=self.lang
            )
            self.operator_buttons[op.id] = btn
            op_grid.addWidget(btn, 0, i)

        card_layout.addLayout(op_grid)

        self.balance_info = QLabel("")
        self.balance_info.setStyleSheet(f"""
            color: {TEXT_MEDIUM};
            font-size: 14px;
            font-weight: bold;
            background-color: {BG_LIGHT};
            border-radius: 10px;
            padding: 14px;
            border: 1px solid {BORDER};
        """)
        self.balance_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.balance_info)

        amt_lbl = QLabel(L("amount_to_sell"))
        amt_lbl.setStyleSheet(label_field())
        card_layout.addWidget(amt_lbl)

        self.amount_input = QDoubleSpinBox()
        self.amount_input.setRange(10, 500)
        self.amount_input.setDecimals(2)
        self.amount_input.setSingleStep(5)
        self.amount_input.setValue(20)
        self.amount_input.setSuffix(" DH")
        self.amount_input.setMinimumHeight(55)
        self.amount_input.setStyleSheet(input_style() + """
            QDoubleSpinBox {
                font-size: 22px;
                font-weight: bold;
                padding: 10px 18px;
            }
        """)
        self.amount_input.valueChanged.connect(self.update_preview)
        self.amount_input.lineEdit().returnPressed.connect(self.on_validate)
        card_layout.addWidget(self.amount_input)

        preview = QFrame()
        preview.setStyleSheet("""
            QFrame {
                background-color: #f0fdf4;
                border-radius: 12px;
                border: 2px solid #86efac;
            }
        """)
        prev_layout = QVBoxLayout(preview)
        prev_layout.setContentsMargins(20, 16, 20, 16)
        prev_layout.setSpacing(8)

        self.client_pays_lbl = QLabel("")
        self.client_pays_lbl.setStyleSheet("""
            color: #166534;
            font-size: 18px;
            font-weight: bold;
            background: transparent;
        """)
        prev_layout.addWidget(self.client_pays_lbl)

        self.new_balance_lbl = QLabel("")
        self.new_balance_lbl.setStyleSheet("""
            color: #16a34a;
            font-size: 14px;
            background: transparent;
        """)
        prev_layout.addWidget(self.new_balance_lbl)

        card_layout.addWidget(preview)
        card_layout.addStretch()

        btn_row = QHBoxLayout()
        btn_row.addStretch()

        cancel_btn = QPushButton(L("cancel"))
        cancel_btn.setMinimumHeight(46)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet(btn_secondary())
        cancel_btn.clicked.connect(self.reset)
        btn_row.addWidget(cancel_btn)

        validate_btn = QPushButton("✓ " + L("validate_sale"))
        validate_btn.setMinimumHeight(46)
        validate_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        validate_btn.setStyleSheet(btn_success())
        validate_btn.clicked.connect(self.on_validate)
        btn_row.addWidget(validate_btn)

        card_layout.addLayout(btn_row)
        outer.addWidget(card, 1)

        self.selected_operator = None
        self.update_preview()

    def select_operator(self, op):
        self.selected_operator = op
        for op_id, btn in self.operator_buttons.items():
            btn.set_selected(op_id == op.id)
        self.update_preview()

    def update_preview(self):
        L = lambda key: t(key, self.lang)
        amount = self.amount_input.value()

        if not self.selected_operator:
            self.balance_info.setText("⚠️ " + L("choose_operator"))
            self.balance_info.setStyleSheet("""
                color: #92400e;
                font-size: 14px;
                font-weight: bold;
                background-color: #fef3c7;
                border-radius: 10px;
                padding: 14px;
                border: 1px solid #fcd34d;
            """)
            self.client_pays_lbl.setText(L("client_pays") + " : 0.00 DH")
            self.new_balance_lbl.setText("")
            return

        op = get_operator(self.selected_operator.id)
        new_balance = op.balance - amount
        r, g, b = hex_to_rgb(op.color)

        self.balance_info.setText(
            f"💰 {L('balance')} {op.name} : {op.balance:.2f} DH"
        )
        self.balance_info.setStyleSheet(f"""
            color: {op.color};
            font-size: 14px;
            font-weight: bold;
            background-color: rgba({r}, {g}, {b}, 0.1);
            border-radius: 10px;
            padding: 14px;
            border: 1px solid rgba({r}, {g}, {b}, 0.3);
        """)

        self.client_pays_lbl.setText(f"{L('client_pays')} : {amount:.2f} DH")
        self.new_balance_lbl.setText(f"{L('balance_after')} : {new_balance:.2f} DH")

        for op_id, btn in self.operator_buttons.items():
            if op_id == op.id:
                btn.update_preview(amount)

    def reset(self):
        self.selected_operator = None
        for btn in self.operator_buttons.values():
            btn.set_selected(False)
        self.amount_input.setValue(20)
        self.update_preview()

    def on_validate(self):
        L = lambda key: t(key, self.lang)
        if not self.selected_operator:
            QMessageBox.warning(self, L("warning"), L("choose_operator"))
            return

        op = get_operator(self.selected_operator.id)
        amount = self.amount_input.value()

        if op.balance < amount:
            QMessageBox.warning(
                self, L("insufficient_balance"),
                L("insufficient_msg").replace("{op}", op.name)
                                     .replace("{balance}", f"{op.balance:.2f}")
            )
            return

        try:
            sell_credit(op.id, amount)
            QMessageBox.information(
                self, "✅ " + L("success"),
                L("sale_success_msg").replace("{amount}", f"{amount:.2f}")
                                     .replace("{op}", op.name)
            )
            self.operators = get_all_operators()
            self.reset()
        except Exception as e:
            QMessageBox.critical(self, L("error"), str(e))

    def on_edit_balance(self, op):
        dlg = AdminPasswordDialog(self, action_text=f"Modifier le solde {op.name}")
        if not dlg.exec():
            return

        edit_dlg = EditBalanceDialog(self, operator=op)
        if not edit_dlg.exec():
            return

        try:
            old_balance = op.balance
            new_balance = edit_dlg.new_balance
            adjust_operator_balance(op.id, old_balance, new_balance)
            QMessageBox.information(
                self, "✅ Succès",
                f"Solde {op.name} modifié !\n\n"
                f"💰 Ancien : {old_balance:.2f} DH\n"
                f"💚 Nouveau : {new_balance:.2f} DH"
            )
            self.operators = get_all_operators()
            self.selected_operator = None
            self.reset()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))