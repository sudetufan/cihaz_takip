from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
db_name = "cihazlar.db"

def get_db_connection():
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    cihazlar = conn.execute('''
        SELECT c.id, ct.ad AS cihaz_tipi, c.marka, c.model, c.seri_no,
               d.ad AS durum, o.ad AS oda, p.ad AS personel_adi, c.tarih
        FROM cihazlar c
        JOIN cihaz_tipleri ct ON c.cihaz_tipi_id = ct.id
        JOIN durumlar d ON c.durum_id = d.id
        JOIN odalar o ON c.oda_id = o.id
        JOIN personeller p ON c.personel_id = p.id
    ''').fetchall()
    conn.close()
    return render_template("index.html", cihazlar=cihazlar)

@app.route("/cihaz_ekle", methods=('GET', 'POST'))
def cihaz_ekle():
    if request.method == "POST":
        cihaz_tipi = request.form["cihaz_tipi"]
        marka = request.form["marka"]
        model = request.form["model"]
        seri_no = request.form["seri_no"]
        durum = request.form["durum"]
        oda = request.form["oda"]
        personel = request.form["personel"]
        tarih = request.form["tarih"]

        # POST kısmında bağlantıyı aç
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO cihazlar (cihaz_tipi_id, marka, model, seri_no, durum_id, oda_id, personel_id, tarih)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (cihaz_tipi, marka, model, seri_no, durum, oda, personel, tarih)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    # GET kısmı için ayrı bağlantı aç (POST'un dışında!)
    conn = get_db_connection()
    cihaz_tipleri = conn.execute("SELECT * FROM cihaz_tipleri").fetchall()
    durumlar = conn.execute("SELECT * FROM durumlar").fetchall()
    odalar = conn.execute("SELECT * FROM odalar").fetchall()
    personeller = conn.execute("SELECT * FROM personeller").fetchall()
    conn.close()

    return render_template(
        'cihaz_ekle.html',
        cihaz_tipleri=cihaz_tipleri,
        durumlar=durumlar,
        odalar=odalar,
        personeller=personeller
    )

if __name__ == "__main__":
    app.run(debug=True)





