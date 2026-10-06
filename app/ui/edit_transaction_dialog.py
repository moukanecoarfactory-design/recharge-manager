"""Dialog pour modifier le montant d'une transaction."""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QDoubleSpinBox,
    QPushButton, QFrame, QMessageBox, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from app.locales.translations import t, get_current_language


class EditTransactionDialog(QDialog):
    """Modifie le montant d'une transaction délaire."""

    def __init__(self, parent=None, transaction: dict = None):
        super().__init__(parent)
        self.lang = get_current_language()
        self.transaction = transaction or {}
        self.new_amount = None

        L = lambda key: t(key, self.lang)

        self.setWindowTitle("✏ " + L("edit_transaction"))
        self.setFixedSize(420, 380)
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1e293b, stop:1 #0f172a
                );
            }
        """)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(30, 30, 30, 30)

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 14px;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(22)
        shadow.setColor(QColor(0, 0, 0, 40))
        card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(28, 24, 28, 24)
        card_layout.setSpacing(12)

        # Icône
        icon = QLabel("✏️")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet("font-size: 42px; background: transparent;")
        card_layout.addWidget(icon)

        # Titre
        title = QLabel(L("edit_transaction"))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            color: #0f172a; font-size: 18px;
            font-weight: bold; background: transparent;
        """)
        card_layout.addWidget(title)

        # Info transaction actuelle
        old_amount = self.transaction.get("amount", 0)
        info = QLabel(
            f"{L('current_amount')} : {old_amount:.2f} DH"
        )
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setStyleSheet("""
            color: #64748b; font-size: 13px;
            background: #f8fafc;
            border-radius: 6px;
            padding: 8px;
        """)
        card_layout.addWidget(info)

        # Nouveau montant
        new_lbl = QLabel(L("new_amount"))
        new_lbl.setStyleSheet("""
            color: #334155; font-size: 13px;
            font-weight: bold; background: transparent;
        """)
        card_layout.addWidget(new_lbl)

        self.amount_input = QDoubleSpinBox()
        self.amount_input.setRange(1, 100000)
        self.amount_input.setDecimals(2)
        self.amount_input.setValue(old_amount)
        self.amount_input.setSuffix(" DH")
        self.amount_input.setMinimumHeight(48)
        self.amount_input.setStyleSheet("""
            QDoubleSpinBox {
                background-color: #f8fafc;
                color: #0f172a;
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                padding: 8px 14px;
                font-size: 18px;
                font-weight: bold;
            }
            QDoubleSpinBox:focus { border: 2px solid #6366f1; }
        """)
        card_layout.addWidget(self.amount_input)

        # Boutons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        cancel_btn = QPushButton(L("cancel"))
        cancel_btn.setMinimumHeight(42)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                color: #475569;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
                padding: 10px;
            }
            QPushButton:hover { background-color: #e2e8f0; }
        """)
        cancel_btn.clicked.connect(self.reject)
        btn_row.addWidget(cancel_btn)

        ok_btn = QPushButton("✓ " + L("save"))
        ok_btn.setMinimumHeight(42)
        ok_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        ok_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0ea5e9, stop:1 #6366f1
                );
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
                padding: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0284c7, stop:1 #4f46e5
                );
            }
        """)
        ok_btn.clicked.connect(self._on_validate)
        btn_row.addWidget(ok_btn)

        card_layout.addLayout(btn_row)
        outer.addWidget(card)

    def _on_validate(self):
        self.new_amount = self.amount_input.value()
        if self.new_amount <= 0:
            QMessageBox.warning(self, "Erreur", "Montant invalide")
            return
        self.accept()