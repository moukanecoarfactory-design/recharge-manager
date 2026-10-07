@@ -1,69 +0,0 @@
# 📱 Recharge Manager

Application de gestion de recharge délaire et cartes pour Inwi, IAM et Orange.

## ✨ Fonctionnalités

- 💰 **Vendre Délaire** : vends du crédit aux clients
- 📥 **Recharger Délaire** : recharge ton crédit
- 🎫 **Cartes** : gère ton stock de cartes
- 📜 **Historique** : consulte tes transactions
- 💵 **Caisse** : suivi automatique
- 📊 **Rapports** : statistiques
- ⚙️ **Paramètres** : langue, sécurité, backup

  ## 📸 Captures d'écran

### 🏠 Tableau de bord
![Tableau de bord](screenshots/01_dashboard.png)

*Vue d'ensemble : caisse, soldes opérateurs et graphique des ventes*

### 💰 Vendre Délaire
![Vendre Délaire](screenshots/02_sell.png)

*Sélection de l'opérateur et validation de vente*

### 📥 Recharger Délaire
![Recharger Délaire](screenshots/03_buy.png)

*Rechargement avec calcul automatique des commissions*

### 🎫 Gestion des Cartes
![Cartes](screenshots/04_cards.png)

*Stock, alertes et mouvements de cartes prépayées*

### 📜 Historique
![Historique](screenshots/05_history.png)

*Toutes les transactions avec filtres et totaux*

### 💵 Caisse
![Caisse](screenshots/06_cash.png)

*Suivi automatique du fond de caisse*

### 📊 Rapports
![Rapports](screenshots/07_reports.png)

*Statistiques par opérateur et période*

### ⚙️ Paramètres
![Paramètres](screenshots/08_settings.png)

*Configuration, sécurité et sauvegardes*

## 🛠️ Technologies

- Python 3.14
- PySide6 (Qt6)
- SQLite

## 🚀 Installation

```bash
git clone https://github.com/TON_USERNAME/recharge-manager.git
cd recharge-manager
pip install -r requirements.txt
python main.py
