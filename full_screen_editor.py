from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtCore import Qt, QSizeF
from PyQt5.QtGui import QPainter, QTextDocument

class FullScreenEditor(QDialog):
        def __init__(self, text, title, parent=None):
            super().__init__(parent)
            self.setWindowTitle(title)
            self.setGeometry(100, 100, 800, 600)
            self.setWindowState(self.windowState() | Qt.WindowFullScreen)
            layout = QVBoxLayout()
            self.text_edit = QTextEdit()
            self.text_edit.setText(text)
            self.text_edit.setFont(QFont("Arial", 14))
            layout.addWidget(self.text_edit)
            button_layout = QHBoxLayout()
            self.save_button = QPushButton("Kaydet")
            self.save_button.clicked.connect(self.save_text)
            button_layout.addWidget(self.save_button)
            self.print_button = QPushButton("Yazdır")
            self.print_button.clicked.connect(self.print_text)
            button_layout.addWidget(self.print_button)
            self.close_button = QPushButton("Kapat")
            self.close_button.clicked.connect(self.close)
            button_layout.addWidget(self.close_button)
            layout.addLayout(button_layout)
            self.setLayout(layout)

        def save_text(self):
            self.accept()

        def get_text(self):
            return self.text_edit.toPlainText()

        def print_text(self):
            printer = QPrinter(QPrinter.HighResolution)
            printer.setPageSize(QPrinter.A4)
            printer.setOrientation(QPrinter.Portrait)
            printer.setResolution(300)  # Çözünürlüğü ayarlayın

            dialog = QPrintDialog(printer, self)
            if dialog.exec_() == QPrintDialog.Accepted:
                document = QTextDocument()
                document.setHtml(self.text_edit.toHtml())
            # Yazdırılacak metin boyutunu ayarlayın
                font = QFont("Arial", 12)
                document.setDefaultFont(font)
                document.setPageSize(QSizeF(printer.pageRect().size()))
                document.print_(printer)
