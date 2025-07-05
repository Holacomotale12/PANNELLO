from flask import Flask, request, redirect, render_template
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
LINK_DESTINAZIONE = "https://netfree2.cc/home?utm_source=home_page"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        codice = request.form.get("code", "").strip()
        conn = sqlite3.connect("keys.db")
        c = conn.cursor()
        c.execute("SELECT type, activated_at FROM keys WHERE code = ?", (codice,))
        row = c.fetchone()

        if row:
            tipo, attivata = row
            if attivata is None:
                now = datetime.now()
                if tipo == "1gg":
                    expires = now + timedelta(days=1)
                elif tipo == "3mesi":
                    expires = now + timedelta(days=90)
                else:
                    expires = None
                c.execute("UPDATE keys SET activated_at = ?, expires_at = ? WHERE code = ?",
                          (now.isoformat(), expires.isoformat() if expires else None, codice))
                conn.commit()
            conn.close()
            return redirect(LINK_DESTINAZIONE)
        else:
            conn.close()
            return "❌ Chiave non valida", 403
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
