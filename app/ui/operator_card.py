"""Widget carte opérateur — design PRO SOFT."""
from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QProgressBar, QGraphicsDropShadowEffect, QMessageBox
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QColor

from app.db.operator_repo import get_operator
from app.db.settings_repo import get_low_balance_alert
from app.db.transaction_repo import buy_credit
from app.locales.translations import t, get_current_language
from app.ui.logo_widget import OperatorLogo


def hex_to_rgb(hex_color: str):
    """Convertit #RRGGBB en (r, g, b)."""
    c = hex_color.lstrip("#")
    return int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)


class OperatorCard(QFrame):
    clicked = Signal(int)

    def __init__(self, operator, lang=None, show_recharge=True):
        super().__init__()
        self.operator = operator
        self.lang = lang or get_current_language()
        self.show_recharge = show_recharge
        self.pulse_state = False
        self.low_threshold = get_low_balance_alert()

        self._build_ui()

        self.pulse_timer = QTimer()
        self.pulse_timer.setInterval(600)
        self.pulse_timer.timeout.connect(self._pulse)

        self._check_alert()

    def _build_ui(self):
        op = self.operator
        L = lambda key: t(key, self.lang)
        r, g, b = hex_to_rgb(op.color)

        self.setMinimumHeight(230)
        self.setStyleSheet(self._normal_style())

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(24)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 20))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(14)

        # Header
        header = QHBoxLayout()
        header.setSpacing(16)

        logo = OperatorLogo(
            code=op.code, name=op.name,
            color=op.color, size=64
        )
        header.addWidget(logo)

        name_col = QVBoxLayout()
        name_col.setSpacing(4)

        name_row = QHBoxLayout()
        name_row.setSpacing(6)

        name_lbl = QLabel(op.name)
        name_lbl.setStyleSheet(f"""
            color: {op.color};
            font-size: 20px;
            font-weight: bold;
            background: transparent;
        """)
        name_row.addWidget(name_lbl)

        self.alert_icon = QLabel("")
        self.alert_icon.setStyleSheet("font-size: 15px; background: transparent;")
        name_row.addWidget(self.alert_icon)
        name_row.addStretch()

        name_col.addLayout(name_row)

        comm_lbl = QLabel(f"{t('commission', self.lang)} : {op.commission}%")
        comm_lbl.setStyleSheet(f"""
            color: {op.color};
            font-size: 12px;
            font-weight: bold;
            background: transparent;
        """)
        name_col.addWidget(comm_lbl)

        header.addLayout(name_col)
        header.addStretch()
        layout.addLayout(header)

        # Solde
        self.balance_lbl = QLabel(f"{op.balance:.2f} DH")
        self.balance_lbl.setStyleSheet(f"""
            color: {op.color};
            font-size: 28px;
            font-weight: bold;
            background: transparent;
        """)
        layout.addWidget(self.balance_lbl)

        # Progress
        self.progress = QProgressBar()
        self.progress.setRange(0, 1000)
        self.progress.setValue(min(int(op.balance), 1000))
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(8)
        self.progress.setStyleSheet(f"""
            QProgressBar {{
                background-color: #f1f5f9;
                border-radius: 4px;
                border: none;
            }}
            QProgressBar::chunk {{
                background-color: {op.color};
                border-radius: 4px;
            }}
        """)
        layout.addWidget(self.progress)

        # Bouton recharge pastel avec rgba()
        self.recharge_btn = QPushButton("⚡ Recharger 500 DH")
        self.recharge_btn.setFixedHeight(38)
        self.recharge_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.recharge_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba({r}, {g}, {b}, 0.12);
                color: {op.color};
                border: 1.5px solid rgba({r}, {g}, {b}, 0.4);
                border-radius: 10px;
                font-weight: bold;
                font-size: 13px;
                padding: 6px 14px;
            }}
            QPushButton:hover {{
                background-color: rgba({r}, {g}, {b}, 0.22);
                border: 1.5px solid {op.color};
            }}
        """)
        self.recharge_btn.clicked.connect(self._on_recharge_click)
        self.recharge_btn.setVisible(False)
        layout.addWidget(self.recharge_btn)

        layout.addStretch()

    def _normal_style(self):
        return """
            OperatorCard {
                background-color: #ffffff;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
            }
        """

    def _alert_style(self):
        return """
            OperatorCard {
                background-color: #fef2f2;
                border-radius: 16px;
                border: 1.5px solid #fecaca;
            }
        """

    def _alert_style_pulse(self):
        return """
            OperatorCard {
                background-color: #fee2e2;
                border-radius: 16px;
                border: 1.5px solid #fca5a5;
            }
        """

    def _check_alert(self):
        if self.operator.balance < self.low_threshold:
            self.setStyleSheet(self._alert_style())
            self.alert_icon.setText("⚠️")
            self.alert_icon.setStyleSheet("font-size: 15px; background: transparent; color: #dc2626;")
            if self.show_recharge:
                self.recharge_btn.setVisible(True)
            if not self.pulse_timer.isActive():
                self.pulse_timer.start()
        else:
            self.setStyleSheet(self._normal_style())
            self.alert_icon.setText("")
            self.recharge_btn.setVisible(False)
            self.pulse_timer.stop()

    def _pulse(self):
        if self.pulse_state:
            self.setStyleSheet(self._alert_style_pulse())
        else:
            self.setStyleSheet(self._alert_style())
        self.pulse_state = not self.pulse_state

    def _on_recharge_click(self):
        L = lambda key: t(key, self.lang)
        op = get_operator(self.operator.id)

        confirm = QMessageBox.question(
            self,
            "⚡ " + L("quick_recharge"),
            f"{L('quick_recharge_msg')}\n\n"
            f"👤 {op.name}\n"
            f"💰 {L('credit_received')} : 500.00 DH\n"
            f"📊 {L('commission')} : {op.commission}%",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                buy_credit(op.id, 500)
                commission = 500 * (op.commission / 100)
                QMessageBox.information(
                    self, "✅ " + L("success"),
                    L("recharge_success_msg").replace("{op}", op.name)
                                              .replace("{amount}", "500.00")
                                              .replace("{commission}", f"{commission:.2f}")
                )
                self.clicked.emit(op.id)
            except Exception as e:
                QMessageBox.critical(self, L("error"), str(e))