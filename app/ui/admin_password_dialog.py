"""Dialog pour demander le mot de passe admin."""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QMessageBox, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from app.db.settings_repo import verify_admin_password
from app.locales.translations import t, get_current_language


class AdminPasswordDialog(QDialog):
    """Demande le mot de passe admin avant une action sensible."""

    def __init__(self, parent=None, action_text: str = ""):
        super().__init__(parent)
        self.lang = get_current_language()
        L = lambda key: t(key, self.lang)

        self.setWindowTitle("🔐 " + L("admin_password"))
        self.setFixedSize(420, 340)
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

        # Card
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
        icon = QLabel("🔐")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet("font-size: 42px; background: transparent;")
        card_layout.addWidget(icon)

        # Titre
        title = QLabel(L("admin_password_title"))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            color: #0f172a; font-size: 18px;
            font-weight: bold; background: transparent;
        """)
        card_layout.addWidget(title)

        # Action demandée
        if action_text:
            action_lbl = QLabel(action_text)
            action_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            action_lbl.setStyleSheet("""
                color: #dc2626; font-size: 13px;
                font-weight: bold; background: transparent;
            """)
            card_layout.addWidget(action_lbl)

        # Champ mot de passe
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText(L("enter_password"))
        self.password_input.setMinimumHeight(44)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #f8fafc;
                color: #0f172a;
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                padding: 10px 14px;
                font-size: 14px;
            }
            QLineEdit:focus {
                background-color: #ffffff;
                border: 2px solid #6366f1;
            }
        """)
        self.password_input.returnPressed.connect(self._on_validate)
        card_layout.addWidget(self.password_input)

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

        ok_btn = QPushButton("✓ " + L("confirm"))
        ok_btn.setMinimumHeight(42)
        ok_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        ok_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6366f1, stop:1 #8b5cf6
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
                    stop:0 #4f46e5, stop:1 #7c3aed
                );
            }
        """)
        ok_btn.clicked.connect(self._on_validate)
        btn_row.addWidget(ok_btn)

        card_layout.addLayout(btn_row)
        outer.addWidget(card)

        self.password_input.setFocus()

    def _on_validate(self):
        L = lambda key: t(key, self.lang)
        password = self.password_input.text()

        if not password:
            QMessageBox.warning(self, L("warning"), L("enter_password"))
            return

        if verify_admin_password(password):
            self.accept()
        else:
            QMessageBox.warning(self, L("error"), L("wrong_admin_password"))
            self.password_input.clear()
            self.password_input.setFocus()