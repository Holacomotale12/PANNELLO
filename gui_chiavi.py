import sys
import sqlite3
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QLabel
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor

class KeyManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestione Chiavi PRO")
        self.resize(950, 550)

        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #f0f0f0;
                font-family: 'Segoe UI';
                font-size: 12pt;
            }
            QLineEdit, QPushButton {
                padding: 6px;
                font-size: 11pt;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #2980b9;
                color: white;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: white;
                font-weight: bold;
                padding: 4px;
            }
        """)

        layout = QVBoxLayout(self)

        # Layout filtro + bottoni
        filter_layout = QHBoxLayout()
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("🔍 Cerca chiave o tipo...")
        self.filter_input.textChanged.connect(self.carica_chiavi)
        filter_layout.addWidget(QLabel("Filtro:"))
        filter_layout.addWidget(self.filter_input)

        # Bottone aggiorna manualmente
        self.btn_aggiorna = QPushButton("🔄 Aggiorna")
        self.btn_aggiorna.clicked.connect(self.carica_chiavi)
        filter_layout.addWidget(self.btn_aggiorna)

        # Bottone copia
        self.btn_copia = QPushButton("📋 Copia Chiave Selezionata")
        self.btn_copia.clicked.connect(self.copia_chiave)
        filter_layout.addWidget(self.btn_copia)

        layout.addLayout(filter_layout)

        # Tabella
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Chiave", "Tipo", "Stato", "Scadenza"])
        self.table.setSortingEnabled(True)
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)
        layout.addWidget(self.table)

        # Stato
        self.status = QLabel("")
        layout.addWidget(self.status)

        # Auto-refresh ogni 30 secondi
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.carica_chiavi)
        self.timer.start(30000)

        self.carica_chiavi()

    def carica_chiavi(self):
        filtro = self.filter_input.text().lower()
        conn = sqlite3.connect("keys.db")
        c = conn.cursor()
        c.execute("SELECT code, type, activated_at, expires_at FROM keys")
        dati = c.fetchall()
        conn.close()

        self.table.setRowCount(0)
        now = datetime.now()

        for codice, tipo, att, exp in dati:
            stato = "NON USATA"
            colore = QColor(39, 174, 96)  # verde

            if att:
                if exp:
                    exp_dt = datetime.fromisoformat(exp)
                    if now > exp_dt:
                        stato = "SCADUTA"
                    else:
                        stato = "USATA"
                else:
                    stato = "USATA (LIFETIME)"
                colore = QColor(231, 76, 60)  # rosso

            exp_str = exp if exp else "N/A"
            riga_testo = f"{codice} {tipo} {stato}".lower()
            if filtro not in riga_testo:
                continue

            riga = self.table.rowCount()
            self.table.insertRow(riga)

            for i, val in enumerate([codice, tipo.upper(), stato, exp_str]):
                item = QTableWidgetItem(val)
                item.setBackground(colore)
                item.setForeground(QColor("white"))
                self.table.setItem(riga, i, item)

        self.table.resizeColumnsToContents()
        self.status.setText(f"🔑 {self.table.rowCount()} chiavi visualizzate")

    def copia_chiave(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Attenzione", "Seleziona una riga!")
            return
        codice = selected[0].text()
        QApplication.clipboard().setText(codice)
        QMessageBox.information(self, "Copiato", f"Chiave '{codice}' copiata!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = KeyManager()
    win.show()
    sys.exit(app.exec())
