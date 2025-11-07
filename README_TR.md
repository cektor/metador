# Metador - Metadata Temizleyici

![Metador Logo](metadorlo.png)

**Metador**, dosyalarınızdaki hassas metadata verilerini güvenli bir şekilde temizleyen, düzenleyen ve yöneten modern bir GTK4/Libadwaita uygulamasıdır.

## 📋 İçindekiler

- [Özellikler](#özellikler)
- [Desteklenen Dosya Formatları](#desteklenen-dosya-formatları)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Sistem Gereksinimleri](#sistem-gereksinimleri)
- [Geliştirici Bilgileri](#geliştirici-bilgileri)
- [Lisans](#lisans)

## ✨ Özellikler

### 🔒 Güvenlik ve Gizlilik
- **Hassas Metadata Temizleme**: GPS konum bilgileri, kamera modeli, çekim tarihi gibi kişisel verileri güvenli şekilde kaldırır
- **Yedekleme Sistemi**: Temizleme işlemi sırasında otomatik yedek oluşturur
- **Güvenli Silme**: Metadata'yı kalıcı olarak kaldırır

### 🎨 Modern Arayüz
- **GTK4 & Libadwaita**: Modern ve kullanıcı dostu arayüz
- **Karanlık/Aydınlık Tema**: Göz yorgunluğunu azaltan tema seçenekleri
- **Duyarlı Tasarım**: Farklı ekran boyutlarına uyumlu
- **Sürükle-Bırak Desteği**: Dosyaları kolayca sürükleyip bırakabilirsiniz

### 📁 Dosya Yönetimi
- **Çoklu Dosya Desteği**: Birden fazla dosyayı aynı anda işleyebilir
- **Dosya Önizleme**: Resim, video ve PDF dosyaları için önizleme
- **Navigasyon**: Dosyalar arasında kolayca geçiş yapabilirsiniz
- **Batch İşleme**: Toplu metadata temizleme

### 🔧 Gelişmiş Özellikler
- **Metadata Düzenleme**: Metadata değerlerini görüntüleyebilir ve düzenleyebilirsiniz
- **Kategorize Görünüm**: EXIF, XMP, IPTC, GPS gibi kategorilerde organize edilmiş görünüm
- **Arama ve Filtreleme**: Metadata içinde arama yapabilirsiniz
- **Dışa Aktarma**: Metadata bilgilerini JSON formatında dışa aktarabilirsiniz

### 🌍 Çok Dilli Destek
- **Türkçe**: Tam Türkçe dil desteği
- **İngilizce**: Tam İngilizce dil desteği
- **Dinamik Dil Değiştirme**: Uygulama yeniden başlatılmadan dil değiştirilebilir

## 📂 Desteklenen Dosya Formatları

### 🖼️ Resim Dosyaları
- **Standart Formatlar**: JPG, JPEG, PNG, TIFF, TIF, BMP, GIF, WebP
- **RAW Formatlar**: CR2, CR3, NEF, ARW, DNG, ORF, RW2, PEF, SRW
- **Yeni Nesil**: HEIC, HEIF

### 🎬 Video Dosyaları
- **Popüler Formatlar**: MP4, AVI, MOV, MKV, WMV, FLV, WebM, M4V
- **Thumbnail Desteği**: Video dosyaları için otomatik thumbnail oluşturma

### 🎵 Ses Dosyaları
- **Kaliteli Formatlar**: MP3, FLAC, WAV, OGG, AAC, M4A, WMA
- **ID3 Tag Desteği**: Ses dosyalarındaki ID3 etiketlerini yönetir

### 📄 Belge Dosyaları
- **Office Belgeleri**: PDF, DOCX, DOC, XLSX, XLS, PPTX, PPT
- **Metadata Yönetimi**: Belge özelliklerini ve metadata'sını temizler

## 🚀 Kurulum

### Sistem Paket Yöneticisi ile Kurulum

#### Debian/Ubuntu Tabanlı Sistemler
```bash
# Gerekli bağımlılıkları yükleyin
sudo apt update
sudo apt install python3 python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adwaita-1 libexif-tools exiftool

# Metador'u indirin ve kurun
git clone https://github.com/cektor/metador.git
cd metador
sudo make install
```

#### Fedora/RHEL Tabanlı Sistemler
```bash
# Gerekli bağımlılıkları yükleyin
sudo dnf install python3 python3-gobject gtk4-devel libadwaita-devel perl-Image-ExifTool

# Metador'u indirin ve kurun
git clone https://github.com/cektor/metador.git
cd metador
sudo make install
```

#### Arch Linux
```bash
# Gerekli bağımlılıkları yükleyin
sudo pacman -S python python-gobject gtk4 libadwaita perl-image-exiftool

# Metador'u indirin ve kurun
git clone https://github.com/cektor/metador.git
cd metador
sudo make install
```

### Manuel Kurulum

1. **Bağımlılıkları Kontrol Edin**:
   ```bash
   python3 --version  # Python 3.8+
   exiftool -ver      # ExifTool
   ```

2. **Kaynak Kodunu İndirin**:
   ```bash
   git clone https://github.com/cektor/metador.git
   cd metador
   ```

3. **Uygulamayı Çalıştırın**:
   ```bash
   python3 metador.py
   ```

## 📖 Kullanım

### Temel Kullanım

1. **Dosya Açma**:
   - "Aç" butonuna tıklayın veya dosyaları sürükleyip bırakın
   - Birden fazla dosya seçebilirsiniz

2. **Metadata Görüntüleme**:
   - Dosya yüklendikten sonra metadata bilgileri kategorilere ayrılmış şekilde görüntülenir
   - Sol panelde dosya önizlemesi, sağ panelde metadata bilgileri yer alır

3. **Metadata Temizleme**:
   - "Metadata Temizle" butonuna tıklayın
   - Onay dialogunda "Temizle" seçeneğini seçin
   - İşlem tamamlandığında başarı mesajı görüntülenir

### Gelişmiş Özellikler

#### Metadata Düzenleme
- Herhangi bir metadata değerinin yanındaki "Düzenle" butonuna tıklayın
- Yeni değeri girin ve "Kaydet" butonuna tıklayın
- Değişiklikler otomatik olarak kaydedilir

#### Çoklu Dosya İşleme
- Birden fazla dosya seçin
- Navigasyon butonları ile dosyalar arasında geçiş yapın
- Toplu temizleme işlemi gerçekleştirin

#### Tema Değiştirme
- Header bar'daki güneş/ay ikonuna tıklayın
- Tema tercihiniz otomatik olarak kaydedilir

#### Dil Değiştirme
- Header bar'daki dil butonuna tıklayın
- Türkçe veya İngilizce seçin
- Uygulama anında yeniden yüklenir

### Klavye Kısayolları

| Kısayol | Fonksiyon |
|---------|-----------|
| `Ctrl+O` | Dosya Aç |
| `Ctrl+S` | Değişiklikleri Kaydet |
| `Ctrl+Z` | Geri Al |
| `F1` | Hakkında |
| `Escape` | Dialog Kapat |

## 🔧 Sistem Gereksinimleri

### Minimum Gereksinimler
- **İşletim Sistemi**: Linux (GTK4 desteği olan)
- **Python**: 3.8 veya üzeri
- **GTK**: 4.0 veya üzeri
- **Libadwaita**: 1.0 veya üzeri
- **ExifTool**: Herhangi bir sürüm
- **RAM**: 512 MB
- **Disk Alanı**: 50 MB

### Önerilen Gereksinimler
- **RAM**: 1 GB veya üzeri
- **İşlemci**: Çift çekirdekli
- **Disk Alanı**: 100 MB
- **Ekran Çözünürlüğü**: 1024x768 veya üzeri

### Test Edilen Sistemler
- ✅ Ubuntu 22.04 LTS
- ✅ Fedora 38
- ✅ Arch Linux
- ✅ Debian 12
- ✅ openSUSE Tumbleweed
- ✅ Pardus 23

## 🛠️ Geliştirme

### Geliştirme Ortamı Kurulumu

```bash
# Depoyu klonlayın
git clone https://github.com/cektor/metador.git
cd metador

# Sanal ortam oluşturun
python3 -m venv venv
source venv/bin/activate

# Geliştirme bağımlılıklarını yükleyin
pip install -r requirements.txt

# Uygulamayı geliştirme modunda çalıştırın
python3 metador.py
```

### Proje Yapısı

```
metador/
├── metador.py              # Ana uygulama dosyası
├── language_manager.py     # Dil yönetimi
├── languages/              # Dil dosyaları
│   ├── turkish.ini
│   └── english.ini
├── style.css              # CSS stilleri
├── metadorlo.png          # Uygulama ikonu
├── requirements.txt       # Python bağımlılıkları
├── Makefile              # Kurulum scripti
└── README.md             # Bu dosya
```

### Katkıda Bulunma

1. Projeyi fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/yeni-ozellik`)
5. Pull Request oluşturun

## 🐛 Hata Bildirimi

Hata bulduğunuzda veya öneriniz olduğunda:

1. [GitHub Issues](https://github.com/cektor/metador/issues) sayfasını ziyaret edin
2. Yeni bir issue oluşturun
3. Hatayı detaylı şekilde açıklayın
4. Sistem bilgilerinizi ekleyin

### Log Dosyaları

Hata durumunda log dosyalarını kontrol edin:
- **Konum**: `~/.local/share/metador/metador.log`
- **Terminal Çıktısı**: Uygulamayı terminal'den çalıştırın

## 🔒 Güvenlik

### Gizlilik Politikası
- Metador hiçbir veriyi internet üzerinden göndermez
- Tüm işlemler yerel olarak gerçekleştirilir
- Kullanıcı verileri toplanmaz veya saklanmaz

### Güvenlik Özellikleri
- Otomatik yedekleme sistemi
- Güvenli metadata silme
- Dosya bütünlüğü koruması
- Hata durumunda geri alma

## 📜 Lisans

Bu proje **GNU General Public License v3.0** lisansı altında dağıtılmaktadır.

```
Metador - Metadata Temizleyici
Copyright (C) 2024 Fatih ÖNDER (CekToR)

Bu program özgür yazılımdır: Free Software Foundation tarafından yayımlanan
GNU Genel Kamu Lisansı'nın 3. sürümü veya (tercihinize bağlı olarak) daha
sonraki bir sürümü altında yeniden dağıtabilir ve/veya değiştirebilirsiniz.

Bu program faydalı olacağı umuduyla dağıtılmaktadır, ancak HİÇBİR GARANTİ
VERİLMEMEKTEDİR; hatta SATILABİLİRLİK veya BELİRLİ BİR AMACA UYGUNLUK
için örtük garanti bile verilmemektedir.
```

## 👨‍💻 Geliştirici

**Fatih ÖNDER (CekToR)**
- 🌐 Website: [https://github.com/cektor](https://github.com/cektor)
- 📧 E-posta: [fatih@onder.web.tr](mailto:fatih@onder.web.tr)
- 🐙 GitHub: [@cektor](https://github.com/cektor)

## 🙏 Teşekkürler

- **ExifTool**: Phil Harvey tarafından geliştirilen güçlü metadata aracı
- **GTK Team**: Modern ve güzel arayüz framework'ü
- **GNOME Team**: Libadwaita kütüphanesi
- **Python Community**: Güçlü programlama dili
- **Open Source Community**: Özgür yazılım topluluğu

## 🎯 Gelecek Planları

- [ ] Daha fazla dosya formatı desteği
- [ ] Metadata şablonları
- [ ] Toplu işleme iyileştirmeleri
- [ ] Plugin sistemi
- [ ] Komut satırı arayüzü
- [ ] Flatpak paketi
- [ ] Snap paketi
- [ ] AppImage desteği

---

**Metador ile dosyalarınızın gizliliğini koruyun! 🛡️**