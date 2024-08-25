from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QComboBox, QPushButton, QHBoxLayout
import json
import sqlite3

class SeansOncesiAnketDialog(QDialog):
    def __init__(self, hasta_id, parent=None):
        super().__init__(parent)
        self.hasta_id = hasta_id
        self.setWindowTitle("Seans Öncesi Anket")
        self.setGeometry(100, 100, 600, 400)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.combo_boxes = []
        anket_sorulari = [
            "İştahın nasıl?",
            "Uyku düzenin nasıl?",
            "Stres seviyen nedir?",
            "Enerji seviyen nasıl?",
            "Sindirim problemin var mı?",
            "Kas ve eklem ağrıların var mı?",
            "Cilt problemin var mı?",
            "Adet düzenin nasıl? (Kadınlar için)"
        ]
        for soru in anket_sorulari:
            label = soru
            combo_box = QComboBox()
            combo_box.addItems(["0", "1", "2", "3", "4"])
            form_layout.addRow(label, combo_box)
            self.combo_boxes.append(combo_box)

        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        self.submit_button = QPushButton("Gönder")
        self.submit_button.clicked.connect(self.submit_answers)
        self.cancel_button = QPushButton("İptal")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def submit_answers(self):
        answers = [combo_box.currentText() for combo_box in self.combo_boxes]
        answers_dict = {f"soru_{i + 1}": answers[i] for i in range(len(answers))}
        answers_json = json.dumps(answers_dict, ensure_ascii=False)

        conn = sqlite3.connect('klinik.db')
        c = conn.cursor()
        c.execute("INSERT INTO anket_sonuclari (hasta_id, tarih, anket_sonuc) VALUES (?, DATE('now'), ?)", (self.hasta_id, answers_json))
        conn.commit()
        conn.close()

        self.accept()
