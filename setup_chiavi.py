import sqlite3
import random
import string
from datetime import datetime, timedelta

def genera_codice(prefix):
    suffisso = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{prefix}-{suffisso}"

def crea_db_e_chiavi():
    conn = sqlite3.connect("keys.db")
    c = conn.cursor()

    # Ricrea tabella keys
    c.execute("DROP TABLE IF EXISTS keys")
    c.execute("""
    CREATE TABLE keys (
        code TEXT PRIMARY KEY,
        type TEXT,
        activated_at TEXT,
        expires_at TEXT
    )
    """)

    adesso = datetime.now()

    # 30 chiavi 1 giorno
    for _ in range(30):
        code = genera_codice("1G")
        expires = adesso + timedelta(days=1)
        c.execute("INSERT INTO keys VALUES (?, ?, ?, ?)", (code, "1g", None, expires.isoformat()))

    # 30 chiavi 3 mesi
    for _ in range(30):
        code = genera_codice("3M")
        expires = adesso + timedelta(days=90)
        c.execute("INSERT INTO keys VALUES (?, ?, ?, ?)", (code, "3m", None, expires.isoformat()))

    # 40 chiavi lifetime
    for _ in range(40):
        code = genera_codice("LIFE")
        c.execute("INSERT INTO keys VALUES (?, ?, ?, ?)", (code, "life", None, None))

    conn.commit()
    conn.close()
    print("Database creato e 100 chiavi generate!")

if __name__ == "__main__":
    crea_db_e_chiavi()
