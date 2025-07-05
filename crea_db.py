import sqlite3
from random import choice
import string

conn = sqlite3.connect("keys.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS keys (
    code TEXT PRIMARY KEY,
    type TEXT,
    activated_at TEXT,
    expires_at TEXT
)
""")

def genera_codice():
    return ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(10))

tipi = ["1gg", "3mesi", "lifetime"]

for _ in range(100):
    codice = genera_codice()
    tipo = choice(tipi)
    c.execute("INSERT OR IGNORE INTO keys (code, type, activated_at, expires_at) VALUES (?, ?, ?, ?)",
              (codice, tipo, None, None))

conn.commit()
conn.close()
print("✔️ 100 chiavi generate in keys.db")
