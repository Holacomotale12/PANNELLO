import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt

API_BASE_URL = "http://localhost:5000/api"  # Cambia con il tuo indirizzo reale

class UserManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Utenti Connessi - Gestione")
        self.resize(900, 500)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Tabella utenti
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID Sessione", "Username", "IP", "Stato"])
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)
        self.layout.addWidget(self.table)

        # Pulsanti azioni
        btn_layout = QHBoxLayout()
        self.btn_refresh = QPushButton("Aggiorna Lista")
        self.btn_kick = QPushButton("Kick Utente")
        self.btn_ban = QPushButton("Ban Utente")

        btn_layout.addWidget(self.btn_refresh)
        btn_layout.addWidget(self.btn_kick)
        btn_layout.addWidget(self.btn_ban)
        self.layout.addLayout(btn_layout)

        # Connetti eventi
        self.btn_refresh.clicked.connect(self.load_users)
        self.btn_kick.clicked.connect(self.kick_user)
        self.btn_ban.clicked.connect(self.ban_user)

        # Carica utenti all'avvio
        self.load_users()

    def load_users(self):
        try:
            response = requests.get(f"{API_BASE_URL}/connected_users")
            response.raise_for_status()
            users = response.json()

            self.table.setRowCount(0)
            for user in users:
                riga = self.table.rowCount()
                self.table.insertRow(riga)
                self.table.setItem(riga, 0, QTableWidgetItem(str(user.get("session_id", ""))))
                self.table.setItem(riga, 1, QTableWidgetItem(user.get("username", "Anonimo")))
                self.table.setItem(riga, 2, QTableWidgetItem(user.get("ip", "")))
                self.table.setItem(riga, 3, QTableWidgetItem(user.get("status", "Attivo")))
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Impossibile caricare utenti:\n{e}")

    def get_selected_user(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Attenzione", "Seleziona un utente dalla lista!")
            return None
        # Presuppone che ID sessione sia nella colonna 0
        session_id = selected[0].text()
        username = selected[1].text()
        return {"session_id": session_id, "username": username}

    def kick_user(self):
        user = self.get_selected_user()
        if not user:
            return
        try:
            resp = requests.post(f"{API_BASE_URL}/kick_user", json={"session_id": user["session_id"]})
            resp.raise_for_status()
            QMessageBox.information(self, "Successo", f"Utente {user['username']} kickato con successo.")
            self.load_users()
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Kick fallito:\n{e}")

    def ban_user(self):
        user = self.get_selected_user()
        if not user:
            return
        try:
            resp = requests.post(f"{API_BASE_URL}/ban_user", json={"session_id": user["session_id"]})
            resp.raise_for_status()
            QMessageBox.information(self, "Successo", f"Utente {user['username']} bannato con successo.")
            self.load_users()
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Ban fallito:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserManager()
    window.show()
    sys.exit(app.exec())
