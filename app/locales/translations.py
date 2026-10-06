"""Traductions FR / AR / EN"""

TRANSLATIONS = {
    "fr": {
        # Sidebar
        "dashboard": "Tableau de bord",
        "sell_credit": "Vendre Délaire",
        "buy_credit": "Recharger Délaire",
        "cards": "Cartes",
        "history": "Historique",
        "reports": "Rapports",
        "settings": "Paramètres",

        # Common
        "refresh": "Actualiser",
        "cancel": "Annuler",
        "save": "Enregistrer",
        "confirm": "Confirmer",
        "close": "Fermer",
        "yes": "Oui",
        "no": "Non",
        "add": "Ajouter",
        "delete": "Supprimer",
        "edit": "Modifier",
        "search": "Rechercher",
        "language": "Langue",

        # Dashboard
        "balance": "Solde",
        "commission": "Commission",
        "cards_in_stock": "Cartes en stock",
        "today": "Aujourd'hui",
        "sold_credit": "Ventes délaire",
        "bought_credit": "Achats délaire",
        "sold_cards": "Cartes vendues",
        "profit_today": "Profit du jour",
        "total_balance": "Solde total",
        "total_stock": "Stock cartes",
        "transactions": "transaction(s)",
        "recharges_today": "Recharges du jour",
        "cards_sold": "carte(s)",
        "net_profit": "Bénéfice net",
        "on_3_operators": "Sur les 3 opérateurs",
        "all_denominations": "Toutes dénominations",

        # Vendre Délaire
        "sell_credit_title": "Vendre Délaire",
        "operator": "Opérateur",
        "amount_to_sell": "Montant à vendre (10 - 500 DH)",
        "client_pays": "Client paie",
        "balance_after": "Solde après",
        "validate_sale": "Valider la vente",
        "choose_operator": "Choisis un opérateur",
        "sale_success": "Vente réussie",
        "sale_success_msg": "Vente de {amount} DH {op} enregistrée !",
        "insufficient_balance": "Solde insuffisant",
        "insufficient_msg": "Solde {op} : {balance} DH\nRecharge ton délaire {op} d'abord.",

        # Recharger Délaire
        "buy_credit_title": "Recharger Délaire",
        "credit_to_receive": "Délaire à recevoir",
        "credit_received": "Solde reçu",
        "you_pay": "TU PAYES",
        "validate_recharge": "Valider la recharge",
        "recharge_success": "Recharge réussie",
        "recharge_success_msg": "Recharge {op} de {amount} DH effectuée !\nCommission : {commission} DH",

        # Cartes
        "cards_title": "Cartes de recharge",
        "buy_cards": "Acheter des cartes",
        "sell_cards": "Vendre des cartes",
        "denomination": "Montant",
        "stock": "Stock",
        "status": "Statut",
        "alert": "Alerte",
        "rupture": "Rupture",
        "low_stock": "Stock bas",
        "ok": "OK",
        "restock": "Réapprovisionner",
        "quantity": "Quantité",
        "unit_price": "Prix unitaire",
        "available_cards": "carte(s) disponible(s)",
        "buy_success": "{qty} cartes ajoutées au stock",
        "sell_success": "{qty} carte(s) vendue(s)",

        # Historique
        "history_title": "Historique",
        "all": "Tout",
        "credit": "Délaire",
        "card": "Cartes",
        "date": "Date",
        "type": "Type",
        "details": "Détails",
        "amount": "Montant",
        "profit": "Profit",
        "sale": "Vente",
        "recharge": "Recharge",

        # Rapports
        "reports_title": "Rapports",
        "global_state": "État global",
        "operator_detail": "Détail par opérateur",
        "total_balance_label": "Solde total",
        "total_stock_label": "Stock total cartes",
        "active_operators": "Opérateurs actifs",

        # Paramètres
        "settings_title": "Paramètres",
        "backup_title": "Sauvegarde de la base de données",
        "backup_hint": "Crée une copie de ta base de données dans un dossier de sauvegarde.\nRecommandé : fais-le chaque semaine pour protéger tes données.",
        "create_backup": "Créer une sauvegarde",
        "backup_done": "Sauvegarde créée",
        "backup_done_msg": "Fichier : {name}\n\nDossier : {folder}",
        "about": "À propos",
        "about_text": "📱 Recharge Manager v1.0\n\nApplication de gestion des recharges et cartes\nInwi · IAM · Orange\n\nBase de données : recharge.db\nFait avec Python + PySide6 + SQLite",

        # Alerts
        "warning": "Attention",
        "error": "Erreur",
        "success": "Succès",
        "recharge_500": "Recharger 500 DH",
        "quick_recharge": "Recharge rapide",
        "quick_recharge_msg": "Confirmer la recharge rapide ?",
        "chart_today": "Ventes du jour",

        # Dialogs
        "admin_password": "Mot de passe admin",
        "admin_password_title": "Confirmation administrateur",
        "enter_password": "Entrez le mot de passe",
        "wrong_admin_password": "Mot de passe admin incorrect",
        "edit_transaction": "Modifier la transaction",
        "current_amount": "Montant actuel",
        "new_amount": "Nouveau montant",
        "delete_transaction": "Supprimer la transaction",
        "confirm_delete_transaction": "Es-tu sûr de vouloir supprimer cette transaction ?",
        "no_selection": "Aucune sélection",
        "clear_all": "Vider tout",
        "clear_all_confirm": "⚠️ ATTENTION ! Cette action va SUPPRIMER TOUTES les transactions.\n\nLes soldes seront remis à 0 et les stocks de cartes à 0.\n\nContinuer ?",
        "clear_all_confirm2": "⚠️⚠️ DERNIÈRE CONFIRMATION !\n\nToutes les données seront PERDUES.\nEs-tu VRAIMENT sûr ?",
        "clear_all_done": "✅ Toutes les transactions ont été supprimées !",
        "edit_stock": "Modifier le stock",
        "edit_stock_title": "Modifier le stock",
        "current_stock": "Stock actuel",
        "new_stock": "Nouveau stock",
        "clear_stock": "Vider le stock",
        "clear_stock_confirm": "Mettre le stock à 0 ?",
        "clear_all_stocks": "Vider TOUS les stocks",
        "clear_all_stocks_confirm": "⚠️ Mettre TOUS les stocks à 0 ?",
        "stock_updated": "Stock mis à jour",
    },
    "ar": {
        # Sidebar
        "dashboard": "لوحة التحكم",
        "sell_credit": "بيع الرصيد",
        "buy_credit": "شحن الرصيد",
        "cards": "البطاقات",
        "history": "السجل",
        "reports": "التقارير",
        "settings": "الإعدادات",

        # Common
        "refresh": "تحديث",
        "cancel": "إلغاء",
        "save": "حفظ",
        "confirm": "تأكيد",
        "close": "إغلاق",
        "yes": "نعم",
        "no": "لا",
        "add": "إضافة",
        "delete": "حذف",
        "edit": "تعديل",
        "search": "بحث",
        "language": "اللغة",

        # Dashboard
        "balance": "الرصيد",
        "commission": "العمولة",
        "cards_in_stock": "البطاقات في المخزون",
        "today": "اليوم",
        "sold_credit": "مبيعات الرصيد",
        "bought_credit": "مشتريات الرصيد",
        "sold_cards": "البطاقات المباعة",
        "profit_today": "أرباح اليوم",
        "total_balance": "الرصيد الإجمالي",
        "total_stock": "مخزون البطاقات",
        "transactions": "عملية",
        "recharges_today": "شحن اليوم",
        "cards_sold": "بطاقة",
        "net_profit": "الربح الصافي",
        "on_3_operators": "على 3 مشغلين",
        "all_denominations": "جميع الفئات",

        # Vendre Délaire
        "sell_credit_title": "بيع الرصيد",
        "operator": "المشغل",
        "amount_to_sell": "المبلغ المراد بيعه (10 - 500 درهم)",
        "client_pays": "العميل يدفع",
        "balance_after": "الرصيد بعد",
        "validate_sale": "تأكيد البيع",
        "choose_operator": "اختر مشغلاً",
        "sale_success": "تم البيع بنجاح",
        "sale_success_msg": "تم تسجيل بيع {amount} درهم {op}!",
        "insufficient_balance": "رصيد غير كافٍ",
        "insufficient_msg": "رصيد {op} : {balance} درهم\nاشحن رصيد {op} أولاً.",

        # Recharger Délaire
        "buy_credit_title": "شحن الرصيد",
        "credit_to_receive": "الرصيد المراد استلامه",
        "credit_received": "الرصيد المستلم",
        "you_pay": "أنت تدفع",
        "validate_recharge": "تأكيد الشحن",
        "recharge_success": "تم الشحن بنجاح",
        "recharge_success_msg": "تم شحن {op} بمبلغ {amount} درهم!\nالعمولة : {commission} درهم",

        # Cartes
        "cards_title": "بطاقات الشحن",
        "buy_cards": "شراء بطاقات",
        "sell_cards": "بيع بطاقات",
        "denomination": "الفئة",
        "stock": "المخزون",
        "status": "الحالة",
        "alert": "تنبيه",
        "rupture": "نفد",
        "low_stock": "مخزون منخفض",
        "ok": "جيد",
        "restock": "إعادة التخزين",
        "quantity": "الكمية",
        "unit_price": "سعر الوحدة",
        "available_cards": "بطاقة متوفرة",
        "buy_success": "تمت إضافة {qty} بطاقة للمخزون",
        "sell_success": "تم بيع {qty} بطاقة",

        # Historique
        "history_title": "السجل",
        "all": "الكل",
        "credit": "الرصيد",
        "card": "البطاقات",
        "date": "التاريخ",
        "type": "النوع",
        "details": "التفاصيل",
        "amount": "المبلغ",
        "profit": "الربح",
        "sale": "بيع",
        "recharge": "شحن",

        # Rapports
        "reports_title": "التقارير",
        "global_state": "الحالة العامة",
        "operator_detail": "التفصيل حسب المشغل",
        "total_balance_label": "الرصيد الإجمالي",
        "total_stock_label": "إجمالي البطاقات",
        "active_operators": "المشغلون النشطون",

        # Paramètres
        "settings_title": "الإعدادات",
        "backup_title": "نسخ احتياطي لقاعدة البيانات",
        "backup_hint": "أنشئ نسخة من قاعدة البيانات في مجلد النسخ الاحتياطي.\nيُنصح به أسبوعياً لحماية بياناتك.",
        "create_backup": "إنشاء نسخة احتياطية",
        "backup_done": "تم إنشاء النسخة",
        "backup_done_msg": "الملف : {name}\n\nالمجلد : {folder}",
        "about": "حول",
        "about_text": "📱 مدير الشحن v1.0\n\nتطبيق إدارة الشحن والبطاقات\nإنوي · اتصالات المغرب · أورنج\n\nقاعدة البيانات : recharge.db\nمصنوع بـ Python + PySide6 + SQLite",

        # Alerts
        "warning": "تنبيه",
        "error": "خطأ",
        "success": "نجاح",
        "recharge_500": "شحن 500 درهم",
        "quick_recharge": "شحن سريع",
        "quick_recharge_msg": "تأكيد الشحن السريع؟",
        "chart_today": "مبيعات اليوم",

        # Dialogs
        "admin_password": "كلمة مرور المدير",
        "admin_password_title": "تأكيد المدير",
        "enter_password": "أدخل كلمة المرور",
        "wrong_admin_password": "كلمة مرور المدير غير صحيحة",
        "edit_transaction": "تعديل العملية",
        "current_amount": "المبلغ الحالي",
        "new_amount": "المبلغ الجديد",
        "delete_transaction": "حذف العملية",
        "confirm_delete_transaction": "هل أنت متأكد من حذف هذه العملية؟",
        "no_selection": "لا يوجد اختيار",
        "clear_all": "حذف الكل",
        "clear_all_confirm": "⚠️ تحذير! هذا الإجراء سيحذف جميع العمليات.\n\nسيتم إعادة الأرصدة إلى 0 والمخزون إلى 0.\n\nهل تريد المتابعة؟",
        "clear_all_confirm2": "⚠️⚠️ التأكيد الأخير!\n\nستفقد جميع البيانات.\nهل أنت متأكد تماماً؟",
        "clear_all_done": "✅ تم حذف جميع العمليات!",
        "edit_stock": "تعديل المخزون",
        "edit_stock_title": "تعديل المخزون",
        "current_stock": "المخزون الحالي",
        "new_stock": "المخزون الجديد",
        "clear_stock": "إفراغ المخزون",
        "clear_stock_confirm": "هل تريد وضع المخزون على 0؟",
        "clear_all_stocks": "إفراغ جميع المخزونات",
        "clear_all_stocks_confirm": "⚠️ وضع جميع المخزونات على 0؟",
        "stock_updated": "تم تحديث المخزون",
    },
    "en": {
        # Sidebar
        "dashboard": "Dashboard",
        "sell_credit": "Sell Credit",
        "buy_credit": "Buy Credit",
        "cards": "Cards",
        "history": "History",
        "reports": "Reports",
        "settings": "Settings",

        # Common
        "refresh": "Refresh",
        "cancel": "Cancel",
        "save": "Save",
        "confirm": "Confirm",
        "close": "Close",
        "yes": "Yes",
        "no": "No",
        "add": "Add",
        "delete": "Delete",
        "edit": "Edit",
        "search": "Search",
        "language": "Language",

        # Dashboard
        "balance": "Balance",
        "commission": "Commission",
        "cards_in_stock": "Cards in stock",
        "today": "Today",
        "sold_credit": "Credit sold",
        "bought_credit": "Credit bought",
        "sold_cards": "Cards sold",
        "profit_today": "Today's profit",
        "total_balance": "Total balance",
        "total_stock": "Cards stock",
        "transactions": "transaction(s)",
        "recharges_today": "Recharges today",
        "cards_sold": "card(s)",
        "net_profit": "Net profit",
        "on_3_operators": "On 3 operators",
        "all_denominations": "All denominations",

        # Vendre Délaire
        "sell_credit_title": "Sell Credit",
        "operator": "Operator",
        "amount_to_sell": "Amount to sell (10 - 500 DH)",
        "client_pays": "Client pays",
        "balance_after": "Balance after",
        "validate_sale": "Validate sale",
        "choose_operator": "Choose an operator",
        "sale_success": "Sale successful",
        "sale_success_msg": "Sale of {amount} DH {op} recorded!",
        "insufficient_balance": "Insufficient balance",
        "insufficient_msg": "{op} balance: {balance} DH\nRecharge {op} first.",

        # Recharger Délaire
        "buy_credit_title": "Buy Credit",
        "credit_to_receive": "Credit to receive",
        "credit_received": "Credit received",
        "you_pay": "YOU PAY",
        "validate_recharge": "Validate recharge",
        "recharge_success": "Recharge successful",
        "recharge_success_msg": "{op} recharge of {amount} DH done!\nCommission: {commission} DH",

        # Cartes
        "cards_title": "Recharge Cards",
        "buy_cards": "Buy cards",
        "sell_cards": "Sell cards",
        "denomination": "Amount",
        "stock": "Stock",
        "status": "Status",
        "alert": "Alert",
        "rupture": "Out of stock",
        "low_stock": "Low stock",
        "ok": "OK",
        "restock": "Restock",
        "quantity": "Quantity",
        "unit_price": "Unit price",
        "available_cards": "card(s) available",
        "buy_success": "{qty} cards added to stock",
        "sell_success": "{qty} card(s) sold",

        # Historique
        "history_title": "History",
        "all": "All",
        "credit": "Credit",
        "card": "Cards",
        "date": "Date",
        "type": "Type",
        "details": "Details",
        "amount": "Amount",
        "profit": "Profit",
        "sale": "Sale",
        "recharge": "Recharge",

        # Rapports
        "reports_title": "Reports",
        "global_state": "Global state",
        "operator_detail": "Detail by operator",
        "total_balance_label": "Total balance",
        "total_stock_label": "Total cards stock",
        "active_operators": "Active operators",

        # Paramètres
        "settings_title": "Settings",
        "backup_title": "Database backup",
        "backup_hint": "Creates a copy of your database in a backup folder.\nRecommended: do it weekly to protect your data.",
        "create_backup": "Create backup",
        "backup_done": "Backup created",
        "backup_done_msg": "File: {name}\n\nFolder: {folder}",
        "about": "About",
        "about_text": "📱 Recharge Manager v1.0\n\nRecharge and card management app\nInwi · IAM · Orange\n\nDatabase: recharge.db\nMade with Python + PySide6 + SQLite",

        # Alerts
        "warning": "Warning",
        "error": "Error",
        "success": "Success",
        "recharge_500": "Recharge 500 DH",
        "quick_recharge": "Quick Recharge",
        "quick_recharge_msg": "Confirm quick recharge?",
        "chart_today": "Today's sales",

        # Dialogs
        "admin_password": "Admin Password",
        "admin_password_title": "Admin Confirmation",
        "enter_password": "Enter password",
        "wrong_admin_password": "Wrong admin password",
        "edit_transaction": "Edit Transaction",
        "current_amount": "Current Amount",
        "new_amount": "New Amount",
        "delete_transaction": "Delete Transaction",
        "confirm_delete_transaction": "Are you sure you want to delete this transaction?",
        "no_selection": "No selection",
        "clear_all": "Clear All",
        "clear_all_confirm": "⚠️ WARNING! This will DELETE ALL transactions.\n\nBalances will be reset to 0 and card stocks to 0.\n\nContinue?",
        "clear_all_confirm2": "⚠️⚠️ FINAL CONFIRMATION!\n\nAll data will be LOST.\nAre you REALLY sure?",
        "clear_all_done": "✅ All transactions have been deleted!",
        "edit_stock": "Edit Stock",
        "edit_stock_title": "Edit Stock",
        "current_stock": "Current Stock",
        "new_stock": "New Stock",
        "clear_stock": "Clear Stock",
        "clear_stock_confirm": "Set stock to 0?",
        "clear_all_stocks": "Clear ALL stocks",
        "clear_all_stocks_confirm": "⚠️ Set ALL stocks to 0?",
        "stock_updated": "Stock updated",
    },
}


def t(key: str, lang: str = "fr") -> str:
    """Traduit une clé dans la langue donnée."""
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS["fr"])
    return lang_dict.get(key, TRANSLATIONS["fr"].get(key, key))


def get_current_language() -> str:
    """Lit la langue actuelle depuis la DB."""
    from app.db.database import get_connection
    conn = get_connection()
    row = conn.execute("SELECT value FROM settings WHERE key = 'language'").fetchone()
    conn.close()
    return row["value"] if row else "fr"


def set_language(lang: str) -> None:
    """Sauvegarde la langue dans la DB."""
    from app.db.database import get_connection
    conn = get_connection()
    conn.execute("""
        INSERT INTO settings (key, value) VALUES ('language', ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
    """, (lang,))
    conn.commit()
    conn.close()