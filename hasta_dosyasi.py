import logging
import sqlite3
import os
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTextEdit, QLabel, QScrollArea, QPushButton, QHBoxLayout, QFormLayout, QLineEdit, QComboBox, QTabWidget, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QFont
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog



class HastaDosyasiPenceresi(QMainWindow):
    def __init__(self, hasta_id, parent=None):
        super().__init__(parent)
        self.hasta_id = hasta_id
        self.web_view = None
        self.edit_widget = None
        self.edit_button = None
        self.print_button = None  # Print button tanımı
        logging.info(f"Initializing HastaDosyasiPenceresi for hasta_id: {self.hasta_id}")
        self.initUI()

    def initUI(self):
        logging.info("Entering initUI function")
        self.setWindowTitle(f"Hasta Dosyası - {self.hasta_id}")
        self.setGeometry(50, 50, 1600, 900)  # Pencere boyutlarını arttırın

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        self.web_view = QWebEngineView()
        self.tabs.addTab(self.web_view, "Görünüm")

        self.edit_button = QPushButton("Düzenle")
        self.edit_button.setFont(QFont("Arial", 16))  # Yazı tipini büyütün
        self.edit_button.clicked.connect(self.edit_mode)
        self.layout.addWidget(self.edit_button)

        self.print_button = QPushButton("Yazdır")  # Print button ekleme
        self.print_button.setFont(QFont("Arial", 16))  # Yazı tipini büyütün
        self.print_button.clicked.connect(self.print_file)
        self.layout.addWidget(self.print_button)

        self.load_patient_file()
        logging.info("Exiting initUI function")

    def print_file(self):
        try:
            printer = QPrinter(QPrinter.HighResolution)
            dialog = QPrintDialog(printer, self)
            if dialog.exec_() == QPrintDialog.Accepted:
                self.handle_print_request(printer)
        except Exception as e:
            logging.error(f"Printing error: {str(e)}")
            QMessageBox.critical(self, "Hata", f"Yazdırma sırasında bir hata oluştu: {str(e)}")

    def handle_print_request(self, printer):
        def callback(result):
            if result:
                painter = QPainter(printer)
                painter.drawPixmap(0, 0, self.web_view.grab())
                painter.end()

        self.web_view.page().print(printer, callback)

    def load_patient_file(self):
        # Remove the edit widget if it exists
        if self.edit_widget:
            self.layout.removeWidget(self.edit_widget)
            self.edit_widget.deleteLater()
            self.edit_widget = None

        # Only add the web_view if it does not exist
        if not self.web_view:
            self.web_view = QWebEngineView()
            self.layout.addWidget(self.web_view)

        # Only add the edit_button if it does not exist
        if not self.edit_button:
            self.edit_button = QPushButton("Düzenle")
            self.edit_button.clicked.connect(self.edit_mode)
            self.layout.addWidget(self.edit_button)

        try:
            logging.info("Loading patient data...")
            html_content = self.generate_html_content()
            self.display_html_content(html_content)
            logging.info("Patient data loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading patient file: {str(e)}")
            raise
    def edit_mode(self):
        if self.web_view:
            self.layout.removeWidget(self.web_view)
            self.web_view.deleteLater()
            self.web_view = None

        if self.edit_button:
            self.layout.removeWidget(self.edit_button)
            self.edit_button.deleteLater()
            self.edit_button = None

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # Temel Bilgiler Sekmesi
        self.basic_info_tab = QWidget()
        self.basic_info_layout = QVBoxLayout(self.basic_info_tab)
        self.scroll_area_basic = QScrollArea()
        self.scroll_area_basic.setWidgetResizable(True)
        self.scroll_content_basic = QWidget()
        self.scroll_layout_basic = QVBoxLayout(self.scroll_content_basic)
        self.patient_info_edit = QTextEdit()
        self.patient_info_edit.setPlainText(self.generate_patient_info_text())
        self.scroll_layout_basic.addWidget(QLabel("Temel Bilgiler"))
        self.scroll_layout_basic.addWidget(self.patient_info_edit)
        self.scroll_area_basic.setWidget(self.scroll_content_basic)
        self.basic_info_layout.addWidget(self.scroll_area_basic)
        self.basic_info_layout.addWidget(QPushButton("Kaydet", clicked=self.save_data))
        self.basic_info_layout.addWidget(QPushButton("Hasta Dosyasını Aç", clicked=self.open_updated_patient_file))
        self.tabs.addTab(self.basic_info_tab, "Temel Bilgiler")

        # Seans Bilgileri Sekmesi
        self.session_tab = QWidget()
        self.session_layout = QVBoxLayout(self.session_tab)
        self.scroll_area_session = QScrollArea()
        self.scroll_area_session.setWidgetResizable(True)
        self.scroll_content_session = QWidget()
        self.scroll_layout_session = QVBoxLayout(self.scroll_content_session)
        seans_data = self.get_seans_data()
        self.seans_edits = []
        for seans in seans_data:
            session_form = QFormLayout()
            session_id = seans[0]
            tarih_edit = QLineEdit(seans[2])
            saat_edit = QLineEdit(seans[3])
            islem_edit = QTextEdit(seans[5])
            notlar_edit = QTextEdit(seans[6])
            session_form.addRow("Tarih:", tarih_edit)
            session_form.addRow("Saat:", saat_edit)
            session_form.addRow("İşlem:", islem_edit)
            session_form.addRow("Notlar:", notlar_edit)
            self.scroll_layout_session.addLayout(session_form)
            self.seans_edits.append((session_id, tarih_edit, saat_edit, islem_edit, notlar_edit))
        self.scroll_area_session.setWidget(self.scroll_content_session)
        self.session_layout.addWidget(self.scroll_area_session)
        self.session_layout.addWidget(QPushButton("Kaydet", clicked=self.save_data))
        self.session_layout.addWidget(QPushButton("Hasta Dosyasını Aç", clicked=self.open_updated_patient_file))
        self.tabs.addTab(self.session_tab, "Seans Bilgileri")

        # Diyet Bilgileri Sekmesi
        self.diet_tab = QWidget()
        self.diet_layout = QVBoxLayout(self.diet_tab)
        self.scroll_area_diet = QScrollArea()
        self.scroll_area_diet.setWidgetResizable(True)
        self.scroll_content_diet = QWidget()
        self.scroll_layout_diet = QVBoxLayout(self.scroll_content_diet)
        self.diet_info_edit = QTextEdit()
        self.diet_info_edit.setPlainText(self.generate_diet_info_text())
        self.scroll_layout_diet.addWidget(QLabel("Diyet Bilgileri"))
        self.scroll_layout_diet.addWidget(self.diet_info_edit)
        self.scroll_area_diet.setWidget(self.scroll_content_diet)
        self.diet_layout.addWidget(self.scroll_area_diet)
        self.diet_layout.addWidget(QPushButton("Kaydet", clicked=self.save_data))
        self.diet_layout.addWidget(QPushButton("Hasta Dosyasını Aç", clicked=self.open_updated_patient_file))
        self.tabs.addTab(self.diet_tab, "Diyet Bilgileri")

        self.layout.addWidget(self.tabs)



    def generate_html_content(self):
        patient_data = self.get_patient_data()
        seans_data = self.get_seans_data()
        diyet_data = self.get_diyet_data()

        evli_text = 'Evet' if patient_data[6] else 'Hayır'

        seanslar_html = self.generate_seans_html(seans_data)
        diyetler_html = self.generate_diyet_html(diyet_data)

        html_content = f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Hasta Dosyası - {patient_data[1]} {patient_data[2]}</title>
                <style>
                    body {{ font-family: 'Arial', sans-serif; background-color: #f4f4f4; color: #333; }}
                    .container {{ width: 80%; margin: auto; padding: 20px; background-color: #fff; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }}
                    h1 {{ text-align: center; color: #4CAF50; font-family: 'Georgia', serif; }}
                    h2 {{ color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 5px; font-family: 'Courier New', monospace; }}
                    table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
                    table, th, td {{ border: 1px solid #ddd; }}
                    th, td {{ padding: 10px; text-align: left; }}
                    th {{ background-color: #f4f4f4; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Hasta Dosyası - {patient_data[1]} {patient_data[2]}</h1>
                    <div class="section">
                        <h2>Hasta Bilgileri</h2>
                        <table>
                            <tr><th>Özellik</th><th>Bilgi</th></tr>
                            <tr><td>ID</td><td>{patient_data[0]}</td></tr>
                            <tr><td>Ad</td><td>{patient_data[1]}</td></tr>
                            <tr><td>Soyad</td><td>{patient_data[2]}</td></tr>
                            <tr><td>Yaş</td><td>{patient_data[3]}</td></tr>
                            <tr><td>TC</td><td>{patient_data[4]}</td></tr>
                            <tr><td>Meslek</td><td>{patient_data[5]}</td></tr>
                            <tr><td>Evli</td><td>{evli_text}</td></tr>
                            <tr><td>Çocuk Sayısı</td><td>{patient_data[7]}</td></tr>
                            <tr><td>Cinsiyet</td><td>{patient_data[8]}</td></tr>
                            <tr><td>Telefon</td><td>{patient_data[9]}</td></tr>
                            <tr><td>Email</td><td>{patient_data[10]}</td></tr>
                            <tr><td>Adres</td><td>{patient_data[11]}</td></tr>
                            <tr><td>Ana Şikayet</td><td>{patient_data[12]}</td></tr>
                        </table>
                    </div>
                    <div class="section">
                        <h2>Hasta Seansları</h2>
                        {seanslar_html}
                    </div>
                    <div class="section">
                        <h2>Diyet Bilgileri</h2>
                        {diyetler_html}
                    </div>
                </div>
            </body>
            </html>
        """
        return html_content


    def display_html_content(self, html_content):
        file_path = os.path.join(os.getcwd(), 'hasta_dosyasi.html')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        if self.web_view:
            self.web_view.setUrl(QUrl.fromLocalFile(file_path))

    def generate_patient_info_text(self):
        patient_data = self.get_patient_data()
        evli_text = 'Evet' if patient_data[6] else 'Hayır'
        return (f"ID: {patient_data[0]}\n"
                f"Ad: {patient_data[1]}\n"
                f"Soyad: {patient_data[2]}\n"
                f"Yaş: {patient_data[3]}\n"
                f"TC: {patient_data[4]}\n"
                f"Meslek: {patient_data[5]}\n"
                f"Evli: {evli_text}\n"
                f"Çocuk Sayısı: {patient_data[7]}\n"
                f"Cinsiyet: {patient_data[8]}\n"
                f"Telefon: {patient_data[9]}\n"
                f"Email: {patient_data[10]}\n"
                f"Adres: {patient_data[11]}\n"
                f"Ana Şikayet: {patient_data[12]}")

    def generate_session_info_text(self):
        seans_data = self.get_seans_data()
        return "\n\n".join([
            f"Tarih: {seans[2]} Saat: {seans[3]}\nİşlem: {seans[5]}\nNotlar: {seans[6]}"
            for seans in seans_data
        ])

    def generate_diet_info_text(self):
        diyet_data = self.get_diyet_data()
        return "\n\n".join([
            f"Tarih: {diyet[2]}\nDiyet: {diyet[3]}"
            for diyet in diyet_data
        ])

    def save_data(self):
        try:
            conn = sqlite3.connect('klinik.db')
            c = conn.cursor()

            patient_info_lines = self.patient_info_edit.toPlainText().split('\n')
            patient_data = {line.split(': ')[0]: line.split(': ')[1] for line in patient_info_lines if ': ' in line}

            logging.info(f"Patient data: {patient_data}")

            update_query = '''UPDATE hastalar SET ad = ?, soyad = ?, yas = ?, tc = ?, meslek = ?, evli = ?, cocuk_sayisi = ?, cinsiyet = ?, telefon = ?, email = ?, adres = ?, ana_sikayet = ? WHERE id = ?'''
            update_values = (
                patient_data.get('Ad', ''),
                patient_data.get('Soyad', ''),
                patient_data.get('Yaş', ''),
                patient_data.get('TC', ''),
                patient_data.get('Meslek', ''),
                1 if patient_data.get('Evli', 'Hayır') == 'Evet' else 0,
                patient_data.get('Çocuk Sayısı', ''),
                patient_data.get('Cinsiyet', ''),
                patient_data.get('Telefon', ''),
                patient_data.get('Email', ''),
                patient_data.get('Adres', ''),
                patient_data.get('Ana Şikayet', ''),
                self.hasta_id
            )

            logging.info(f"Update query: {update_query}")
            logging.info(f"Update values: {update_values}")

            c.execute(update_query, update_values)

            for session_id, tarih_edit, saat_edit, islem_edit, notlar_edit in self.seans_edits:
                tarih = tarih_edit.text()
                saat = saat_edit.text()
                islem = islem_edit.toPlainText()
                notlar = notlar_edit.toPlainText()
                logging.info(f"Seans Güncelleme: {session_id}, {tarih}, {saat}, {islem}, {notlar}")
                c.execute('''UPDATE seanslar SET tarih = ?, saat = ?, islem = ?, notlar = ? WHERE id = ?''', 
                          (tarih, saat, islem, notlar, session_id))

            diet_info_lines = self.diet_info_edit.toPlainText().split('\n\n')
            logging.info(f"Diet info lines: {diet_info_lines}")
            
            c.execute("DELETE FROM diyetler WHERE hasta_id = ?", (self.hasta_id,))
            for diet_info in diet_info_lines:
                if diet_info.strip():
                    lines = diet_info.split('\n')
                    logging.info(f"Diet info lines split: {lines}")
                    if len(lines) >= 2:
                        try:
                            tarih = lines[0].split(': ')[1]
                            diyet = '\n'.join(lines[1:])
                            logging.info(f"Diyet Ekleme: {tarih}, {diyet}")
                            c.execute("INSERT INTO diyetler (hasta_id, tarih, diyet) VALUES (?, ?, ?)", 
                                      (self.hasta_id, tarih, diyet))
                        except IndexError:
                            logging.error(f"Diyet verileri işlenirken hata oluştu: {lines}")
                            continue

            conn.commit()
            conn.close()

            QMessageBox.information(self, "Başarılı", "Veriler başarıyla kaydedildi.")
            self.load_patient_file()
        except Exception as e:
            logging.error(f"Veri kaydetme hatası: {str(e)}")
            QMessageBox.critical(self, "Hata", f"Veri kaydetme sırasında bir hata oluştu: {str(e)}")


    def get_patient_data(self):
        logging.info("Getting patient data...")
        conn = sqlite3.connect('klinik.db')
        c = conn.cursor()
        c.execute("SELECT * FROM hastalar WHERE id = ?", (self.hasta_id,))
        data = c.fetchone()
        conn.close()
        logging.info(f"Patient data: {data}")
        return data

    def get_seans_data(self):
        logging.info("Getting sessions data...")
        conn = sqlite3.connect('klinik.db')
        c = conn.cursor()
        c.execute("SELECT * FROM seanslar WHERE hasta_id = ?", (self.hasta_id,))
        data = c.fetchall()
        conn.close()
        logging.info(f"Sessions data: {data}")
        return data

    def get_diyet_data(self):
        logging.info("Getting diet data...")
        conn = sqlite3.connect('klinik.db')
        c = conn.cursor()
        c.execute("SELECT * FROM diyetler WHERE hasta_id = ?", (self.hasta_id,))
        data = c.fetchall()
        conn.close()
        logging.info(f"Diet data: {data}")
        return data

    def generate_seans_html(self, seans_data):
        seanslar_html = "".join([
            f"<p><strong>Tarih:</strong> {seans[2]} <strong>Saat:</strong> {seans[3]}<br>"
            f"<strong>İşlem:</strong> {seans[5]}<br>"
            f"<strong>Notlar:</strong> {seans[6]}<br><hr></p>"
            for seans in seans_data
        ])
        return seanslar_html

    def generate_diyet_html(self, diyet_data):
        diyetler_html = "".join([
            f"<p><strong>Tarih:</strong> {diyet[2]}<br>"
            f"<strong>Diyet:</strong> {diyet[3]}<br><hr></p>"
            for diyet in diyet_data
        ])
        return diyetler_html
    def open_updated_patient_file(self):
        self.close()
        self.main_window = HastaDosyasiPenceresi(hasta_id=self.hasta_id)
        self.main_window.show()

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = HastaDosyasiPenceresi(hasta_id=16)  # Örnek hasta_id
    window.show()
    sys.exit(app.exec_())
