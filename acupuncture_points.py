def populate_acupuncture_points(self):
    meridyen = self.akupunktur_meridyen_combobox.currentText()
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

