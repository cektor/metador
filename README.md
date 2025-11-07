# Metador - Metadata Cleaner

![Metador Logo](metadorlo.png)

**Metador** is a modern GTK4/Libadwaita application that securely cleans, edits, and manages sensitive metadata from your files.

## 📋 Table of Contents

- [Features](#features)
- [Supported File Formats](#supported-file-formats)
- [Installation](#installation)
- [Usage](#usage)
- [System Requirements](#system-requirements)
- [Developer Information](#developer-information)
- [License](#license)

## ✨ Features

### 🔒 Security and Privacy
- **Sensitive Metadata Cleaning**: Safely removes personal data like GPS location, camera model, shooting date
- **Backup System**: Automatically creates backups during cleaning process
- **Secure Deletion**: Permanently removes metadata

### 🎨 Modern Interface
- **GTK4 & Libadwaita**: Modern and user-friendly interface
- **Dark/Light Theme**: Eye-friendly theme options
- **Responsive Design**: Adapts to different screen sizes
- **Drag & Drop Support**: Easily drag and drop files

### 📁 File Management
- **Multi-file Support**: Process multiple files simultaneously
- **File Preview**: Preview for image, video, and PDF files
- **Navigation**: Easy navigation between files
- **Batch Processing**: Bulk metadata cleaning

### 🔧 Advanced Features
- **Metadata Editing**: View and edit metadata values
- **Categorized View**: Organized view in categories like EXIF, XMP, IPTC, GPS
- **Search and Filter**: Search within metadata
- **Export**: Export metadata information in JSON format

### 🌍 Multi-language Support
- **Turkish**: Full Turkish language support
- **English**: Full English language support
- **Dynamic Language Switching**: Change language without restarting the application

## 📂 Supported File Formats

### 🖼️ Image Files
- **Standard Formats**: JPG, JPEG, PNG, TIFF, TIF, BMP, GIF, WebP
- **RAW Formats**: CR2, CR3, NEF, ARW, DNG, ORF, RW2, PEF, SRW
- **Next Generation**: HEIC, HEIF

### 🎬 Video Files
- **Popular Formats**: MP4, AVI, MOV, MKV, WMV, FLV, WebM, M4V
- **Thumbnail Support**: Automatic thumbnail generation for video files

### 🎵 Audio Files
- **High-Quality Formats**: MP3, FLAC, WAV, OGG, AAC, M4A, WMA
- **ID3 Tag Support**: Manages ID3 tags in audio files

### 📄 Document Files
- **Office Documents**: PDF, DOCX, DOC, XLSX, XLS, PPTX, PPT
- **Metadata Management**: Cleans document properties and metadata

## 🚀 Installation

### Installation via System Package Manager

#### Debian/Ubuntu Based Systems
```bash
# Install required dependencies
sudo apt update
sudo apt install python3 python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adwaita-1 libexif-tools exiftool

# Download and install Metador
git clone https://github.com/cektor/metador.git
cd metador
sudo make install
```

#### Fedora/RHEL Based Systems
```bash
# Install required dependencies
sudo dnf install python3 python3-gobject gtk4-devel libadwaita-devel perl-Image-ExifTool

# Download and install Metador
git clone https://github.com/cektor/metador.git
cd metador
sudo make install
```

#### Arch Linux
```bash
# Install required dependencies
sudo pacman -S python python-gobject gtk4 libadwaita perl-image-exiftool

# Download and install Metador
git clone https://github.com/cektor/metador.git
cd metador
sudo make install
```

### Manual Installation

1. **Check Dependencies**:
   ```bash
   python3 --version  # Python 3.8+
   exiftool -ver      # ExifTool
   ```

2. **Download Source Code**:
   ```bash
   git clone https://github.com/cektor/metador.git
   cd metador
   ```

3. **Run Application**:
   ```bash
   python3 metador.py
   ```

## 📖 Usage

### Basic Usage

1. **Opening Files**:
   - Click the "Open" button or drag and drop files
   - You can select multiple files

2. **Viewing Metadata**:
   - After loading files, metadata information is displayed categorized
   - File preview on the left panel, metadata information on the right panel

3. **Cleaning Metadata**:
   - Click the "Clean Metadata" button
   - Select "Clean" option in the confirmation dialog
   - Success message is displayed when the process is completed

### Advanced Features

#### Metadata Editing
- Click the "Edit" button next to any metadata value
- Enter the new value and click the "Save" button
- Changes are automatically saved

#### Multi-file Processing
- Select multiple files
- Navigate between files using navigation buttons
- Perform batch cleaning operations

#### Theme Switching
- Click the sun/moon icon in the header bar
- Your theme preference is automatically saved

#### Language Switching
- Click the language button in the header bar
- Select Turkish or English
- Application reloads instantly

### Keyboard Shortcuts

| Shortcut | Function |
|----------|----------|
| `Ctrl+O` | Open File |
| `Ctrl+S` | Save Changes |
| `Ctrl+Z` | Undo |
| `F1` | About |
| `Escape` | Close Dialog |

## 🔧 System Requirements

### Minimum Requirements
- **Operating System**: Linux (with GTK4 support)
- **Python**: 3.8 or higher
- **GTK**: 4.0 or higher
- **Libadwaita**: 1.0 or higher
- **ExifTool**: Any version
- **RAM**: 512 MB
- **Disk Space**: 50 MB

### Recommended Requirements
- **RAM**: 1 GB or higher
- **Processor**: Dual-core
- **Disk Space**: 100 MB
- **Screen Resolution**: 1024x768 or higher

### Tested Systems
- ✅ Ubuntu 22.04 LTS
- ✅ Fedora 38
- ✅ Arch Linux
- ✅ Debian 12
- ✅ openSUSE Tumbleweed
- ✅ Pardus 23

## 🛠️ Development

### Development Environment Setup

```bash
# Clone the repository
git clone https://github.com/cektor/metador.git
cd metador

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt

# Run application in development mode
python3 metador.py
```

### Project Structure

```
metador/
├── metador.py              # Main application file
├── language_manager.py     # Language management
├── languages/              # Language files
│   ├── turkish.ini
│   └── english.ini
├── style.css              # CSS styles
├── metadorlo.png          # Application icon
├── requirements.txt       # Python dependencies
├── Makefile              # Installation script
└── README.md             # This file
```

### Contributing

1. Fork the project
2. Create a new branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push your branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 🐛 Bug Reporting

When you find a bug or have suggestions:

1. Visit [GitHub Issues](https://github.com/cektor/metador/issues) page
2. Create a new issue
3. Describe the bug in detail
4. Include your system information

### Log Files

Check log files in case of errors:
- **Location**: `~/.local/share/metador/metador.log`
- **Terminal Output**: Run the application from terminal

## 🔒 Security

### Privacy Policy
- Metador does not send any data over the internet
- All operations are performed locally
- No user data is collected or stored

### Security Features
- Automatic backup system
- Secure metadata deletion
- File integrity protection
- Rollback in case of errors

## 📜 License

This project is distributed under the **GNU General Public License v3.0**.

```
Metador - Metadata Cleaner
Copyright (C) 2024 Fatih ÖNDER (CekToR)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```

## 👨💻 Developer

**Fatih ÖNDER (CekToR)**
- 🌐 Website: [https://github.com/cektor](https://github.com/cektor)
- 📧 Email: [fatih@onder.web.tr](mailto:fatih@onder.web.tr)
- 🐙 GitHub: [@cektor](https://github.com/cektor)

## 🙏 Acknowledgments

- **ExifTool**: Powerful metadata tool developed by Phil Harvey
- **GTK Team**: Modern and beautiful interface framework
- **GNOME Team**: Libadwaita library
- **Python Community**: Powerful programming language
- **Open Source Community**: Free software community

## 🎯 Future Plans

- [ ] Support for more file formats
- [ ] Metadata templates
- [ ] Batch processing improvements
- [ ] Plugin system
- [ ] Command line interface
- [ ] Flatpak package
- [ ] Snap package
- [ ] AppImage support

---

**Protect your file privacy with Metador! 🛡️**