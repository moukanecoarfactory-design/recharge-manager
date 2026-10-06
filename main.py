print("🚀🚀🚀 MAIN.PY DÉMARRÉ 🚀🚀🚀")

import sys
from PySide6.QtWidgets import QApplication

from app.db.database import init_database
from app.ui.main_window import MainWindow


def main():
    print("🚀 MAIN() APPELÉE")
    init_database()
    print("🚀 DB INITIALISÉE")

    app = QApplication(sys.argv)
    app.setApplicationName("Recharge Manager")

    print("🚀 CRÉATION FENÊTRE")
    window = MainWindow()
    print("🚀 FENÊTRE CRÉÉE")

    window.show()
    print("🚀 FENÊTRE AFFICHÉE")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
import sys
from PySide6.QtWidgets import QApplication

from app.db.database import init_database
from app.ui.main_window import MainWindow


def main():
    # Créer la base de données si elle n'existe pas
    init_database()

    app = QApplication(sys.argv)
    app.setApplicationName("Recharge Manager")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()