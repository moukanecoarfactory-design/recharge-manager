"""Dialog pour modifier le solde d'un opérateur."""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QDoubleSpinBox,
    QPushButton, QFrame, QMessageBox, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from app.locales.translations import t, get_current_language


class EditBalanceDialog(QDialog):
    """Modifie le solde d'un opérateur."""

    def __init__(self, parent=None, operator=None):
        super().__init__(parent)
        self.lang = get_current_language()
        self.operator = operator
        self.new_balance = None

        L = lambda key: t(key, self.lang)

        self.setWindowTitle("✏️ Modifier le solde")
        self.setFixedSize(460, 420)
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

        # Carte blanche
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
        title = QLabel(f"Modifier le solde {operator.name if operator else ''}")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            color: #0f172a; font-size: 16px;
            font-weight: bold; background: transparent;
        """)
        card_layout.addWidget(title)

        # Solde actuel
        current_lbl = QLabel(
            f"💰 Solde actuel : {operator.balance:.2f} DH" if operator else ""
        )
        current_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        current_lbl.setStyleSheet("""
            color: #64748b; font-size: 14px;
            background: #f8fafc;
            border-radius: 8px;
            padding: 10px;
        """)
        card_layout.addWidget(current_lbl)

        # Label nouveau solde
        new_lbl = QLabel("Nouveau solde :")
        new_lbl.setStyleSheet("""
            color: #334155; font-size: 13px;
            font-weight: bold; background: transparent;
        """)
        card_layout.addWidget(new_lbl)

        # Input nouveau solde
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setRange(0, 1000000)
        self.amount_input.setDecimals(2)
        self.amount_input.setSuffix(" DH")
        self.amount_input.setValue(operator.balance if operator else 0)
        self.amount_input.setMinimumHeight(50)
        self.amount_input.setStyleSheet("""
            QDoubleSpinBox {
                background-color: #f8fafc;
                color: #0f172a;
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                padding: 8px 14px;
                font-size: 20px;
                font-weight: bold;
            }
            QDoubleSpinBox:focus { border: 2px solid #6366f1; }
        """)
        card_layout.addWidget(self.amount_input)

        # Info
        info = QLabel(
            "⚠️ Cette modification sera enregistrée "
            "dans l'historique comme un ajustement."
        )
        info.setWordWrap(True)
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setStyleSheet("""
            color: #92400e; font-size: 11px;
            background: #fef3c7;
            border-radius: 6px;
            padding: 8px;
        """)
        card_layout.addWidget(info)

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

        ok_btn = QPushButton("✓ Enregistrer")
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

        self.amount_input.setFocus()
        self.amount_input.selectAll()

    def _on_validate(self):
        self.new_balance = self.amount_input.value()
        self.accept()