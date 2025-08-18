from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash


app = Flask(__name__)
db_name = "cihazlar.db"

app.secret_key = "supersecretkey"
    
def get_db_connection():
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/cihazlar")
@login_required
def cihaz_listesi():
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

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO cihazlar (cihaz_tipi_id, marka, model, seri_no, durum_id, oda_id, personel_id, tarih)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (cihaz_tipi, marka, model, seri_no, durum, oda, personel, tarih)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('cihaz_listesi'))

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


login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id, username, password, rol):
        self.id = id
        self.username = username
        self.password_hash = password
        self.rol = rol

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    conn=get_db_connection()
    user=conn.execute("select * from kullanicilar where id = ?", (user_id)).fetchone()
    conn.close()
    if user:
        return User(user["id"], user["username"], user["password"], user["rol"])
    return None


@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn= get_db_connection()
        user = conn.execute("select * from kullanicilar where username = ?", (username,)).fetchone()
        conn.close()
        
        if user:
            user_obj = User(user["id"], user["username"],user["password"], user["rol"])
            if user_obj.check_password(password):
                login_user(user_obj)
                flash("Başarıyla giriş yapıldı", "success")
                return redirect(url_for("cihaz_listesi"))
            
        flash("Hatalı kullanıcı adı veya parola", "danger")
    return render_template("login.html")    
            
        


@app.route("/protected")
@login_required
def protected():
    return f"Merhaba {current_user.name}! Bu sayfa sadece giriş yapan kullanıcılar içindir."

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Başarıyla çıkış yapıldı", "info")
    return redirect(url_for("login"))

@app.route("/cihaz_sil/<int:cihaz_id>", methods={"POST"})
@login_required
def cihaz_sil(cihaz_id):
    conn = get_db_connection()
    conn.execute("delete from cihazlar where id = ?", (cihaz_id,))
    conn.commit()
    conn.close()
    flash("Cihaz başarıyla silindi", "success")
    return redirect(url_for("cihaz_listesi"))

if __name__ == "__main__":
    app.run(debug=True)





