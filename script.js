const akupunkturNoktalari = {
    "Lung (LU)": ["LU1 (Orta Saray)", "LU2 (Bulut Kapısı)", "LU3 (Göksel Depo)", "LU4 (Göksel Bina)", "LU5 (Büküm Havuzu)", "LU6 (En Yüce Çukur)", "LU7 (Kırık Dizi)", "LU8 (Kan Kanalı)", "LU9 (Büyük Uçurum)", "LU10 (Balık Karnı)", "LU11 (Azimli Tükenmez)"],
    "Large Intestine (LI)": ["LI1 (Metalin Büyüklüğü)", "LI2 (İkinci Aralık)", "LI3 (Üçüncü Aralık)", "LI4 (Büyük Birlik)", "LI5 (Yang Deresi)", "LI6 (Yan Ağız)", "LI7 (Sıcaklık Alanı)", "LI8 (Üst Akış)", "LI9 (Düşük Akış)", "LI10 (Kol Üç Mili)", "LI11 (Eğik Havuz)", "LI12 (Kol Kemeri)", "LI13 (Kol Üst Noktası)", "LI14 (Kolun Yüce Noktası)", "LI15 (Omuz Kemeri)", "LI16 (Büyük Kemik)", "LI17 (Gırtlak Yardımı)", "LI18 (Dış Kuyu)", "LI19 (Yan Kuyu)", "LI20 (Koku Kapısı)"],
    "Stomach (ST)": ["ST1 (Tepkinin Uçları)", "ST2 (Dört Beyazlık)", "ST3 (Büyük Kemik)", "ST4 (Toplu Üst Nokta)", "ST5 (Büyük Karşılık)", "ST6 (Çene Arabası)", "ST7 (Alt Çene Birliği)", "ST8 (Bağlantı Köşesi)", "ST9 (Karşı Tepki)", "ST10 (Su Mağarası)", "ST11 (Gaz Bağlantısı)", "ST12 (Boşluk Kapısı)", "ST13 (Boğaz Açıklığı)", "ST14 (Göğüs Temizliği)", "ST15 (Göğüs Kapısı)", "ST16 (Göğüs Tatlılığı)", "ST17 (Göğüs Orta Nokta)", "ST18 (Süt Kapağı)", "ST19 (Çözülme)", "ST20 (Destek Noktası)", "ST21 (İç Avlu)", "ST22 (Büyük Karın)", "ST23 (Karın Üçüncü Noktası)", "ST24 (Karın Merkezi)", "ST25 (Göbek Bölgesi)", "ST26 (Dış Saha)", "ST27 (Büyük İç)", "ST28 (Sıvı Kapısı)", "ST29 (Dönme Noktası)", "ST30 (Qi'nin Kavşağı)", "ST31 (Üst Köşe)", "ST32 (İkinci Yan)", "ST33 (Orta Yan)", "ST34 (Işığın Yolu)", "ST35 (Yan Diz)", "ST36 (Ayağın Üç Noktası)", "ST37 (Üçüncü Bölge)", "ST38 (Orta Kanal)", "ST39 (Alt Bölge)", "ST40 (Hoşluk Yolu)", "ST41 (Karşı Tepki)", "ST42 (Chongyang)", "ST43 (Derin Kuyu)", "ST44 (İç Avlu)", "ST45 (Sertlik Alanı)"],
    "Spleen (SP)": ["SP1 (Gizli Beyazlık)", "SP2 (Büyük Metin)", "SP3 (En Yüce Beyaz)", "SP4 (Aynı Konum)", "SP5 (Ağır Şehir)", "SP6 (Üç Gizemli)", "SP7 (Kaçan Taban)", "SP8 (Yeraltı Kaynağı)", "SP9 (Su Bahçesi)", "SP10 (Deniz Büyük Konak)", "SP11 (Kuşak Açıklığı)", "SP12 (Ağır Sıvı)", "SP13 (Yüce Sıvı)", "SP14 (Karın Merkezi)", "SP15 (Büyük Karın)", "SP16 (Yan Karın)", "SP17 (Yan Göğüs)", "SP18 (Yan Bağlantı)", "SP19 (Yan İki)", "SP20 (Büyük Şehir)", "SP21 (Büyük Yan)"],
    "Heart (HT)": ["HT1 (Yüce Pazar)", "HT2 (Genel Merkezi)", "HT3 (Genel Merkezi Deresi)", "HT4 (Genel Deresi)", "HT5 (Yüce Kapı)", "HT6 (Yüce Deniz)", "HT7 (Yüce Avlu)", "HT8 (Genel Saray)", "HT9 (Genel Sonu)"],
    "Small Intestine (SI)": ["SI1 (Yüce Batı)", "SI2 (Yan Açıklık)", "SI3 (Arka Vadisi)", "SI4 (Kemik Destekçisi)", "SI5 (Yang Vadisi)", "SI6 (Yang Çıplaklığı)", "SI7 (Genel Kapı)", "SI8 (Genel Kale)", "SI9 (Omuz Birliği)", "SI10 (Yüce Avlu)", "SI11 (Yan Bölge)", "SI12 (Tutuş Noktası)", "SI13 (Omuz Noktası)", "SI14 (Üst Omuz)", "SI15 (Omuzun Yüce Noktası)", "SI16 (Boğaz Tepkisi)", "SI17 (Boğaz Merkezi)", "SI18 (Çene Tepkisi)", "SI19 (Kulak Merkezi)"],
    "Bladder (BL)": ["BL1 (Parlak Gözetleme)", "BL2 (Bambu Topu)", "BL3 (Melek İnişi)", "BL4 (Çeneye Ulaşan Işık)", "BL5 (Toplu Karşılık)", "BL6 (Büyük Karşılık)", "BL7 (Göksel Kapı)", "BL8 (Azimli Kapsam)", "BL9 (Arka Kuyu)", "BL10 (Göksel Direk)", "BL11 (Büyük Usta)", "BL12 (Rüzgar Kapısı)", "BL13 (Akciğer Şehri)", "BL14 (Yüce Konak)", "BL15 (Kalp Şehri)", "BL16 (Yüce Pazar)", "BL17 (Kalp Penceresi)", "BL18 (Karaciğer Şehri)", "BL19 (Safra Şehri)", "BL20 (Dalak Şehri)", "BL21 (Mide Şehri)", "BL22 (Üst Avlu)", "BL23 (Böbrek Şehri)", "BL24 (Yüce Göğüs)", "BL25 (Büyük Bağırsak Şehri)", "BL26 (Karın Şehri)", "BL27 (İnce Bağırsak Şehri)", "BL28 (Mesane Şehri)", "BL29 (Genel Saray)", "BL30 (Kaçış Yolu)", "BL31 (Üst Pazar)", "BL32 (İkinci Pazar)", "BL33 (Üçüncü Pazar)", "BL34 (Dördüncü Pazar)", "BL35 (Bağlantı Noktası)", "BL36 (Üst İnziva)", "BL37 (Büyük İnziva)", "BL38 (Orta İnziva)", "BL39 (Alt İnziva)", "BL40 (Büküm Deresi)", "BL41 (Destek Bölgesi)", "BL42 (Akciğer Gözetleme)", "BL43 (Kalp Gözetleme)", "BL44 (Kalp Gözetleme)", "BL45 (Yüce Gözetleme)", "BL46 (Karaciğer Gözetleme)", "BL47 (Dalak Gözetleme)", "BL48 (Safra Gözetleme)", "BL49 (Mide Gözetleme)", "BL50 (Bağlantı Gözetleme)", "BL51 (Büyük Gözetleme)", "BL52 (Böbrek Gözetleme)", "BL53 (Mesane Gözetleme)", "BL54 (Yüce Gözetleme)", "BL55 (Alt Gözetleme)", "BL56 (Üst Nokta)", "BL57 (Orta Nokta)", "BL58 (Alt Nokta)", "BL59 (Genel Pazar)", "BL60 (Genel Gözetleme)", "BL61 (Yüce Yolu)", "BL62 (Yang Yolu)", "BL63 (Yüce Nokta)", "BL64 (Büyük Gözetleme)", "BL65 (Genel Gözetleme)", "BL66 (Genel Nokta)", "BL67 (Yüce Toprak)"],
    "Kidney (KI)": ["KI1 (Genel Kaynak)", "KI2 (Yan İniş)", "KI3 (Büyük Akış)", "KI4 (Genel Saray)", "KI5 (Büyük Denge)", "KI6 (Yüce Yol)", "KI7 (Büyük Irmak)", "KI8 (Genel Denge)", "KI9 (Genel Kapı)", "KI10 (Genel Toprak)", "KI11 (Yan Kapı)", "KI12 (Genel Şehir)", "KI13 (Büyük Avlu)", "KI14 (Yan Yol)", "KI15 (Genel Konak)", "KI16 (Büyük Bağlantı)", "KI17 (Yan Bağlantı)", "KI18 (Genel Bağlantı)", "KI19 (Yüce Bağlantı)", "KI20 (Genel Yolu)", "KI21 (Yüce Yolu)", "KI22 (Yan Şehri)", "KI23 (Büyük Şehri)", "KI24 (Büyük Şehri Bağlantı)", "KI25 (Yan Şehri Bağlantı)", "KI26 (Büyük Şehri Noktası)", "KI27 (Yan Şehri Noktası)"],
    "Pericardium (PC)": ["PC1 (Göğüs Mezarı)", "PC2 (Göğüs Suyu)", "PC3 (Dirsek Kıvrımı)", "PC4 (Kapının İçinde)", "PC5 (İnce Kanal)", "PC6 (İç Kapı)", "PC7 (Büyük Tepki)", "PC8 (Çalışkan Saray)", "PC9 (Meridyen Sonu)"],
    "Triple Burner (TB)": ["TB1 (Geçit Çukuru)", "TB2 (Sıcak Pazar)", "TB3 (Orta Tepki)", "TB4 (Açık Boşluk)", "TB5 (Dış Kapı)", "TB6 (Dış Geçit)", "TB7 (Sıcak Gözetleme)", "TB8 (Üçlü Şehir)", "TB9 (Yan Meridyen)", "TB10 (Göğüs Boşluğu)", "TB11 (Göğüs Tepkisi)", "TB12 (Yan Yolu)", "TB13 (Omuz Bağlantısı)", "TB14 (Omuz Gözetleme)", "TB15 (Yan Bağlantı)", "TB16 (Yan Yolu)", "TB17 (Kulak Kapısı)", "TB18 (Kulak Suyu)", "TB19 (Kulak Tepkisi)", "TB20 (Kulak Gözetleme)", "TB21 (Kulak Geçiti)", "TB22 (Çene Tepkisi)", "TB23 (Yüce Gözetleme)"],
    "Gall Bladder (GB)": ["GB1 (Göze Ulaşan Işık)", "GB2 (Kulak Kapısı)", "GB3 (Üst Kulak)", "GB4 (Yan Baş)", "GB5 (Göksel Kapı)", "GB6 (Yan Saç Çizgisi)", "GB7 (Kulak Üstü)", "GB8 (Yan Bağlantı)", "GB9 (Yan Yolu)", "GB10 (Kulak Merkezi)", "GB11 (Yan Şehri)", "GB12 (Kulak Gözetleme)", "GB13 (Yan Tepki)", "GB14 (Büyük Avlu)", "GB15 (Üst Meridyen)", "GB16 (Yan Bağlantı)", "GB17 (Yan Yolu)", "GB18 (Yan Şehri)", "GB19 (Yüce Şehir)", "GB20 (Yan Tepki)", "GB21 (Omuz Tepkisi)", "GB22 (Yan Avlu)", "GB23 (Üst Omuz)", "GB24 (Yan Tepki)", "GB25 (Omuz Yolu)", "GB26 (Yan Meridyen)", "GB27 (Büyük Şehri)", "GB28 (Yan Bağlantı)", "GB29 (Omuz Gözetleme)", "GB30 (Büyük Gözetleme)", "GB31 (Omuz Meridyen)", "GB32 (Yan Tepkisi)", "GB33 (Yan Merkez)", "GB34 (Yan Yol)", "GB35 (Yan Kapı)", "GB36 (Yan Merkez)", "GB37 (Yan Yolu)", "GB38 (Yan Avlu)", "GB39 (Yan Tepkisi)", "GB40 (Yan Şehri)", "GB41 (Yan Yolu)", "GB42 (Yan Tepkisi)", "GB43 (Yan Kapı)", "GB44 (Yan Sonu)"],
    "Liver (LR)": ["LR1 (Büyük Tepki)", "LR2 (Yan Pazar)", "LR3 (Büyük Birlik)", "LR4 (Yan Kapı)", "LR5 (Büyük Kapı)", "LR6 (Yan Gözetleme)", "LR7 (Yan Yolu)", "LR8 (Yan Kapı)", "LR9 (Yan Bağlantı)", "LR10 (Yan Şehri)", "LR11 (Yan Tepkisi)", "LR12 (Yan Şehri)", "LR13 (Yan Meridyen)", "LR14 (Yan Sonu)"],
    "Du (DU)": ["DU1 (Uzay Girişi)", "DU2 (Bel Kapısı)", "DU3 (Bel Direği)", "DU4 (Mingmen Kapısı)", "DU5 (Beli Koruyan Nokta)", "DU6 (Omur Bağlantısı)", "DU7 (Orta Bel)", "DU8 (Kasılma Bağlantısı)", "DU9 (Sırt Üstü)", "DU10 (Sakrum Bağlantısı)", "DU11 (Sırt Merkezi)", "DU12 (Sırt Yüksekliği)", "DU13 (Omuz Tepesi)", "DU14 (Büyük Omur)", "DU15 (Boyun Kapısı)", "DU16 (Beyin Kıvrımı)", "DU17 (Beyin Kapısı)", "DU18 (Beyin Bağlantısı)", "DU19 (Beyin Merkez Noktası)", "DU20 (Beyin Tepesi)", "DU21 (Ön Kafa Noktası)", "DU22 (Ön Kafa Merkezi)", "DU23 (Ön Kafa Tepesi)", "DU24 (Ön Kafa Kapısı)", "DU25 (Ön Kafa Bağlantısı)", "DU26 (Ön Kafa Merkezi)", "DU27 (Üst Dudak Merkezi)", "DU28 (Üst Dudak Bağlantısı)"],
    "Ren (REN)": ["REN1 (Perineum Merkezi)", "REN2 (Kasıktaki Kapı)", "REN3 (Üçlü Kapı)", "REN4 (Orta Kapı)", "REN5 (İkili Kapı)", "REN6 (Enerji Merkezi)", "REN7 (Göbek Üstü)", "REN8 (Göbek)", "REN9 (Su Ayrımı)", "REN10 (Mide Kapısı)", "REN11 (Mide Merkezi)", "REN12 (Orta Mide)", "REN13 (Üst Mide)", "REN14 (Kalp Kapısı)", "REN15 (Kalp Merkezi)", "REN16 (Göğüs Ortası)", "REN17 (Göğüs Merkezi)", "REN18 (Göğüs Üstü)", "REN19 (Üst Göğüs Kapısı)", "REN20 (Göğüs Tepesi)", "REN21 (Göğüs Bağlantısı)", "REN22 (Boğaz Merkezi)", "REN23 (Boğaz Tepesi)", "REN24 (Dudak Merkezi)"],
    "Extra Points": ["Yintang (Üçüncü Göz)", "Taiyang (Şakaklar)", "EX-HN1 (Baihui - Yüz Toplantısı)", "EX-HN3 (Shanglianquan - Üst Lianquan)", "EX-HN5 (Yiming - Parlayan Işık)", "EX-HN6 (Anmian - Huzurlu Uyku)", "EX-HN7 (Yintang - Üçüncü Göz)", "EX-HN8 (Shenmen - Ruhun Kapısı)", "EX-HN9 (Erjian - Kulak Ucu)"]
};


const akupunkturCombinations = {
    "2'li Kombinasyonlar": [
        "LI4 + LR3 (Dört Kapı): Qi ve kan dolaşımını düzenler, ağrı ve spazmları hafifletir.",
        "ST36 + SP6 (Genel Tonifikasyon): Enerji artırır, sindirim ve bağışıklık sistemini destekler.",
        "PC6 + SP4 (Chong Mai / Mide Problemleri): Mide bulantısı ve hazımsızlığı hafifletir."
    ],
    "3'lü Kombinasyonlar": [
        "LI4 + LI11 + ST36 (Yang Enerjisi): Yang enerjisini artırır, bağışıklık sistemini güçlendirir.",
        "SP6 + KI3 + LR3 (Yin Enerjisi): Yin enerjisini destekler, hormonal dengeyi iyileştirir.",
        "GB20 + LI4 + LR3 (Baş Ağrısı): Baş ağrısını hafifletir, stres ve gerginliği azaltır."
    ],
    "4'lü Kombinasyonlar": [
        "LI4 + LR3 + SP6 + ST36 (Dört Çiçek): Qi ve kan dolaşımını düzenler, genel sağlık ve denge sağlar.",
        "GB20 + LI4 + LR3 + ST36 (Genel Sağlık): Genel sağlık ve enerji seviyelerini artırır.",
        "PC6 + SP4 + ST36 + LI11 (Sindirim): Sindirim sistemi problemlerini hafifletir, mide bulantısını azaltır."
    ],
    "Yuan-Luo Kombinasyonları": [
        "LU9 + LI6 (Yuan-Luo Kombinasyonu): Akciğer ve kalın bağırsak meridyenlerini dengeler, ödem ve şişkinliği azaltır.",
        "SP3 + ST40 (Yuan-Luo Kombinasyonu): Dalak ve mide meridyenlerini dengeler, balgam ve nem sorunlarını giderir.",
        "HT7 + SI7 (Yuan-Luo Kombinasyonu): Kalp ve ince bağırsak meridyenlerini dengeler, ruhsal denge ve sakinlik sağlar.",
        "KD3 + BL58 (Yuan-Luo Kombinasyonu): Böbrek ve mesane meridyenlerini dengeler, alt sırt ağrısını hafifletir.",
        "PC7 + SJ5 (Yuan-Luo Kombinasyonu): Perikard ve üçlü ısıtıcı meridyenlerini dengeler, göğüs ağrısı ve şişkinliği giderir.",
        "LR3 + GB37 (Yuan-Luo Kombinasyonu): Karaciğer ve safra kesesi meridyenlerini dengeler, göz problemleri ve baş ağrısını hafifletir."
    ],
    "Efsane Kombinasyonlar": [
        "LI4 + ST44 + LI11 + ST36 (Dört Atlılar Kombinasyonu): Ateş, iltihap ve enfeksiyonları azaltır.",
        "SP6 + KI3 + LR3 + GB34 (Beş Element Kombinasyonu): Beş element teorisine göre vücuttaki dengeyi sağlar.",
        "LU7 + KI6 + SP6 + ST36 (Sekiz Asil Kombinasyonu): Enerji, uyku ve genel sağlığı iyileştirir.",
        "GV20 + CV6 + ST36 + SP6 (Dört Asil Nokta): Enerji artırır, genel sağlığı ve dayanıklılığı iyileştirir.",
        "BL23 + KI3 + BL40 + GV4 (Böbrek Yangını Destekleme): Böbrek yangını destekler, alt sırt ağrısını hafifletir.",
        "CV12 + ST36 + SP6 + LI10 (Sindirim Sağlığı): Sindirim problemlerini giderir, mide ve bağırsak sağlığını iyileştirir."
    ]
};


let currentHastaId; // Global değişken olarak currentHastaId tanımlandı.

// Bölüm gösterme fonksiyonu
function showSection(sectionId) {
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.remove('active');
        section.style.display = 'none';
    });

    const activeSection = document.getElementById(sectionId);
    if (activeSection) {
        activeSection.classList.add('active');
        activeSection.style.display = 'block';
    }
}

// Akupunktur Noktası Seçim Fonksiyonları
function showPoints(meridian) {
    const modal = document.getElementById('pointModal');
    const modalSelect = document.getElementById('modal-akupunktur-noktalari');
    modalSelect.innerHTML = '<option value="">Nokta Seçin</option>';

    if (meridian && akupunkturNoktalari[meridian]) {
        akupunkturNoktalari[meridian].forEach(nokta => {
            const option = document.createElement('option');
            option.value = nokta;
            option.textContent = nokta;
            modalSelect.appendChild(option);
        });
    }

    modal.style.display = 'block';
}

function closeModal() {
    const modal = document.getElementById('pointModal');
    modal.style.display = 'none';
}

function ekleAkupunkturNoktasi() {
    const modalSelect = document.getElementById('modal-akupunktur-noktalari');
    const selectedNokta = modalSelect.value;
    const islemTextarea = document.getElementById('islem');

    if (selectedNokta) {
        const currentIslem = islemTextarea.value;
        islemTextarea.value = currentIslem + (currentIslem ? '\n' : '') + selectedNokta;
    }

    closeModal();
}

// Kombinasyon Seçim Fonksiyonları
function showCombinations(type) {
    const modal = document.getElementById('combinationModal');
    const modalSelect = document.getElementById('modal-kombinasyonlar');
    modalSelect.innerHTML = '<option value="">Kombinasyon Seçin</option>';

    if (type && akupunkturCombinations[type]) {
        akupunkturCombinations[type].forEach(kombinasyon => {
            const option = document.createElement('option');
            option.value = kombinasyon;
            option.textContent = kombinasyon;
            modalSelect.appendChild(option);
        });
    }

    modal.style.display = 'block';
}

function closeCombinationModal() {
    const modal = document.getElementById('combinationModal');
    modal.style.display = 'none';
}

function ekleKombinasyon() {
    const modalSelect = document.getElementById('modal-kombinasyonlar');
    const selectedKombinasyon = modalSelect.value;
    const islemTextarea = document.getElementById('islem');

    if (selectedKombinasyon) {
        const currentIslem = islemTextarea.value;
        islemTextarea.value = currentIslem + (currentIslem ? '\n' : '') + selectedKombinasyon;
    }

    closeCombinationModal();
}

// Form sıfırlama fonksiyonu
function resetForm() {
    document.getElementById('seans-form').reset();
    document.getElementById('selected-akupunktur-noktalari').innerHTML = '';
    document.getElementById('selected-kombinasyonlar').innerHTML = '';
}

// Hasta dosyası yükleme fonksiyonu
function fetchHastaDosyasi(hastaId) {
    console.log('Hasta ID:', hastaId);

    if (!hastaId) {
        console.error("Geçersiz Hasta ID.");
        return;
    }

    fetch(`/api/hasta-dosyasi/${hastaId}`)
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => {
                    console.error(`Error: ${response.status} - ${text}`);
                    throw new Error('Invalid response from server');
                });
            }
            return response.json();
        })
        .then(data => {
            console.log("API yanıtı:", data);

            document.getElementById('hasta-ad').value = data.ad || '';
            document.getElementById('hasta-soyad').value = data.soyad || '';
            document.getElementById('hasta-yas').value = data.yas || '';
            document.getElementById('hasta-tc').value = data.tc || '';
            document.getElementById('hasta-meslek').value = data.meslek || '';
            document.getElementById('hasta-evli').checked = data.evli || false;
            document.getElementById('hasta-cocuk_sayisi').value = data.cocuk_sayisi || '';
            document.getElementById('hasta-cinsiyet').value = data.cinsiyet || '';
            document.getElementById('hasta-telefon').value = data.telefon || '';
            document.getElementById('hasta-email').value = data.email || '';
            document.getElementById('hasta-adres').value = data.adres || '';
            document.getElementById('hasta-ana_sikayet').value = data.ana_sikayet || '';
            document.getElementById('notlar-dusunceler-alani').value = data.notlar_dusunceler || '';

            const gecmisSeanslar = document.getElementById('gecmis-seanslar');
            gecmisSeanslar.innerHTML = '';
            if (data.gecmis_seanslar && data.gecmis_seanslar.length > 0) {
                data.gecmis_seanslar.forEach(seans => {
                    const li = document.createElement('li');
                    li.innerHTML = `<b>Tarih:</b> ${seans.tarih} <b>Saat:</b> ${seans.saat} <b>İşlem:</b> ${seans.islem}<br>`;
                    gecmisSeanslar.appendChild(li);
                });
            } else {
                gecmisSeanslar.innerHTML = '<li>Geçmiş seans bulunamadı.</li>';
            }

            const gelecekSeanslar = document.getElementById('gelecek-seanslar');
            gelecekSeanslar.innerHTML = '';
            if (data.gelecek_seanslar && data.gelecek_seanslar.length > 0) {
                data.gelecek_seanslar.forEach(seans => {
                    const li = document.createElement('li');
                    li.innerHTML = `<b>Tarih:</b> ${seans.tarih} <b>Saat:</b> ${seans.saat} <b>İşlem:</b> ${seans.islem}<br>`;
                    gelecekSeanslar.appendChild(li);
                });
            } else {
                gelecekSeanslar.innerHTML = '<li>Gelecek seans bulunamadı.</li>';
            }

            const diyetListesi = document.getElementById('diyet-listesi');
            diyetListesi.innerHTML = '';
            if (data.diyetler && data.diyetler.length > 0) {
                data.diyetler.forEach(diyet => {
                    const li = document.createElement('li');
                    li.textContent = diyet;
                    diyetListesi.appendChild(li);
                });
            } else {
                diyetListesi.innerHTML = '<li>Diyet bulunamadı.</li>';
            }

            const anketListesi = document.getElementById('anket-listesi');
            anketListesi.innerHTML = '';
            if (data.anketler && data.anketler.length > 0) {
                data.anketler.forEach(anket => {
                    const li = document.createElement('li');
                    li.textContent = anket;
                    anketListesi.appendChild(li);
                });
            } else {
                anketListesi.innerHTML = '<li>Anket bulunamadı.</li>';
            }
        })
        .catch(error => {
            console.error('Fetch işlemi sırasında bir hata oluştu:', error);
            alert('Hasta dosyası getirilirken bir hata oluştu. Lütfen tekrar deneyin.');
        });
}

// Hasta listesi yükleme fonksiyonu
function fetchHastaListesi() {
    fetch('/api/hastalar')
        .then(response => response.json())
        .then(data => {
            const hastaListesi = document.getElementById('hasta-listesi');
            hastaListesi.innerHTML = '';
            data.forEach(hasta => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${hasta.id}</td>
                    <td>${hasta.ad}</td>
                    <td>${hasta.soyad}</td>
                    <td>${hasta.yas}</td>
                    <td>${hasta.tc}</td>
                    <td>${hasta.meslek}</td>
                    <td>${hasta.evli ? 'Evet' : 'Hayır'}</td>
                    <td>${hasta.cocuk_sayisi}</td>
                    <td>${hasta.cinsiyet}</td>
                    <td>${hasta.telefon}</td>
                    <td>${hasta.email}</td>
                    <td>${hasta.adres}</td>
                    <td>${hasta.ana_sikayet}</td>
                    <td>${hasta.toplam_seans}</td>
                `;
                row.addEventListener('click', function () {
                    currentHastaId = hasta.id;
                    fetchHastaDosyasi(hasta.id);
                    showSection('hasta-dosyasi');
                });
                hastaListesi.appendChild(row);
            });
        })
        .catch(error => console.error('Error:', error));
}

// Hasta dosyası ID ile arama fonksiyonu
function fetchHastaDosyasiById() {
    const hastaId = document.getElementById('hasta-id-ara').value;
    fetchHastaDosyasi(hastaId);
}

// Hasta seçim listesi yükleme fonksiyonları
function fetchHastaSecimListesi() {
    fetch('/api/hastalar')
        .then(response => response.json())
        .then(data => {
            const hastaSecimListesi = document.getElementById('hasta-secimi');
            hastaSecimListesi.innerHTML = '<option value="">Hasta Seçin</option>';
            data.forEach(hasta => {
                const option = document.createElement('option');
                option.value = hasta.id;
                option.textContent = `${hasta.id} - ${hasta.ad} ${hasta.soyad}`;
                hastaSecimListesi.appendChild(option);
            });
        })
        .catch(error => console.error('Error:', error));
}

function fetchHastaSecimListesiDiyet() {
    fetch('/api/hastalar')
        .then(response => response.json())
        .then(data => {
            const hastaSecimListesi = document.getElementById('hasta-secimi-diyet');
            hastaSecimListesi.innerHTML = '<option value="">Hasta Seçin</option>';
            data.forEach(hasta => {
                const option = document.createElement('option');
                option.value = hasta.id;
                option.textContent = `${hasta.id} - ${hasta.ad} ${hasta.soyad}`;
                hastaSecimListesi.appendChild(option);
            });
        })
        .catch(error => console.error('Error:', error));
}

// Hasta dosyasını indir fonksiyonu
function indirHastaDosyasi() {
    const hastaId = document.getElementById('hasta-id-ara').value;
    window.open(`/api/hasta-dosyasi/indir/${hastaId}`, '_blank');
}

// Hasta dosyasını yazdır fonksiyonu
function yazdirHastaDosyasi() {
    window.print();
}

// Document Ready - Tüm içerik yüklendiğinde çalışacak
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('nav ul li a').forEach(navItem => {
        navItem.addEventListener('click', function (e) {
            e.preventDefault();
            showSection(this.getAttribute('href').substring(1));
        });
    });

    document.getElementById('hasta-form').addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = {
            ad: document.getElementById('ad').value,
            soyad: document.getElementById('soyad').value,
            yas: document.getElementById('yas').value,
            tc: document.getElementById('tc').value,
            meslek: document.getElementById('meslek').value,
            evli: document.getElementById('evli').checked,
            cocuk_sayisi: document.getElementById('cocuk_sayisi').value,
            cinsiyet: document.getElementById('cinsiyet').value,
            telefon: document.getElementById('telefon').value,
            email: document.getElementById('email').value,
            adres: document.getElementById('adres').value,
            ana_sikayet: document.getElementById('ana_sikayet').value
        };

        fetch('/api/hastalar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message + " Hasta ID: " + data.hasta_id);
            document.getElementById('hasta-form').reset();
            fetchHastaListesi();
        })
        .catch(error => console.error('Error:', error));
    });

    document.getElementById('seans-form').addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = {
            hasta_id: document.getElementById('hasta-secimi').value,
            tarih: document.getElementById('tarih').value,
            saat: document.getElementById('saat').value,
            islem: document.getElementById('islem').value
        };

        fetch('/api/seanslar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            document.getElementById('seans-form').reset();
            fetchHastaDosyasi(currentHastaId);
        })
        .catch(error => console.error('Error:', error));
    });

    document.getElementById('diyet-form').addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = {
            hasta_id: document.getElementById('hasta-secimi-diyet').value,
            diyet: document.getElementById('diyet').value
        };

        fetch('/api/diyetler', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            document.getElementById('diyet-form').reset();
            fetchHastaDosyasi(currentHastaId);
        })
        .catch(error => console.error('Error:', error));
    });

    // Sayfa yüklendiğinde başlangıçta tüm listeleri doldurma
    fetchHastaListesi();
    fetchHastaSecimListesi();
    fetchHastaSecimListesiDiyet();
});

