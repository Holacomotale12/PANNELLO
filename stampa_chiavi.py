import sqlite3
from datetime import datetime

def stato_chiave(activated_at, expires_at):
    now = datetime.now()
    if activated_at is None:
        return "NON USATA"
    if expires_at:
        exp = datetime.fromisoformat(expires_at)
        if now > exp:
            return "SCADUTA"
        else:
            return "USATA"
    return "USATA (LIFETIME)"

def stampa_tutte_chiavi():
    conn = sqlite3.connect("keys.db")
    c = conn.cursor()
    c.execute("SELECT code, type, activated_at, expires_at FROM keys")
    righe = c.fetchall()
    conn.close()

    for code, tipo, att, exp in righe:
        print(f"{code} ({tipo}): {stato_chiave(att, exp)}")

if __name__ == "__main__":
    stampa_tutte_chiavi()
