from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFrame
)
from PySide6.QtCore import Qt

from app.locales.translations import t, get_current_language
from app.ui.dashboard_page import DashboardPage
from app.ui.sell_credit_page import SellCreditPage
from app.ui.buy_credit_page import BuyCreditPage
from app.ui.cards_page import CardsPage
from app.ui.history_page import HistoryPage
from app.ui.cash_page import CashPage
from app.ui.reports_page import ReportsPage
from app.ui.settings_page import SettingsPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lang = get_current_language()
        L = lambda key: t(key, self.lang)

        self.setWindowTitle("Recharge Manager")
        self.resize(1280, 780)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ================= SIDEBAR =================
        sidebar = QFrame()
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0f172a, stop:1 #1e293b
                );
                border-right: 1px solid #334155;
            }
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        # Logo
        logo_frame = QFrame()
        logo_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0ea5e9, stop:1 #6366f1
                );
                border: none;
            }
        """)
        logo_frame.setFixedHeight(90)
        logo_layout = QVBoxLayout(logo_frame)
        logo_layout.setContentsMargins(20, 14, 20, 14)
        logo_layout.setSpacing(2)

        title = QLabel("📱 Recharge Manager")
        title.setStyleSheet("""
            color: white; font-size: 16px;
            font-weight: bold; background: transparent;
        """)
        logo_layout.addWidget(title)

        subtitle = QLabel("Inwi · IAM · Orange")
        subtitle.setStyleSheet("""
            color: #e0f2fe; font-size: 10px;
            background: transparent;
        """)
        logo_layout.addWidget(subtitle)

        sidebar_layout.addWidget(logo_frame)

        # Navigation
        self.nav_buttons = []
        pages = [
            ("🏠  " + L("dashboard"),    0),
            ("💰  " + L("sell_credit"),  1),
            ("📥  " + L("buy_credit"),   2),
            ("🎫  " + L("cards"),        3),
            ("📜  " + L("history"),      4),
            ("💵  Caisse",               5),  # 🆕
            ("📊  " + L("reports"),      6),
            ("⚙️   " + L("settings"),    7),
        ]

        nav_container = QVBoxLayout()
        nav_container.setContentsMargins(8, 12, 8, 12)
        nav_container.setSpacing(2)

        for label, idx in pages:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    color: #cbd5e1;
                    background: transparent;
                    text-align: left;
                    padding: 12px 18px;
                    font-size: 14px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.06);
                    color: white;
                }
                QPushButton:checked {
                    background: qlineargradient(
                        x1:0, y1:0, x2:1, y2:0,
                        stop:0 #0ea5e9, stop:1 #6366f1
                    );
                    color: white;
                    font-weight: bold;
                }
            """)
            btn.clicked.connect(lambda checked=False, i=idx: self.switch_page(i))
            nav_container.addWidget(btn)
            self.nav_buttons.append(btn)

        sidebar_layout.addLayout(nav_container)
        sidebar_layout.addStretch()

        # Footer
        footer = QLabel("v1.0")
        footer.setStyleSheet("""
            color: #475569; font-size: 10px;
            padding: 6px 18px; background: transparent;
        """)
        sidebar_layout.addWidget(footer)

        # ================= CONTENT =================
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background-color: #f1f5f9;")

        # Toutes les pages
        self.stack.addWidget(DashboardPage())       # 0
        self.stack.addWidget(SellCreditPage())      # 1
        self.stack.addWidget(BuyCreditPage())       # 2
        self.stack.addWidget(CardsPage())           # 3
        self.stack.addWidget(HistoryPage())         # 4
        self.stack.addWidget(CashPage())            # 5  🆕
        self.stack.addWidget(ReportsPage())         # 6
        self.stack.addWidget(SettingsPage())        # 7

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stack, 1)

        self.nav_buttons[0].setChecked(True)
        self.stack.setCurrentIndex(0)

    def switch_page(self, index: int):
        self.stack.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)