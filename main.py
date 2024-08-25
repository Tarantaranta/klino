import sys
import os
import logging
import json
import sqlite3
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)
logging.basicConfig(filename='app.log', level=logging.DEBUG)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/styles.css')
def styles():
    return send_from_directory('.', 'styles.css')

@app.route('/script.js')
def script():
    return send_from_directory('.', 'script.js')

def veritabani_baglantisi():
    app_path = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(app_path, 'klinik.db')
    conn = sqlite3.connect(db_path)
    return conn, conn.cursor()

@app.route('/api/hastalar', methods=['POST'])
def hasta_ekle():
    data = request.json
    try:
        conn, c = veritabani_baglantisi()
        ad = data.get("ad", "")
        soyad = data.get("soyad", "")
        yas = data.get("yas", "")
        tc = data.get("tc", "")
        meslek = data.get("meslek", "")
        evli = 1 if data.get("evli", False) else 0
        cocuk_sayisi = data.get("cocuk_sayisi", "")
        cinsiyet = data.get("cinsiyet", "")
        telefon = data.get("telefon", "")
        email = data.get("email", "")
        adres = data.get("adres", "")
        ana_sikayet = data.get("ana_sikayet", "")

        c.execute('''INSERT INTO hastalar (ad, soyad, yas, tc, meslek, evli, cocuk_sayisi, cinsiyet, telefon, email, adres, ana_sikayet)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (ad, soyad, yas, tc, meslek, evli, cocuk_sayisi, cinsiyet, telefon, email, adres, ana_sikayet))
        conn.commit()
        hasta_id = c.lastrowid
        conn.close()

        return jsonify(message="Hasta başarıyla eklendi", hasta_id=hasta_id), 201
    except Exception as e:
        logging.error(f'Hasta eklenirken hata oluştu: {e}')
        return jsonify({"error": "Veritabanı hatası"}), 500

@app.route('/api/hastalar', methods=['GET'])
def hasta_listesini_getir():
    arama_kriteri = request.args.get('q', '').lower()
    conn, c = veritabani_baglantisi()
    query = """
        SELECT h.id, h.ad, h.soyad, h.yas, h.tc, h.meslek, 
               CASE WHEN h.evli = 1 THEN 'Evet' ELSE 'Hayır' END AS evli, 
               h.cocuk_sayisi, h.cinsiyet, h.telefon, h.email, h.adres, h.ana_sikayet, 
               (SELECT COUNT(*) FROM seanslar s WHERE s.hasta_id = h.id) AS toplam_seans
        FROM hastalar h
    """
    if arama_kriteri:
        query += " WHERE LOWER(h.ad) LIKE ? OR LOWER(h.soyad) LIKE ? OR LOWER(h.ana_sikayet) LIKE ?"
        c.execute(query, ('%' + arama_kriteri + '%', '%' + arama_kriteri + '%', '%' + arama_kriteri + '%'))
    else:
        c.execute(query)

    hastalar = c.fetchall()
    conn.close()

    hastalar_listesi = []
    for hasta in hastalar:
        hasta_dict = {
            "id": hasta[0],
            "ad": hasta[1],
            "soyad": hasta[2],
            "yas": hasta[3],
            "tc": hasta[4],
            "meslek": hasta[5],
            "evli": hasta[6],
            "cocuk_sayisi": hasta[7],
            "cinsiyet": hasta[8],
            "telefon": hasta[9],
            "email": hasta[10],
            "adres": hasta[11],
            "ana_sikayet": hasta[12],
            "toplam_seans": hasta[13]
        }
        hastalar_listesi.append(hasta_dict)

    return jsonify(hastalar_listesi), 200

@app.route('/api/seanslar', methods=['POST'])
def seans_ekle():
    data = request.get_json()
    try:
        hasta_id = data['hasta_id']
        tarih = data['tarih']
        saat = data['saat']
        islem = data['islem']
        # Add logic to save the session information to the database
        return jsonify({"message": "Seans başarıyla eklendi"})
    except KeyError as e:
        return jsonify({"error": f"Missing data: {str(e)}"}), 400

@app.route('/api/diyetler', methods=['POST'])
def diyet_ekle():
    data = request.get_json()
    try:
        hasta_id = data['hasta_id']
        diyet = data['diyet']
        # Add logic to save the diet information to the database
        return jsonify({"message": "Diyet başarıyla eklendi"})
    except KeyError as e:
        return jsonify({"error": f"Missing data: {str(e)}"}), 400


@app.route('/api/sendromlar', methods=['GET'])
def sendromlari_listele():
    try:
        with open('sendrom_aciklamalari.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            sendromlar = sorted(data.keys())
    except (FileNotFoundError, json.JSONDecodeError):
        sendromlar = []

    return jsonify(sendromlar), 200

def create_tables():
    conn, c = veritabani_baglantisi()
    c.execute('''CREATE TABLE IF NOT EXISTS hastalar (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ad TEXT,
                    soyad TEXT,
                    yas INTEGER,
                    tc TEXT,
                    meslek TEXT,
                    evli INTEGER,
                    cocuk_sayisi INTEGER,
                    cinsiyet TEXT,
                    telefon TEXT,
                    email TEXT,
                    adres TEXT,
                    ana_sikayet TEXT,
                    ekstra_puan TEXT,
                    genel_bulgular TEXT
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS seanslar (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hasta_id INTEGER,
                    tarih TEXT,
                    saat TEXT,
                    seans_no INTEGER,
                    islem TEXT,
                    notlar TEXT,
                    FOREIGN KEY (hasta_id) REFERENCES hastalar(id)
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS diyetler (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hasta_id INTEGER,
                    tarih TEXT,
                    diyet TEXT,
                    FOREIGN KEY (hasta_id) REFERENCES hastalar(id)
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS teshisler (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hasta_id INTEGER,
                    tarih TEXT,
                    sonuc TEXT,
                    puanlar TEXT,
                    detayli_sonuc TEXT,
                    txt_path TEXT,
                    FOREIGN KEY (hasta_id) REFERENCES hastalar(id)
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS teshis_aciklamalari (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sendrom TEXT UNIQUE,
                    aciklama TEXT
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS anket_sonuclari (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hasta_id INTEGER,
                    tarih TEXT,
                    anket_sonuc TEXT,
                    FOREIGN KEY (hasta_id) REFERENCES hastalar(id)
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS diagnosis_texts (
                    patient_id TEXT,
                    diagnosis_text TEXT
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS html_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hasta_id INTEGER,
                    html_content TEXT,
                    FOREIGN KEY (hasta_id) REFERENCES hastalar(id)
                )''')

    conn.commit()
    conn.close()

@app.route('/api/hasta-dosyasi/<int:hasta_id>', methods=['GET'])
def hasta_dosyasi(hasta_id):
    conn, c = veritabani_baglantisi()

    # Hasta bilgileri
    c.execute("SELECT * FROM hastalar WHERE id = ?", (hasta_id,))
    hasta = c.fetchone()

    # Notlar ve Düşünceler
    c.execute("SELECT notlar FROM hasta_notlari WHERE hasta_id = ?", (hasta_id,))
    notlar = c.fetchone()

    # Seans Bilgileri
    c.execute("SELECT tarih, saat, islem FROM seanslar WHERE hasta_id = ? AND tarih < date('now')", (hasta_id,))
    gecmis_seanslar = c.fetchall()
    c.execute("SELECT tarih, saat, islem FROM seanslar WHERE hasta_id = ? AND tarih >= date('now')", (hasta_id,))
    gelecek_seanslar = c.fetchall()

    # Diyet Bilgileri
    c.execute("SELECT tarih, diyet FROM diyetler WHERE hasta_id = ?", (hasta_id,))
    diyetler = c.fetchall()

    # Anket Bilgileri
    c.execute("SELECT tarih, anket_sonuc FROM anket_sonuclari WHERE hasta_id = ?", (hasta_id,))
    anketler = c.fetchall()

    conn.close()

    return jsonify({
        'ad': hasta[1],
        'soyad': hasta[2],
        'yas': hasta[3],
        'tc': hasta[4],
        'meslek': hasta[5],
        'evli': 'Evet' if hasta[6] else 'Hayır',
        'cocuk_sayisi': hasta[7],
        'cinsiyet': hasta[8],
        'telefon': hasta[9],
        'email': hasta[10],
        'adres': hasta[11],
        'ana_sikayet': hasta[12],
        'notlar_dusunceler': notlar[0] if notlar else '',
        'gecmis_seanslar': [{'tarih': seans[0], 'saat': seans[1], 'islem': seans[2]} for seans in gecmis_seanslar],
        'gelecek_seanslar': [{'tarih': seans[0], 'saat': seans[1], 'islem': seans[2]} for seans in gelecek_seanslar],
        'diyetler': [diyet[1] for diyet in diyetler],
        'anketler': [anket[1] for anket in anketler]
    })


@app.route('/api/hasta-dosyasi/<int:hasta_id>', methods=['POST'])
def update_hasta_dosyasi(hasta_id):
    data = request.get_json()
    conn, c = veritabani_baglantisi()

    c.execute("""
        UPDATE hastalar SET
            ad = ?, soyad = ?, yas = ?, tc = ?, meslek = ?,
            evli = ?, cocuk_sayisi = ?, cinsiyet = ?, telefon = ?, email = ?, adres = ?, ana_sikayet = ?
        WHERE id = ?
    """, (
        data['ad'], data['soyad'], data['yas'], data['tc'], data['meslek'],
        1 if data['evli'] else 0, data['cocuk_sayisi'], data['cinsiyet'],
        data['telefon'], data['email'], data['adres'], data['ana_sikayet'], hasta_id
    ))

    c.execute("""
        INSERT OR REPLACE INTO hasta_notlari (hasta_id, notlar) VALUES (?, ?)
    """, (hasta_id, data['notlar_dusunceler']))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Hasta bilgileri güncellendi'})

@app.route('/api/hasta-dosyasi/indir/<int:hasta_id>', methods=['GET'])
def indir_hasta_dosyasi(hasta_id):
    conn, c = veritabani_baglantisi()
    c.execute("SELECT * FROM hastalar WHERE id = ?", (hasta_id,))
    hasta = c.fetchone()

    if not hasta:
        return jsonify({"error": "Hasta bulunamadı"}), 404

    c.execute("SELECT tarih, saat, islem FROM seanslar WHERE hasta_id = ?", (hasta_id,))
    seanslar = c.fetchall()

    c.execute("SELECT tarih, diyet FROM diyetler WHERE hasta_id = ?", (hasta_id,))
    diyetler = c.fetchall()

    conn.close()

    dosya_icerigi = f"""
    Hasta Bilgileri:
    Ad: {hasta[1]}
    Soyad: {hasta[2]}
    Yaş: {hasta[3]}
    TC: {hasta[4]}
    Meslek: {hasta[5]}
    Evli: {'Evet' if hasta[6] else 'Hayır'}
    Çocuk Sayısı: {hasta[7]}
    Cinsiyet: {hasta[8]}
    Telefon: {hasta[9]}
    Email: {hasta[10]}
    Adres: {hasta[11]}
    Ana Şikayet: {hasta[12]}

    Seanslar:
    """
    for seans in seanslar:
        dosya_icerigi += f"\nTarih: {seans[0]} Saat: {seans[1]} İşlem: {seans[2]}"

    dosya_icerigi += "\n\nDiyetler:\n"
    for diyet in diyetler:
        dosya_icerigi += f"\nTarih: {diyet[0]} Diyet: {diyet[1]}"

    return dosya_icerigi, 200, {
        'Content-Type': 'text/plain; charset=utf-8',
        'Content-Disposition': f'attachment;filename=hasta_{hasta_id}.txt',
    }

if __name__ == '__main__':
    try:
        create_tables()
        app.run(debug=True, port=52140)
    except Exception as e:
        logging.critical("Fatal Error: %s", e)
        raise
