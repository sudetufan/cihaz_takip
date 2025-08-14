import sqlite3

conn = sqlite3.connect("cihazlar.db")
cursor = conn.cursor()

# Tabloları oluştur (varsa tekrar oluşturmaz)
cursor.execute('CREATE TABLE IF NOT EXISTS cihaz_tipleri (id INTEGER PRIMARY KEY AUTOINCREMENT, ad TEXT NOT NULL)')
cursor.execute('CREATE TABLE IF NOT EXISTS durumlar (id INTEGER PRIMARY KEY AUTOINCREMENT, ad TEXT NOT NULL)')
cursor.execute('CREATE TABLE IF NOT EXISTS odalar (id INTEGER PRIMARY KEY AUTOINCREMENT, ad TEXT NOT NULL)')
cursor.execute('CREATE TABLE IF NOT EXISTS personeller (id INTEGER PRIMARY KEY AUTOINCREMENT, ad TEXT NOT NULL)')

cursor.execute('''
CREATE TABLE IF NOT EXISTS cihazlar(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cihaz_tipi_id INTEGER,
    marka TEXT,
    model TEXT,
    seri_no TEXT,
    durum_id INTEGER,
    oda_id INTEGER,
    personel_id INTEGER,
    tarih TEXT,
    FOREIGN KEY (cihaz_tipi_id) REFERENCES cihaz_tipleri(id),
    FOREIGN KEY (durum_id) REFERENCES durumlar(id),
    FOREIGN KEY (oda_id) REFERENCES odalar(id),
    FOREIGN KEY (personel_id) REFERENCES personeller(id)
)
''')

# 🧹 Önce örnek verileri temizle
cursor.execute("DELETE FROM cihaz_tipleri")
cursor.execute("DELETE FROM durumlar")
cursor.execute("DELETE FROM odalar")
cursor.execute("DELETE FROM personeller")

# ✅ Verileri ekle
cursor.executemany("INSERT INTO cihaz_tipleri (ad) VALUES (?)", [
    ("Monitör",),
    ("Yazıcı",),
    ("Tarayıcı",),
    ("Kasa",),
    ("Klavye",)
])

cursor.executemany("INSERT INTO durumlar (ad) VALUES (?)", [
    ('Kullanımda',),
    ('Arızalı',),
    ('Depoda',)
])

cursor.executemany("INSERT INTO odalar (ad) VALUES (?)", [
    ('301A',),
    ('302B',),
    ('Laboratuvar',),
    ('302C',),
    ('Bilgi İşlem',),
    ('Teknik Servis',)
])

cursor.executemany("INSERT INTO personeller (ad) VALUES (?)", [
    ('Ahmet Yılmaz',),
    ('Zeynep Demir',),
    ('Mehmet Kaya',),
    ('Elif Şahin',),
    ('Mustafa Arslan',),
    ('Ayşe Korkmaz',),
    ('Emre Çelik',),
    ('Fatma Özkan',),
    ('Burak Aydın',),
    ('Selin Yıldız',),
    ('Ali Vural',)
])

conn.commit()
conn.close()
