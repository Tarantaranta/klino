import logging
import json
import pytz
import os
import sqlite3
from PyQt5.QtGui import QFont

from datetime import datetime
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTextEdit, QLabel, QScrollArea,
    QPushButton, QHBoxLayout, QFormLayout, QLineEdit, QComboBox, QTabWidget, QMessageBox, QCheckBox, QCalendarWidget, QListWidget, QDialog, QListWidgetItem, QTableWidget, QTableWidgetItem
)

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl, pyqtSlot, QObject, Qt, QDate, QSize
from PyQt5.QtGui import QTextCharFormat, QColor, QFont, QIcon
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtGui import QPainter, QTextDocument
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt
from full_screen_editor import FullScreenEditor
from seans_oncesi_anket import SeansOncesiAnketDialog
from acupuncture_points import populate_acupuncture_points
from hasta_dosyasi import HastaDosyasiPenceresi

class DescriptionDialog(QDialog):
    def __init__(self, parent=None, sendrom=None):
        super().__init__(parent)
        self.sendrom = sendrom
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"Sendrom Düzenle: {self.sendrom}")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout(self)

        self.description_entry = QTextEdit()
        layout.addWidget(self.description_entry)

        self.save_button = QPushButton("Kaydet")
        self.save_button.clicked.connect(self.save_description)
        layout.addWidget(self.save_button)

        self.load_description()

    def load_description(self):
        try:
            with open('sendrom_aciklamalari.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.description_entry.setPlainText(data.get(self.sendrom, ""))
        except (FileNotFoundError, json.JSONDecodeError):
            self.description_entry.setPlainText("")

    def save_description(self):
        description = self.description_entry.toPlainText()
        try:
            with open('sendrom_aciklamalari.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        data[self.sendrom] = description

        with open('sendrom_aciklamalari.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        self.accept()

class KlinikUygulamasi(QMainWindow):
    def __init__(self):
        super().__init__()
        try:
            self.veritabani_baglantisi()
            self.current_patient_id = None
            self.initUI()
            self.hasta_dosyasi_penceresi = None  # Önce None olarak başlatılıyor
            logging.info("KlinikUygulamasi initialized successfully")
        except Exception as e:
            logging.error("Initialization Error: %s", e)
            raise

    def initUI(self):
        self.setWindowTitle("Çin Tıbbı Kliniği Hasta Takip Sistemi")
        self.setGeometry(100, 100, 1200, 800)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout(self.centralWidget)

        self.tabWidget = QTabWidget()
        self.layout.addWidget(self.tabWidget)

        self.tab_hasta_ekle = QWidget()
        self.tab_seans_ekle = QWidget()
        self.tab_diyet_ekle = QWidget()
        self.tab_takvim = QWidget()
        self.tab_sozluk = QWidget()
        self.tab_hasta_havuzu = QWidget() 
        

        self.tabWidget.addTab(self.tab_hasta_ekle, "Hasta Ekle")
        self.tabWidget.addTab(self.tab_seans_ekle, "Seans Ekle")
        self.tabWidget.addTab(self.tab_diyet_ekle, "Diyet Ekle")
        self.tabWidget.addTab(self.tab_takvim, "Genel Takvim")
        self.tabWidget.addTab(self.tab_sozluk, "Sözlük")
        self.tabWidget.addTab(self.tab_hasta_havuzu, "Hasta Havuzu")

        self.hasta_ekle_tab()
        self.seans_ekle_tab()
        self.diyet_ekle_tab()
        self.genel_takvim_tab()
        self.sozluk_tab()
        self.hasta_havuzu_tab() 

    def hasta_havuzu_tab(self):
        layout = QVBoxLayout()

        self.arama_girdisi = QLineEdit()
        self.arama_girdisi.setPlaceholderText("Hasta Ara")
        layout.addWidget(self.arama_girdisi)

        self.hasta_listesi = QTableWidget()
        self.hasta_listesi.setColumnCount(6)
        self.hasta_listesi.setHorizontalHeaderLabels([
        "ID", "Ad", "Soyad", "Yaş", "TC", "Meslek", "Evli", "Çocuk Sayısı", 
        "Cinsiyet", "Telefon", "Email", "Adres", "Ana Şikayet", "Toplam Seans"
    ])
        self.hasta_listesi.cellClicked.connect(self.detayli_hasta_bilgileri_goster)  # Tıklanabilir hale getirme
        layout.addWidget(self.hasta_listesi)

        self.arama_girdisi.textChanged.connect(self.hasta_listesini_doldur)

        self.tab_hasta_havuzu.setLayout(layout)
        self.hasta_listesini_doldur()


    def hasta_listesini_doldur(self):
        arama_kriteri = self.arama_girdisi.text().lower()
        query = """
            SELECT h.id, h.ad, h.soyad, h.yas, h.tc, h.meslek, 
                   CASE WHEN h.evli = 1 THEN 'Evet' ELSE 'Hayır' END AS evli, 
                   h.cocuk_sayisi, h.cinsiyet, h.telefon, h.email, h.adres, h.ana_sikayet, 
                   (SELECT COUNT(*) FROM seanslar s WHERE s.hasta_id = h.id) AS toplam_seans
            FROM hastalar h
        """
        if arama_kriteri:
            query += " WHERE LOWER(h.ad) LIKE ? OR LOWER(h.soyad) LIKE ? OR LOWER(h.ana_sikayet) LIKE ?"
            self.c.execute(query, ('%' + arama_kriteri + '%', '%' + arama_kriteri + '%', '%' + arama_kriteri + '%'))
        else:
            self.c.execute(query)

        hastalar = self.c.fetchall()

        self.hasta_listesi.setRowCount(len(hastalar))
        for row_num, hasta in enumerate(hastalar):
            for col_num, data in enumerate(hasta):
                self.hasta_listesi.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def detayli_hasta_bilgileri_goster(self, row, column):
        hasta_id = self.hasta_listesi.item(row, 0).text()
        self.hasta_dosyasi_ac(hasta_id)

    def hasta_ekle_tab(self):
        layout = QVBoxLayout()

        form_layout = QFormLayout()

        fields = ["Ad", "Soyad", "Yaş", "TC", "Meslek", "Evli", "Çocuk Sayısı", "Cinsiyet", "Telefon", "Email", "Adres", "Ana Şikayet"]
        self.entries = {}
        for field in fields:
            label = QLabel(field)
            entry = QLineEdit()
            form_layout.addRow(label, entry)
            self.entries[field] = entry

        self.evli_check = QCheckBox()
        form_layout.addRow(QLabel("Evli"), self.evli_check)

        self.cinsiyet_combobox = QComboBox()
        self.cinsiyet_combobox.addItems(["Erkek", "Kadın"])
        form_layout.addRow(QLabel("Cinsiyet"), self.cinsiyet_combobox)

        layout.addLayout(form_layout)

        self.kaydet_button = QPushButton('Kaydet')
        self.kaydet_button.clicked.connect(self.hasta_ekle)
        layout.addWidget(self.kaydet_button)

        # Adding Hasta Ara functionality within the Hasta Ekle tab
        search_layout = QVBoxLayout()

        self.hasta_secimi_combobox_ara = QComboBox()
        self.guncelle_hasta_secimi_combobox_ara()
        search_layout.addWidget(self.hasta_secimi_combobox_ara)

        self.arama_hasta = QLineEdit()
        self.arama_hasta.setPlaceholderText("Hasta Ara")
        self.arama_hasta.textChanged.connect(lambda: self.guncelle_hasta_secimi_combobox_ara(self.arama_hasta.text()))
        search_layout.addWidget(self.arama_hasta)

        self.hasta_dosyasi_ac_button = QPushButton("Hasta Dosyasını Aç")
        self.hasta_dosyasi_ac_button.clicked.connect(self.hasta_dosyasi_ac_button_click)
        search_layout.addWidget(self.hasta_dosyasi_ac_button)

        layout.addLayout(search_layout)

        self.tab_hasta_ekle.setLayout(layout)

    def hasta_dosyasi_ac_button_click(self):
        current_index = self.hasta_secimi_combobox_ara.currentIndex()
        if current_index >= 0:
            hasta_id = self.hasta_secimi_combobox_ara.itemData(current_index)
            logging.info(f"Button clicked to open patient file for hasta_id: {hasta_id}")
            self.hasta_dosyasi_ac(hasta_id)

        
    def hasta_ekle(self):
        ad = self.entries["Ad"].text()
        soyad = self.entries["Soyad"].text()
        yas = self.entries["Yaş"].text()
        tc = self.entries["TC"].text()
        meslek = self.entries["Meslek"].text()
        evli = 1 if self.evli_check.isChecked() else 0
        cocuk_sayisi = self.entries["Çocuk Sayısı"].text()
        cinsiyet = self.cinsiyet_combobox.currentText()
        telefon = self.entries["Telefon"].text()
        email = self.entries["Email"].text()
        adres = self.entries["Adres"].text()
        ana_sikayet = self.entries["Ana Şikayet"].text()

        self.c.execute('''INSERT INTO hastalar (ad, soyad, yas, tc, meslek, evli, cocuk_sayisi, cinsiyet, telefon, email, adres, ana_sikayet)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (ad, soyad, yas, tc, meslek, evli, cocuk_sayisi, cinsiyet, telefon, email, adres, ana_sikayet))
        self.conn.commit()

        hasta_id = self.c.lastrowid  # Otomatik oluşturulan ID'yi alıyoruz
        QMessageBox.information(self, "Başarılı", f"Hasta başarıyla eklendi! Hasta ID: {hasta_id}")

        self.guncelle_hasta_secimi_combobox()
        self.guncelle_hasta_secimi_combobox_diyet()

    def guncelle_hasta_secimi_combobox_ara(self, arama_kriteri=""):
        self.hasta_secimi_combobox_ara.clear()

        if arama_kriteri:
            arama_kriteri = arama_kriteri.strip().lower()
            if arama_kriteri.isdigit():
                self.c.execute("SELECT id, ad, soyad FROM hastalar WHERE id LIKE ?", ('%' + arama_kriteri + '%',))
            else:
                self.c.execute("SELECT id, ad, soyad FROM hastalar WHERE LOWER(ad) LIKE ? OR LOWER(soyad) LIKE ?", ('%' + arama_kriteri + '%', '%' + arama_kriteri + '%'))
        else:
            self.c.execute("SELECT id, ad, soyad FROM hastalar")

        hastalar = self.c.fetchall()
        for hasta in hastalar:
            self.hasta_secimi_combobox_ara.addItem(f"{hasta[1]} {hasta[2]} (ID: {hasta[0]})", hasta[0])

    def veritabani_baglantisi(self):
        try:
            app_path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(app_path, 'klinik.db')
            self.conn = sqlite3.connect(db_path)
            self.c = self.conn.cursor()

            self.create_tables()

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Veritabanı Hatası", f"Veritabanı bağlantısı sırasında bir hata oluştu: {e}")
        except Exception as e:
            logging.error("Database Connection Error: %s", e)
            raise

    def create_tables(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS hastalar (
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

        self.c.execute('''CREATE TABLE IF NOT EXISTS seanslar (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            hasta_id INTEGER,
                            tarih TEXT,
                            saat TEXT,
                            seans_no INTEGER,
                            islem TEXT,
                            notlar TEXT,
                            FOREIGN KEY (hasta_id) REFERENCES hastalar(id)
                        )''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS diyetler (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            hasta_id INTEGER,
                            tarih TEXT,
                            diyet TEXT,
                            FOREIGN KEY (hasta_id) REFERENCES hastalar(id)
                        )''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS teshisler (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            hasta_id INTEGER,
                            tarih TEXT,
                            sonuc TEXT,
                            puanlar TEXT,
                            detayli_sonuc TEXT,
                            txt_path TEXT,
                            FOREIGN KEY (hasta_id) REFERENCES hastalar(id)
                        )''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS teshis_aciklamalari (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            sendrom TEXT UNIQUE,
                            aciklama TEXT
                        )''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS anket_sonuclari (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            hasta_id INTEGER,
                            tarih TEXT,
                            anket_sonuc TEXT,
                            FOREIGN KEY (hasta_id) REFERENCES hastalar(id)
                        )''')

        self.c.execute('''CREATE TABLE IF NOT EXISTS diagnosis_texts (
                            patient_id TEXT,
                            diagnosis_text TEXT
                        )''')

        # Yeni tablo oluşturma kodu
        self.c.execute('''CREATE TABLE IF NOT EXISTS html_files (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            hasta_id INTEGER,
                            html_content TEXT,
                            FOREIGN KEY (hasta_id) REFERENCES hastalar(id)
                        )''')

        self.conn.commit()




    def guncelle_hasta_secimi_combobox(self, arama_kriteri=""):
        self.hasta_secimi_combobox.clear()

        if arama_kriteri:
            arama_kriteri = arama_kriteri.strip().lower()
            if arama_kriteri.isdigit():
                self.c.execute("SELECT id, ad, soyad FROM hastalar WHERE id LIKE ?", ('%' + arama_kriteri + '%',))
            else:
                self.c.execute("SELECT id, ad, soyad FROM hastalar WHERE LOWER(ad) LIKE ? OR LOWER(soyad) LIKE ?", ('%' + arama_kriteri + '%', '%' + arama_kriteri + '%'))
        else:
            self.c.execute("SELECT id, ad, soyad FROM hastalar")

        hastalar = self.c.fetchall()
        for hasta in hastalar:
            self.hasta_secimi_combobox.addItem(f"{hasta[1]} {hasta[2]} (ID: {hasta[0]})", hasta[0])

    def sozluk_tab(self):
        layout = QVBoxLayout()

        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText("Sendrom Ara")
        self.search_button = QPushButton("Ara")
        self.search_button.clicked.connect(self.sendrom_ara)

        layout.addWidget(self.search_entry)
        layout.addWidget(self.search_button)

        self.result_list = QListWidget()
        self.result_list.itemDoubleClicked.connect(self.sendrom_duzenle)
        layout.addWidget(self.result_list)

        self.tab_sozluk.setLayout(layout)
        self.sendromlari_listele()

    def sendromlari_listele(self):
        self.result_list.clear()
        try:
            with open('sendrom_aciklamalari.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                for sendrom in sorted(data.keys()):
                    item = QListWidgetItem(sendrom)
                    item.setData(Qt.UserRole, sendrom)
                    self.result_list.addItem(item)
        except (FileNotFoundError, json.JSONDecodeError):
            pass


    def get_acupuncture_points(self, meridyen):
        points = []
        if meridyen == "Lung (LU)":
            points = [
                "LU1 (Orta Saray)", "LU2 (Bulut Kapısı)", "LU3 (Göksel Depo)", "LU4 (Göksel Bina)",
                "LU5 (Büküm Havuzu)", "LU6 (En Yüce Çukur)", "LU7 (Kırık Dizi)", "LU8 (Kan Kanalı)",
                "LU9 (Büyük Uçurum)", "LU10 (Balık Karnı)", "LU11 (Azimli Tükenmez)"
            ]
        elif meridyen == "Large Intestine (LI)":
            points = [
                "LI1 (Metalin Büyüklüğü)", "LI2 (İkinci Aralık)", "LI3 (Üçüncü Aralık)", "LI4 (Büyük Birlik)",
                "LI5 (Yang Deresi)", "LI6 (Yan Ağız)", "LI7 (Sıcaklık Alanı)", "LI8 (Üst Akış)",
                "LI9 (Düşük Akış)", "LI10 (Kol Üç Mili)", "LI11 (Eğik Havuz)", "LI12 (Kol Kemeri)",
                "LI13 (Kol Üst Noktası)", "LI14 (Kolun Yüce Noktası)", "LI15 (Omuz Kemeri)",
                "LI16 (Büyük Kemik)", "LI17 (Gırtlak Yardımı)", "LI18 (Dış Kuyu)", "LI19 (Yan Kuyu)",
                "LI20 (Koku Kapısı)"
            ]
        elif meridyen == "Stomach (ST)":
            points = [
                "ST1 (Tepkinin Uçları)", "ST2 (Dört Beyazlık)", "ST3 (Büyük Kemik)", "ST4 (Toplu Üst Nokta)",
                "ST5 (Büyük Karşılık)", "ST6 (Çene Arabası)", "ST7 (Alt Çene Birliği)", "ST8 (Bağlantı Köşesi)",
                "ST9 (Karşı Tepki)", "ST10 (Su Mağarası)", "ST11 (Gaz Bağlantısı)", "ST12 (Boşluk Kapısı)",
                "ST13 (Boğaz Açıklığı)", "ST14 (Göğüs Temizliği)", "ST15 (Göğüs Kapısı)", "ST16 (Göğüs Tatlılığı)",
                "ST17 (Göğüs Orta Nokta)", "ST18 (Süt Kapağı)", "ST19 (Çözülme)", "ST20 (Destek Noktası)",
                "ST21 (İç Avlu)", "ST22 (Büyük Karın)", "ST23 (Karın Üçüncü Noktası)", "ST24 (Karın Merkezi)",
                "ST25 (Göbek Bölgesi)", "ST26 (Dış Saha)", "ST27 (Büyük İç)", "ST28 (Sıvı Kapısı)",
                "ST29 (Dönme Noktası)", "ST30 (Qi'nin Kavşağı)", "ST31 (Üst Köşe)", "ST32 (İkinci Yan)",
                "ST33 (Orta Yan)", "ST34 (Işığın Yolu)", "ST35 (Yan Diz)", "ST36 (Ayağın Üç Noktası)",
                "ST37 (Üçüncü Bölge)", "ST38 (Orta Kanal)", "ST39 (Alt Bölge)", "ST40 (Hoşluk Yolu)",
                "ST41 (Karşı Tepki)", "ST42 (Chongyang)", "ST43 (Derin Kuyu)", "ST44 (İç Avlu)",
                "ST45 (Sertlik Alanı)"
            ]
        elif meridyen == "Spleen (SP)":
            points = [
                "SP1 (Gizli Beyazlık)", "SP2 (Büyük Metin)", "SP3 (En Yüce Beyaz)", "SP4 (Aynı Konum)",
                "SP5 (Ağır Şehir)", "SP6 (Üç Gizemli)", "SP7 (Kaçan Taban)", "SP8 (Yeraltı Kaynağı)",
                "SP9 (Su Bahçesi)", "SP10 (Deniz Büyük Konak)", "SP11 (Kuşak Açıklığı)", "SP12 (Ağır Sıvı)",
                "SP13 (Yüce Sıvı)", "SP14 (Karın Merkezi)", "SP15 (Büyük Karın)", "SP16 (Yan Karın)",
                "SP17 (Yan Göğüs)", "SP18 (Yan Bağlantı)", "SP19 (Yan İki)", "SP20 (Büyük Şehir)",
                "SP21 (Büyük Yan)"
            ]
        elif meridyen == "Heart (HT)":
            points = [
                "HT1 (Yüce Pazar)", "HT2 (Genel Merkezi)", "HT3 (Genel Merkezi Deresi)", "HT4 (Genel Deresi)",
                "HT5 (Yüce Kapı)", "HT6 (Yüce Deniz)", "HT7 (Yüce Avlu)", "HT8 (Genel Saray)", "HT9 (Genel Sonu)"
            ]
        elif meridyen == "Small Intestine (SI)":
            points = [
                "SI1 (Yüce Batı)", "SI2 (Yan Açıklık)", "SI3 (Arka Vadisi)", "SI4 (Kemik Destekçisi)",
                "SI5 (Yang Vadisi)", "SI6 (Yang Çıplaklığı)", "SI7 (Genel Kapı)", "SI8 (Genel Kale)",
                "SI9 (Omuz Birliği)", "SI10 (Yüce Avlu)", "SI11 (Yan Bölge)", "SI12 (Tutuş Noktası)",
                "SI13 (Omuz Noktası)", "SI14 (Üst Omuz)", "SI15 (Omuzun Yüce Noktası)", "SI16 (Boğaz Tepkisi)",
                "SI17 (Boğaz Merkezi)", "SI18 (Çene Tepkisi)", "SI19 (Kulak Merkezi)"
            ]
        elif meridyen == "Bladder (BL)":
            points = [
                "BL1 (Parlak Gözetleme)", "BL2 (Bambu Topu)", "BL3 (Melek İnişi)", "BL4 (Çeneye Ulaşan Işık)",
                "BL5 (Toplu Karşılık)", "BL6 (Büyük Karşılık)", "BL7 (Göksel Kapı)", "BL8 (Azimli Kapsam)",
                "BL9 (Arka Kuyu)", "BL10 (Göksel Direk)", "BL11 (Büyük Usta)", "BL12 (Rüzgar Kapısı)",
                "BL13 (Akciğer Şehri)", "BL14 (Yüce Konak)", "BL15 (Kalp Şehri)", "BL16 (Yüce Pazar)",
                "BL17 (Kalp Penceresi)", "BL18 (Karaciğer Şehri)", "BL19 (Safra Şehri)", "BL20 (Dalak Şehri)",
                "BL21 (Mide Şehri)", "BL22 (Üst Avlu)", "BL23 (Böbrek Şehri)", "BL24 (Yüce Göğüs)",
                "BL25 (Büyük Bağırsak Şehri)", "BL26 (Karın Şehri)", "BL27 (İnce Bağırsak Şehri)",
                "BL28 (Mesane Şehri)", "BL29 (Genel Saray)", "BL30 (Kaçış Yolu)", "BL31 (Üst Pazar)",
                "BL32 (İkinci Pazar)", "BL33 (Üçüncü Pazar)", "BL34 (Dördüncü Pazar)", "BL35 (Bağlantı Noktası)",
                "BL36 (Üst İnziva)", "BL37 (Büyük İnziva)", "BL38 (Orta İnziva)", "BL39 (Alt İnziva)",
                "BL40 (Büküm Deresi)", "BL41 (Destek Bölgesi)", "BL42 (Akciğer Gözetleme)", "BL43 (Kalp Gözetleme)",
                "BL44 (Kalp Gözetleme)", "BL45 (Yüce Gözetleme)", "BL46 (Karaciğer Gözetleme)", "BL47 (Dalak Gözetleme)",
                "BL48 (Safra Gözetleme)", "BL49 (Mide Gözetleme)", "BL50 (Bağlantı Gözetleme)", "BL51 (Büyük Gözetleme)",
                "BL52 (Böbrek Gözetleme)", "BL53 (Mesane Gözetleme)", "BL54 (Yüce Gözetleme)", "BL55 (Alt Gözetleme)",
                "BL56 (Üst Nokta)", "BL57 (Orta Nokta)", "BL58 (Alt Nokta)", "BL59 (Genel Pazar)", "BL60 (Genel Gözetleme)",
                "BL61 (Yüce Yolu)", "BL62 (Yang Yolu)", "BL63 (Yüce Nokta)", "BL64 (Büyük Gözetleme)",
                "BL65 (Genel Gözetleme)", "BL66 (Genel Nokta)", "BL67 (Yüce Toprak)"
            ]
        elif meridyen == "Kidney (KI)":
            points = [
                "KI1 (Genel Kaynak)", "KI2 (Yan İniş)", "KI3 (Büyük Akış)", "KI4 (Genel Saray)",
                "KI5 (Büyük Denge)", "KI6 (Yüce Yol)", "KI7 (Büyük Irmak)", "KI8 (Genel Denge)",
                "KI9 (Genel Kapı)", "KI10 (Genel Toprak)", "KI11 (Yan Kapı)", "KI12 (Genel Şehir)",
                "KI13 (Büyük Avlu)", "KI14 (Yan Yol)", "KI15 (Genel Konak)", "KI16 (Büyük Bağlantı)",
                "KI17 (Yan Bağlantı)", "KI18 (Genel Bağlantı)", "KI19 (Yüce Bağlantı)", "KI20 (Genel Yolu)",
                "KI21 (Yüce Yolu)", "KI22 (Yan Şehri)", "KI23 (Büyük Şehri)", "KI24 (Büyük Şehri Bağlantı)",
                "KI25 (Yan Şehri Bağlantı)", "KI26 (Büyük Şehri Noktası)", "KI27 (Yan Şehri Noktası)"
            ]
        elif meridyen == "Pericardium (PC)":
            points = [
                "PC1 (Göğüs Mezarı)", "PC2 (Göğüs Suyu)", "PC3 (Dirsek Kıvrımı)", "PC4 (Kapının İçinde)",
                "PC5 (İnce Kanal)", "PC6 (İç Kapı)", "PC7 (Büyük Tepki)", "PC8 (Çalışkan Saray)", "PC9 (Meridyen Sonu)"
            ]
        elif meridyen == "Triple Burner (TB)":
            points = [
                "TB1 (Geçit Çukuru)", "TB2 (Sıcak Pazar)", "TB3 (Orta Tepki)", "TB4 (Açık Boşluk)",
                "TB5 (Dış Kapı)", "TB6 (Dış Geçit)", "TB7 (Sıcak Gözetleme)", "TB8 (Üçlü Şehir)", "TB9 (Yan Meridyen)",
                "TB10 (Göğüs Boşluğu)", "TB11 (Göğüs Tepkisi)", "TB12 (Yan Yolu)", "TB13 (Omuz Bağlantısı)", "TB14 (Omuz Gözetleme)",
                "TB15 (Yan Bağlantı)", "TB16 (Yan Yolu)", "TB17 (Kulak Kapısı)", "TB18 (Kulak Suyu)", "TB19 (Kulak Tepkisi)",
                "TB20 (Kulak Gözetleme)", "TB21 (Kulak Geçiti)", "TB22 (Çene Tepkisi)", "TB23 (Yüce Gözetleme)"
            ]
        elif meridyen == "Gall Bladder (GB)":
            points = [
                "GB1 (Göze Ulaşan Işık)", "GB2 (Kulak Kapısı)", "GB3 (Üst Kulak)", "GB4 (Yan Baş)", "GB5 (Göksel Kapı)",
                "GB6 (Yan Saç Çizgisi)", "GB7 (Kulak Üstü)", "GB8 (Yan Bağlantı)", "GB9 (Yan Yolu)", "GB10 (Kulak Merkezi)",
                "GB11 (Yan Şehri)", "GB12 (Kulak Gözetleme)", "GB13 (Yan Tepki)", "GB14 (Büyük Avlu)", "GB15 (Üst Meridyen)",
                "GB16 (Yan Bağlantı)", "GB17 (Yan Yolu)", "GB18 (Yan Şehri)", "GB19 (Yüce Şehir)", "GB20 (Yan Tepki)",
                "GB21 (Omuz Tepkisi)", "GB22 (Yan Avlu)", "GB23 (Üst Omuz)", "GB24 (Yan Tepki)", "GB25 (Omuz Yolu)",
                "GB26 (Yan Meridyen)", "GB27 (Büyük Şehri)", "GB28 (Yan Bağlantı)", "GB29 (Omuz Gözetleme)", "GB30 (Büyük Gözetleme)",
                "GB31 (Omuz Meridyen)", "GB32 (Yan Tepkisi)", "GB33 (Yan Merkez)", "GB34 (Yan Yol)", "GB35 (Yan Kapı)",
                "GB36 (Yan Merkez)", "GB37 (Yan Yolu)", "GB38 (Yan Avlu)", "GB39 (Yan Tepkisi)", "GB40 (Yan Şehri)",
                "GB41 (Yan Yolu)", "GB42 (Yan Tepkisi)", "GB43 (Yan Kapı)", "GB44 (Yan Sonu)"
            ]
        elif meridyen == "Liver (LR)":
            points = [
                "LR1 (Büyük Tepki)", "LR2 (Yan Pazar)", "LR3 (Büyük Birlik)", "LR4 (Yan Kapı)",
                "LR5 (Büyük Kapı)", "LR6 (Yan Gözetleme)", "LR7 (Yan Yolu)", "LR8 (Yan Kapı)",
                "LR9 (Yan Bağlantı)", "LR10 (Yan Şehri)", "LR11 (Yan Tepkisi)", "LR12 (Yan Şehri)",
                "LR13 (Yan Meridyen)", "LR14 (Yan Sonu)"
            ]
        elif meridyen == "Du (DU)":
            points = [
                "DU1 (Uzay Girişi)", "DU2 (Bel Kapısı)", "DU3 (Bel Direği)", "DU4 (Mingmen Kapısı)", "DU5 (Beli Koruyan Nokta)",
                "DU6 (Omur Bağlantısı)", "DU7 (Orta Bel)", "DU8 (Kasılma Bağlantısı)", "DU9 (Sırt Üstü)", "DU10 (Sakrum Bağlantısı)",
                "DU11 (Sırt Merkezi)", "DU12 (Sırt Yüksekliği)", "DU13 (Omuz Tepesi)", "DU14 (Büyük Omur)", "DU15 (Boyun Kapısı)",
                "DU16 (Beyin Kıvrımı)", "DU17 (Beyin Kapısı)", "DU18 (Beyin Bağlantısı)", "DU19 (Beyin Merkez Noktası)", "DU20 (Beyin Tepesi)",
                "DU21 (Ön Kafa Noktası)", "DU22 (Ön Kafa Merkezi)", "DU23 (Ön Kafa Tepesi)", "DU24 (Ön Kafa Kapısı)", "DU25 (Ön Kafa Bağlantısı)",
                "DU26 (Ön Kafa Merkezi)", "DU27 (Üst Dudak Merkezi)", "DU28 (Üst Dudak Bağlantısı)"
            ]
        elif meridyen == "Ren (REN)":
            points = [
                "REN1 (Perineum Merkezi)", "REN2 (Kasıktaki Kapı)", "REN3 (Üçlü Kapı)", "REN4 (Orta Kapı)", "REN5 (İkili Kapı)",
                "REN6 (Enerji Merkezi)", "REN7 (Göbek Üstü)", "REN8 (Göbek)", "REN9 (Su Ayrımı)", "REN10 (Mide Kapısı)",
                "REN11 (Mide Merkezi)", "REN12 (Orta Mide)", "REN13 (Üst Mide)", "REN14 (Kalp Kapısı)", "REN15 (Kalp Merkezi)",
                "REN16 (Göğüs Ortası)", "REN17 (Göğüs Merkezi)", "REN18 (Göğüs Üstü)", "REN19 (Üst Göğüs Kapısı)", "REN20 (Göğüs Tepesi)",
                "REN21 (Göğüs Bağlantısı)", "REN22 (Boğaz Merkezi)", "REN23 (Boğaz Tepesi)", "REN24 (Dudak Merkezi)"
            ]
        elif meridyen == "Extra Points":
            points = [
                "Yintang (Üçüncü Göz)", "Taiyang (Şakaklar)", "EX-HN1 (Baihui - Yüz Toplantısı)", "EX-HN3 (Shanglianquan - Üst Lianquan)",
                "EX-HN5 (Yiming - Parlayan Işık)", "EX-HN6 (Anmian - Huzurlu Uyku)", "EX-HN7 (Yintang - Üçüncü Göz)", 
                "EX-HN8 (Shenmen - Ruhun Kapısı)", "EX-HN9 (Erjian - Kulak Ucu)"
            ]

        self.akupunktur_noktasi_combobox.clear()
        self.akupunktur_noktasi_combobox.addItems(points)


    def sendrom_ara(self):
        arama_kriteri = self.search_entry.text().lower()
        self.result_list.clear()
        try:
            with open('sendrom_aciklamalari.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                for sendrom in sorted(data.keys()):
                    if arama_kriteri in sendrom.lower():
                        item = QListWidgetItem(sendrom)
                        item.setData(Qt.UserRole, sendrom)
                        self.result_list.addItem(item)
        except (FileNotFoundError, json.JSONDecodeError):
            pass


    def sendrom_duzenle(self, item):
        sendrom = item.data(Qt.UserRole)
        self.description_dialog = DescriptionDialog(self, sendrom)
        self.description_dialog.exec_()
        self.sendromlari_listele()

    def guncelle_hasta_secimi_combobox(self, arama_kriteri=""):
        self.hasta_secimi_combobox.clear()

        if arama_kriteri:
            arama_kriteri = arama_kriteri.strip().lower()
            if arama_kriteri.isdigit():
                self.c.execute("SELECT id, ad, soyad FROM hastalar WHERE id LIKE ?", ('%' + arama_kriteri + '%',))
            else:
                self.c.execute("SELECT id, ad, soyad FROM hastalar WHERE LOWER(ad) LIKE ? OR LOWER(soyad) LIKE ?", ('%' + arama_kriteri + '%', '%' + arama_kriteri + '%'))
        else:
            self.c.execute("SELECT id, ad, soyad FROM hastalar")

        hastalar = self.c.fetchall()
        for hasta in hastalar:
            self.hasta_secimi_combobox.addItem(f"{hasta[1]} {hasta[2]} (ID: {hasta[0]})", hasta[0])

    def show_appointments(self, date):
        selected_date = date.toString("yyyy-MM-dd")
        self.c.execute("SELECT * FROM seanslar WHERE tarih = ?", (selected_date,))
        appointments = self.c.fetchall()

        self.appointments_list.clear()
        if appointments:
            for appointment in appointments:
                self.c.execute("SELECT ad, soyad FROM hastalar WHERE id = ?", (appointment[1],))
                patient = self.c.fetchone()
                if patient:
                    self.appointments_list.append(f"Tarih: {appointment[2]} / Saat: {appointment[3]}\nHasta: {patient[0]} {patient[1]}\nİşlem: {appointment[5]}\nNotlar: {appointment[6]}\n\n")
        else:
            self.appointments_list.append("Bu tarihte herhangi bir randevu bulunmamaktadır.")

    def renkli_gunler(self):
        self.c.execute("SELECT DISTINCT tarih FROM seanslar")
        dates = self.c.fetchall()

        format = QTextCharFormat()
        format.setBackground(QColor("yellow"))

        for date in dates:
            date_obj = QDate.fromString(date[0], "yyyy-MM-dd")
            self.calendar.setDateTextFormat(date_obj, format)

    def seans_ekle(self):
        hasta_id = self.hasta_secimi_combobox.currentData()
        tarih = self.seans_tarih.selectedDate().toString("yyyy-MM-dd")
        saat = self.seans_saat.currentText()
        islem = self.islem_entry.toPlainText()
        notlar = self.notlar_entry.toPlainText()

        self.c.execute("SELECT COUNT(*) FROM seanslar WHERE hasta_id = ?", (hasta_id,))
        seans_sayisi = self.c.fetchone()[0] + 1  # Yeni seans numarasını belirle

        self.c.execute('''INSERT INTO seanslar (hasta_id, tarih, saat, seans_no, islem, notlar)
                          VALUES (?, ?, ?, ?, ?, ?)''', (hasta_id, tarih, saat, seans_sayisi, islem, notlar))
        self.conn.commit()

        QMessageBox.information(self, "Başarılı", f"Seans başarıyla eklendi! Hasta ID: {hasta_id} için Seans No: {seans_sayisi}")
        self.show_appointments(self.seans_tarih.selectedDate())
        self.renkli_gunler()


    def seans_ekle_tab(self):
        layout = QVBoxLayout()

        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)

        self.hasta_secimi_combobox = QComboBox()
        self.guncelle_hasta_secimi_combobox()
        scroll_layout.addWidget(self.hasta_secimi_combobox)

        self.arama_seans = QLineEdit()
        self.arama_seans.setPlaceholderText("Hasta Ara")
        self.arama_seans.textChanged.connect(lambda: self.guncelle_hasta_secimi_combobox(self.arama_seans.text()))
        scroll_layout.addWidget(self.arama_seans)

        self.seans_tarih = QCalendarWidget()
        scroll_layout.addWidget(self.seans_tarih)

        self.seans_saat = QComboBox()
        self.populate_time_combobox(self.seans_saat)
        scroll_layout.addWidget(self.seans_saat)

        self.seans_no_entry = QLineEdit()
        self.seans_no_entry.setPlaceholderText("Seans No")
        scroll_layout.addWidget(self.seans_no_entry)

        self.akupunktur_meridyen_combobox = QComboBox()
        self.akupunktur_meridyen_combobox.addItems([
            "Lung (LU)", "Large Intestine (LI)", "Stomach (ST)", "Spleen (SP)",
            "Heart (HT)", "Small Intestine (SI)", "Bladder (BL)", "Kidney (KI)",
            "Pericardium (PC)", "Triple Burner (TB)", "Gall Bladder (GB)", "Liver (LR)",
            "Extra Points"
        ])
        self.akupunktur_meridyen_combobox.setPlaceholderText("Meridyen Seçin")
        self.akupunktur_meridyen_combobox.currentIndexChanged.connect(self.populate_acupuncture_points)
        scroll_layout.addWidget(self.akupunktur_meridyen_combobox)

        self.akupunktur_noktasi_combobox = QComboBox()
        scroll_layout.addWidget(self.akupunktur_noktasi_combobox)

        self.ekle_button = QPushButton("Nokta Ekle")
        self.ekle_button.clicked.connect(self.add_acupuncture_point)
        scroll_layout.addWidget(self.ekle_button)

        self.akupunktur_kombinasyon_category_combobox = QComboBox()
        self.akupunktur_kombinasyon_category_combobox.addItems(["2'li Kombinasyonlar", "3'lü Kombinasyonlar", "4'lü Kombinasyonlar"])
        self.akupunktur_kombinasyon_category_combobox.currentIndexChanged.connect(self.populate_acupuncture_combinations)
        scroll_layout.addWidget(self.akupunktur_kombinasyon_category_combobox)

        self.akupunktur_kombinasyon_combobox = QComboBox()
        scroll_layout.addWidget(self.akupunktur_kombinasyon_combobox)

        self.ekle_kombinasyon_button = QPushButton("Kombinasyon Ekle")
        self.ekle_kombinasyon_button.clicked.connect(self.add_acupuncture_combination)
        scroll_layout.addWidget(self.ekle_kombinasyon_button)

        self.islem_entry = QTextEdit()
        self.islem_entry.setPlaceholderText("İşlem")
        scroll_layout.addWidget(self.islem_entry)

        self.notlar_entry = QTextEdit()
        self.notlar_entry.setPlaceholderText("Notlar")
        scroll_layout.addWidget(self.notlar_entry)

        self.kaydet_button = QPushButton('Kaydet')
        self.kaydet_button.clicked.connect(self.seans_ekle)
        scroll_layout.addWidget(self.kaydet_button)

        self.anket_button = QPushButton("Seans Öncesi Anket")
        self.anket_button.clicked.connect(self.open_seans_oncesi_anketi)
        scroll_layout.addWidget(self.anket_button)

        self.reset_button = QPushButton("Formu Sıfırla")
        self.reset_button.clicked.connect(self.reset_form)
        scroll_layout.addWidget(self.reset_button)

        layout.addWidget(scroll_area)
        self.tab_seans_ekle.setLayout(layout)

    def reset_form(self):
        self.hasta_secimi_combobox.setCurrentIndex(-1)
        self.arama_seans.clear()
        self.seans_tarih.setSelectedDate(QDate.currentDate())
        self.seans_saat.setCurrentIndex(-1)
        self.seans_no_entry.clear()
        self.akupunktur_meridyen_combobox.setCurrentIndex(-1)
        self.akupunktur_noktasi_combobox.clear()
        self.islem_entry.clear()
        self.notlar_entry.clear()

    def populate_acupuncture_points(self):
        meridyen = self.akupunktur_meridyen_combobox.currentText()
        points = self.get_acupuncture_points(meridyen)
        if points:
            self.akupunktur_noktasi_combobox.clear()
            self.akupunktur_noktasi_combobox.addItems(points)

    def populate_acupuncture_combinations(self):
        combinations = {
            "2'li Kombinasyonlar": [
                "LI4 + LR3 (Dört Kapı)",
                "ST36 + SP6 (Genel Tonifikasyon)",
                "PC6 + SP4 (Chong Mai / Mide Problemleri)"
            ],
            "3'lü Kombinasyonlar": [
                "LI4 + LI11 + ST36 (Yang Enerjisi)",
                "SP6 + KI3 + LR3 (Yin Enerjisi)",
                "GB20 + LI4 + LR3 (Baş Ağrısı)"
            ],
            "4'lü Kombinasyonlar": [
                "LI4 + LR3 + SP6 + ST36 (Dört Çiçek)",
                "GB20 + LI4 + LR3 + ST36 (Genel Sağlık)",
                "PC6 + SP4 + ST36 + LI11 (Sindirim)"
            ]
        }

        combination_category = self.akupunktur_kombinasyon_category_combobox.currentText()
        points = combinations.get(combination_category, [])

        self.akupunktur_kombinasyon_combobox.clear()
        self.akupunktur_kombinasyon_combobox.addItems(points)

    def add_acupuncture_point(self):
        point = self.akupunktur_noktasi_combobox.currentText()
        current_text = self.islem_entry.toPlainText()
        new_text = f"{current_text}\n{point}" if current_text else point
        self.islem_entry.setPlainText(new_text)

    def add_acupuncture_combination(self):
        combination = self.akupunktur_kombinasyon_combobox.currentText()
        current_text = self.islem_entry.toPlainText()
        new_text = f"{current_text}\n{combination}" if current_text else combination
        self.islem_entry.setPlainText(new_text)

    def populate_time_combobox(self, combobox):
        times = [
            "10:00", "10:15", "10:30", "10:45",
            "11:00", "11:15", "11:30", "11:45",
            "12:00", "12:15", "12:30", "12:45",
            "13:00", "13:15", "13:30", "13:45",
            "14:00", "14:15", "14:30", "14:45",
            "15:00", "15:15", "15:30", "15:45",
            "16:00", "16:15", "16:30", "16:45",
            "17:00", "17:15", "17:30", "17:45",
            "18:00", "18:15", "18:30", "18:45",
            "19:00", "19:15", "19:30", "19:45",
            "20:00"
        ]
        combobox.addItems(times)

    def diyet_ekle_tab(self):
        layout = QVBoxLayout()

        self.hasta_secimi_combobox_diyet = QComboBox()
        self.guncelle_hasta_secimi_combobox_diyet()
        layout.addWidget(self.hasta_secimi_combobox_diyet)

        self.arama_diyet = QLineEdit()
        self.arama_diyet.setPlaceholderText("Hasta Ara")
        self.arama_diyet.textChanged.connect(lambda: self.guncelle_hasta_secimi_combobox_diyet(self.arama_diyet.text()))
        layout.addWidget(self.arama_diyet)

        self.diyet_entry = QTextEdit()
        self.diyet_entry.setPlaceholderText("Diyet")
        layout.addWidget(self.diyet_entry)

        self.kaydet_button_diyet = QPushButton("Kaydet")
        self.kaydet_button_diyet.clicked.connect(self.diyet_ekle)
        layout.addWidget(self.kaydet_button_diyet)

        self.tab_diyet_ekle.setLayout(layout)

    def guncelle_hasta_secimi_combobox_diyet(self, arama_kriteri=""):
        self.hasta_secimi_combobox_diyet.clear()

        if arama_kriteri:
            arama_kriteri = arama_kriteri.strip().lower()
            if arama_kriteri.isdigit():
                self.c.execute("SELECT id, ad, soyad FROM hastalar WHERE id LIKE ?", ('%' + arama_kriteri + '%',))
            else:
                self.c.execute("SELECT id, ad, soyad FROM hastalar WHERE LOWER(ad) LIKE ? OR LOWER(soyad) LIKE ?", ('%' + arama_kriteri + '%', '%' + arama_kriteri + '%'))
        else:
            self.c.execute("SELECT id, ad, soyad FROM hastalar")

        hastalar = self.c.fetchall()
        for hasta in hastalar:
            self.hasta_secimi_combobox_diyet.addItem(f"{hasta[1]} {hasta[2]} (ID: {hasta[0]})", hasta[0])

    def diyet_ekle(self):
        hasta_id = self.hasta_secimi_combobox_diyet.currentData()
        tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        diyet = self.diyet_entry.toPlainText()

        self.c.execute('''INSERT INTO diyetler (hasta_id, tarih, diyet)
                          VALUES (?, ?, ?)''', (hasta_id, tarih, diyet))
        self.conn.commit()
        QMessageBox.information(self, "Başarılı", "Diyet başarıyla eklendi!")

    def genel_takvim_tab(self):
        layout = QVBoxLayout()

        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.clicked[QDate].connect(self.show_appointments)
        self.renkli_gunler()

        self.appointments_list = QTextEdit()
        self.appointments_list.setReadOnly(True)

        layout.addWidget(self.calendar)
        layout.addWidget(self.appointments_list)

        self.tab_takvim.setLayout(layout)

    def show_appointments(self, date):
        selected_date = date.toString("yyyy-MM-dd")
        self.c.execute("SELECT * FROM seanslar WHERE tarih = ?", (selected_date,))
        appointments = self.c.fetchall()

        self.appointments_list.clear()
        if appointments:
            for appointment in appointments:
                self.c.execute("SELECT ad, soyad FROM hastalar WHERE id = ?", (appointment[1],))
                patient = self.c.fetchone()
                if patient:
                    self.appointments_list.append(f"Tarih: {appointment[2]} / Saat: {appointment[3]}\nHasta: {patient[0]} {patient[1]}\nİşlem: {appointment[5]}\nNotlar: {appointment[6]}\n\n")
    def hasta_dosyasi_ac(self, hasta_id):
        try:
            logging.info(f"Opening patient file for hasta_id: {hasta_id}")
            self.hasta_dosyasi_penceresi = HastaDosyasiPenceresi(hasta_id)
            self.hasta_dosyasi_penceresi.show()
            logging.info(f"Patient file opened successfully for hasta_id: {hasta_id}")
        except Exception as e:
            logging.error(f"Error opening patient file for hasta_id: {hasta_id}, {str(e)}")

    def save_anket_sonuc(self, hasta_id):
        conn = sqlite3.connect('klinik.db')
        c = conn.cursor()
        c.execute("SELECT tarih, anket_sonuc FROM anket_sonuclari WHERE hasta_id = ?", (hasta_id,))
        anket_sonuclari = c.fetchall()
        conn.close()

        if self.hasta_dosyasi_penceresi:
            self.hasta_dosyasi_penceresi.loadAnketSonuclari(anket_sonuclari)

    def open_seans_oncesi_anketi(self):
        hasta_id = self.hasta_secimi_combobox.currentData()  # Seçili hasta ID'sini al
        dialog = SeansOncesiAnketDialog(hasta_id, self)
        if dialog.exec_() == QDialog.Accepted:
            self.save_anket_sonuc(hasta_id)

    def open_seans_sonrasi_anketi(self):
        hasta_id = self.hasta_secimi_combobox.currentData()
        dialog = SeansSonrasiAnketDialog(hasta_id, self)
        if dialog.exec_() == QDialog.Accepted:
            self.save_anket_sonuc(hasta_id)

    def renkli_gunler(self):
        self.c.execute("SELECT DISTINCT tarih FROM seanslar")
        dates = self.c.fetchall()

        format = QTextCharFormat()
        format.setBackground(QColor("yellow"))

        for date in dates:
            date_obj = QDate.fromString(date[0], "yyyy-MM-dd")
            self.calendar.setDateTextFormat(date_obj, format)


if __name__ == "__main__":
    logging.basicConfig(filename='app.log', level=logging.ERROR)
    try:
        app = QApplication(sys.argv)
        mainWindow = KlinikUygulamasi()
        mainWindow.show()
        sys.exit(app.exec_())
    except Exception as e:
        logging.error("Unhandled exception", exc_info=True)
