"""Paramètres — design PRO SOFT."""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QMessageBox, QGraphicsDropShadowEffect,
    QScrollArea, QDialog, QLineEdit, QFormLayout,
    QDialogButtonBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from app.db.database import DB_PATH
from app.db.settings_repo import (
    verify_admin_password, set_admin_password, get_setting, set_setting
)
from app.locales.translations import t, get_current_language, set_language
from app.ui.admin_password_dialog import AdminPasswordDialog
from app.ui.styles import (
    btn_secondary, input_style, label_title,
    WHITE, BORDER, TEXT_DARK, TEXT_LIGHT, TEXT_MEDIUM, BG_LIGHT
)
from pathlib import Path
from datetime import datetime


# ============================================================
# CARD WRAPPER
# ============================================================
class SectionCard(QFrame):
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
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 20, 24, 20)
        self.layout.setSpacing(12)


# ============================================================
# DIALOG CHANGER MOT DE PASSE
# ============================================================
class ChangePasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lang = get_current_language()
        L = lambda key: t(key, self.lang)

        self.setWindowTitle("🔐 Changer le mot de passe")
        self.setMinimumWidth(420)
        self.setStyleSheet(f"QDialog {{ background-color: {WHITE}; }}")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(14)

        title = QLabel("🔐 Changer le mot de passe admin")
        title.setStyleSheet(f"color: {TEXT_DARK}; font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(10)

        self.old_pw = QLineEdit()
        self.old_pw.setEchoMode(QLineEdit.EchoMode.Password)
        self.old_pw.setMinimumHeight(38)
        self.old_pw.setStyleSheet(input_style())
        form.addRow("Ancien mot de passe :", self.old_pw)

        self.new_pw = QLineEdit()
        self.new_pw.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_pw.setMinimumHeight(38)
        self.new_pw.setStyleSheet(input_style())
        form.addRow("Nouveau mot de passe :", self.new_pw)

        self.confirm_pw = QLineEdit()
        self.confirm_pw.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_pw.setMinimumHeight(38)
        self.confirm_pw.setStyleSheet(input_style())
        form.addRow("Confirmer :", self.confirm_pw)

        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText("✓ Enregistrer")
        buttons.button(QDialogButtonBox.Cancel).setText(L("cancel"))
        buttons.accepted.connect(self._on_validate)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _on_validate(self):
        old = self.old_pw.text()
        new = self.new_pw.text()
        confirm = self.confirm_pw.text()

        if not verify_admin_password(old):
            QMessageBox.warning(self, "Erreur", "Ancien mot de passe incorrect.")
            return

        if len(new) < 3:
            QMessageBox.warning(self, "Erreur", "Nouveau mot de passe trop court (min 3 caractères).")
            return

        if new != confirm:
            QMessageBox.warning(self, "Erreur", "Les deux mots de passe ne correspondent pas.")
            return

        set_admin_password(new)
        QMessageBox.information(self, "✅ Succès", "Mot de passe changé avec succès !")
        self.accept()


# ============================================================
# PAGE PARAMÈTRES V2
# ============================================================
class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.lang = get_current_language()
        L = lambda key: t(key, self.lang)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 24, 24, 24)
        outer.setSpacing(14)

        # Header
        header = QHBoxLayout()
        title = QLabel("⚙️ " + L("settings_title"))
        title.setStyleSheet(label_title())
        header.addWidget(title)
        header.addStretch()
        outer.addLayout(header)

        # Scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        content = QWidget()
        content.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(14)

        # ============================================================
        # 🌍 LANGUE
        # ============================================================
        lang_card = SectionCard()
        lang_title = QLabel("🌍 " + L("language"))
        lang_title.setStyleSheet(f"color: {TEXT_DARK}; font-size: 15px; font-weight: bold;")
        lang_card.layout.addWidget(lang_title)

        lang_hint = QLabel("Choisis la langue de l'interface. Redémarre l'appli après changement.")
        lang_hint.setStyleSheet(f"color: {TEXT_LIGHT}; font-size: 12px;")
        lang_card.layout.addWidget(lang_hint)

        lang_btns = QHBoxLayout()
        lang_btns.setSpacing(8)

        self.lang_buttons = {}
        for label, code in [
            ("🇫🇷 Français", "fr"),
            ("🇸🇦 العربية", "ar"),
            ("🇬🇧 English", "en"),
        ]:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setMinimumHeight(40)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #ffffff;
                    color: #334155;
                    border: 1.5px solid #e2e8f0;
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
            btn.clicked.connect(lambda _, c=code: self.change_lang(c))
            if code == self.lang:
                btn.setChecked(True)
            self.lang_buttons[code] = btn
            lang_btns.addWidget(btn)

        lang_btns.addStretch()
        lang_card.layout.addLayout(lang_btns)
        content_layout.addWidget(lang_card)

        # ============================================================
        # 🔐 SÉCURITÉ
        # ============================================================
        sec_card = SectionCard()
        sec_title = QLabel("🔐 Sécurité")
        sec_title.setStyleSheet(f"color: {TEXT_DARK}; font-size: 15px; font-weight: bold;")
        sec_card.layout.addWidget(sec_title)

        sec_hint = QLabel("Mot de passe requis pour : suppressions, modifications, reset complet.")
        sec_hint.setStyleSheet(f"color: {TEXT_LIGHT}; font-size: 12px;")
        sec_card.layout.addWidget(sec_hint)

        change_pw_btn = QPushButton("🔑 Changer le mot de passe admin")
        change_pw_btn.setMinimumHeight(42)
        change_pw_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        change_pw_btn.setStyleSheet("""
            QPushButton {
                background-color: #6366f115;
                color: #6366f1;
                border: 1.5px solid #6366f140;
                padding: 10px 22px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #6366f125;
                border: 1.5px solid #6366f1;
            }
        """)
        change_pw_btn.clicked.connect(self.on_change_password)

        pw_row = QHBoxLayout()
        pw_row.addWidget(change_pw_btn)
        pw_row.addStretch()
        sec_card.layout.addLayout(pw_row)
        content_layout.addWidget(sec_card)

        # ============================================================
        # 💾 SAUVEGARDE
        # ============================================================
        backup_card = SectionCard()
        backup_title = QLabel("💾 " + L("backup_title"))
        backup_title.setStyleSheet(f"color: {TEXT_DARK}; font-size: 15px; font-weight: bold;")
        backup_card.layout.addWidget(backup_title)

        backup_hint = QLabel(L("backup_hint"))
        backup_hint.setWordWrap(True)
        backup_hint.setStyleSheet(f"color: {TEXT_LIGHT}; font-size: 12px;")
        backup_card.layout.addWidget(backup_hint)

        # Info dernière sauvegarde
        self.last_backup_lbl = QLabel("")
        self.last_backup_lbl.setStyleSheet(f"""
            color: {TEXT_MEDIUM};
            font-size: 12px;
            background-color: {BG_LIGHT};
            border-radius: 8px;
            padding: 10px;
        """)
        backup_card.layout.addWidget(self.last_backup_lbl)

        backup_btns = QHBoxLayout()
        backup_btns.setSpacing(8)

        create_backup_btn = QPushButton("📁 " + L("create_backup"))
        create_backup_btn.setMinimumHeight(42)
        create_backup_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        create_backup_btn.setStyleSheet("""
            QPushButton {
                background-color: #16a34a15;
                color: #16a34a;
                border: 1.5px solid #16a34a40;
                padding: 10px 22px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #16a34a25;
                border: 1.5px solid #16a34a;
            }
        """)
        create_backup_btn.clicked.connect(self.on_backup)
        backup_btns.addWidget(create_backup_btn)

        open_folder_btn = QPushButton("📂 Ouvrir le dossier")
        open_folder_btn.setMinimumHeight(42)
        open_folder_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        open_folder_btn.setStyleSheet(btn_secondary())
        open_folder_btn.clicked.connect(self.on_open_backup_folder)
        backup_btns.addWidget(open_folder_btn)

        backup_btns.addStretch()
        backup_card.layout.addLayout(backup_btns)
        content_layout.addWidget(backup_card)

        # ============================================================
        # ⚠️ ZONE DANGEREUSE
        # ============================================================
        danger_card = SectionCard()
        danger_card.setStyleSheet(f"""
            QFrame {{
                background-color: #fef2f2;
                border-radius: 14px;
                border: 1.5px solid #fecaca;
            }}
        """)
        danger_title = QLabel("⚠️ Zone dangereuse")
        danger_title.setStyleSheet("color: #dc2626; font-size: 15px; font-weight: bold;")
        danger_card.layout.addWidget(danger_title)

        danger_hint = QLabel(
            "Cette action remet TOUT à zéro : soldes, stocks, transactions, "
            "caisse, mot de passe et langue. Action IRRÉVERSIBLE."
        )
        danger_hint.setWordWrap(True)
        danger_hint.setStyleSheet("color: #991b1b; font-size: 12px;")
        danger_card.layout.addWidget(danger_hint)

        reset_btn = QPushButton("🗑️ Réinitialiser TOUTES les données")
        reset_btn.setMinimumHeight(42)
        reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc2626;
                color: white;
                border: none;
                padding: 10px 22px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #b91c1c; }
        """)
        reset_btn.clicked.connect(self.on_reset_all)

        reset_row = QHBoxLayout()
        reset_row.addWidget(reset_btn)
        reset_row.addStretch()
        danger_card.layout.addLayout(reset_row)
        content_layout.addWidget(danger_card)

        # ============================================================
        # ℹ️ À PROPOS
        # ============================================================
        about_card = SectionCard()
        about_title = QLabel("ℹ️ " + L("about"))
        about_title.setStyleSheet(f"color: {TEXT_DARK}; font-size: 15px; font-weight: bold;")
        about_card.layout.addWidget(about_title)

        about_text = QLabel(L("about_text"))
        about_text.setWordWrap(True)
        about_text.setStyleSheet(f"color: {TEXT_MEDIUM}; font-size: 12px; line-height: 1.6;")
        about_card.layout.addWidget(about_text)
        content_layout.addWidget(about_card)

        content_layout.addStretch()
        scroll.setWidget(content)
        outer.addWidget(scroll)

        # Rafraîchir la date de sauvegarde
        self.update_last_backup()

    # ============================================================
    # LANGUE
    # ============================================================
    def change_lang(self, code):
        if code == self.lang:
            return

        confirm = QMessageBox.question(
            self, "Changer la langue",
            f"Changer la langue en {code.upper()} ?\nRedémarre l'appli après.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            set_language(code)
            QMessageBox.information(
                self, "✅",
                "Langue changée ! Redémarre l'application pour appliquer."
            )
        else:
            # Revert
            for c, btn in self.lang_buttons.items():
                btn.setChecked(c == self.lang)

    # ============================================================
    # MOT DE PASSE
    # ============================================================
    def on_change_password(self):
        dlg = ChangePasswordDialog(self)
        dlg.exec()

    # ============================================================
    # SAUVEGARDE
    # ============================================================
    def get_backups_dir(self):
        backups_dir = DB_PATH.parent / "backups"
        backups_dir.mkdir(exist_ok=True)
        return backups_dir

    def update_last_backup(self):
        backups_dir = self.get_backups_dir()
        backups = sorted(backups_dir.glob("recharge_backup_*.db"), reverse=True)
        if backups:
            last = backups[0]
            timestamp = last.stem.replace("recharge_backup_", "")
            try:
                dt = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
                date_str = dt.strftime("%d/%m/%Y à %H:%M")
                self.last_backup_lbl.setText(
                    f"📅 Dernière sauvegarde : {date_str}\n"
                    f"📁 Fichier : {last.name}\n"
                    f"📊 Total : {len(backups)} sauvegarde(s)"
                )
            except Exception:
                self.last_backup_lbl.setText(f"📅 Dernière : {last.name}")
        else:
            self.last_backup_lbl.setText("⚠️ Aucune sauvegarde créée pour le moment")

    def on_backup(self):
        L = lambda key: t(key, self.lang)
        import shutil
        try:
            backups_dir = self.get_backups_dir()
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = backups_dir / f"recharge_backup_{ts}.db"
            shutil.copy2(DB_PATH, backup_file)
            QMessageBox.information(
                self, "✅ " + L("backup_done"),
                L("backup_done_msg").replace("{name}", backup_file.name)
                                     .replace("{folder}", str(backups_dir))
            )
            self.update_last_backup()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def on_open_backup_folder(self):
        import subprocess
        import os
        backups_dir = self.get_backups_dir()
        try:
            if os.name == "nt":
                os.startfile(backups_dir)
            elif os.name == "posix":
                subprocess.Popen(["xdg-open", str(backups_dir)])
        except Exception as e:
            QMessageBox.warning(self, "Info", f"Dossier : {backups_dir}")

    # ============================================================
    # RESET COMPLET
    # ============================================================
    def on_reset_all(self):
        # Double confirmation + mot de passe admin
        dlg = AdminPasswordDialog(
            self,
            action_text="Réinitialiser TOUTES les données"
        )
        if not dlg.exec():
            return

        confirm1 = QMessageBox.warning(
            self, "⚠️ Réinitialisation",
            "⚠️ ATTENTION !\n\n"
            "Cette action va TOUT supprimer :\n"
            "• Soldes délaire\n"
            "• Stocks de cartes\n"
            "• Historique complet\n"
            "• Caisse (retour à 1000 DH)\n"
            "• Mot de passe (retour à 'admin')\n"
            "• Langue (retour à FR)\n\n"
            "Continuer ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm1 != QMessageBox.StandardButton.Yes:
            return

        confirm2 = QMessageBox.warning(
            self, "⚠️⚠️ DERNIÈRE CONFIRMATION",
            "Es-tu VRAIMENT sûr ?\n\nCette action est IRRÉVERSIBLE.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm2 != QMessageBox.StandardButton.Yes:
            return

        try:
            from app.db.transaction_repo import clear_all_transactions
            from app.db.cash_repo import reset_cash, set_initial_cash

            clear_all_transactions()

            # 🆕 Réinitialiser la caisse
            reset_cash()
            set_initial_cash(1000)

            # Réinitialiser les paramètres
            import hashlib
            set_setting("admin_password",
                        hashlib.sha256("admin".encode()).hexdigest())
            set_setting("language", "fr")
            set_setting("low_stock_alert", "5")
            set_setting("low_balance_alert", "50")

            QMessageBox.information(
                self, "✅ Terminé",
                "Toutes les données ont été réinitialisées.\n\n"
                "Redémarre l'application."
            )
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))