#!/usr/bin/env python3
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gtk, Adw, GLib, Gio, Gdk, GdkPixbuf
import subprocess
import json
import os

# Önce sistem konumunu dene
system_lang_manager = Path('/usr/share/metador/language_manager.py')
if system_lang_manager.exists():
    sys.path.insert(0, '/usr/share/metador')
    from language_manager import LanguageManager
else:
    # Yerel konumdan import et
    from language_manager import LanguageManager

class MetadataCleanerWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lang = LanguageManager()
        self.setup_logging()
        self.set_title(self.lang.get_text('MAIN', 'app_title'))
        
        # Tema ayarlarını yükle
        self.settings_file = Path(GLib.get_user_config_dir()) / "metador" / "settings.json"
        self.load_theme_settings()
        
        # Icon theme'e pixmaps path'ini ekle
        try:
            icon_theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
            icon_theme.add_search_path("/usr/share/pixmaps")
        except:
            pass
        
        # Pencere ikonu ayarla
        try:
            icon_path = Path("/usr/share/pixmaps/metadorlo.png")
            if icon_path.exists():
                # PNG dosyasını doğrudan pixbuf olarak yükle ve pencere ikonuna ata
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(str(icon_path), 48, 48, True)
                self.set_icon(pixbuf)
            else:
                self.set_icon_name("edit-clear-all-symbolic")
        except Exception as e:
            self.set_icon_name("edit-clear-all-symbolic")
        self.set_default_size(800, 600)
        self.add_css_class('main-window')
        
        self.current_files = []
        self.current_file_index = 0
        self.metadata = {}
        self.changed_metadata = {}
        self.about_click_count = 0  # Easter Egg için tıklama sayacı
        
        self.setup_ui()
        self.load_css()
        self.apply_theme()
   
        
        # Dosya handler - kullanıcı dizininde
        log_dir = Path(GLib.get_user_data_dir()) / "metador"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "metador.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        self.logger.info("Metador başlatıldı")
    
    def load_theme_settings(self):
        """Tema ayarlarını yükle"""
        self.current_theme = "light"  # Varsayılan tema
        
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    self.current_theme = settings.get('theme', 'light')
        except Exception as e:
            self.logger.warning(f"Tema ayarları yüklenemedi: {e}")
    
    def save_theme_settings(self):
        """Tema ayarlarını kaydet"""
        try:
            self.settings_file.parent.mkdir(parents=True, exist_ok=True)
            settings = {'theme': self.current_theme}
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f)
        except Exception as e:
            self.logger.error(f"Tema ayarları kaydedilemedi: {e}")
    
    def apply_theme(self):
        """Temayı uygula"""
        style_manager = Adw.StyleManager.get_default()
        if self.current_theme == "dark":
            style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
        else:
            style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
    
    def update_theme_button_icon(self):
        """Tema butonunun ikonunu güncelle"""
        if self.current_theme == "dark":
            self.theme_button.set_icon_name("weather-clear-night-symbolic")
        else:
            self.theme_button.set_icon_name("weather-clear-symbolic")
    
    def on_theme_clicked(self, button):
        """Tema değiştir"""
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.apply_theme()
        self.update_theme_button_icon()
        self.save_theme_settings()
    
    def load_css(self):
        css_provider = Gtk.CssProvider()
        
        # Önce GResource'tan yüklemeyi dene
        try:
            css_provider.load_from_resource("/com/github/metador/style.css")
        except:
            # Sistem konumunu dene
            system_css = Path("/usr/share/metador/style.css")
            if system_css.exists():
                css_provider.load_from_path(str(system_css))
            else:
                # Yerel konumdan yükle
                local_css = Path(__file__).parent / "style.css"
                if local_css.exists():
                    css_provider.load_from_path(str(local_css))
                else:
                    self.logger.warning("CSS dosyası bulunamadı")
                    return
        
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    
    def setup_ui(self):
        # Header Bar
        header = Adw.HeaderBar()
        
        # Sol taraf butonlar
        left_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        
        open_button = Gtk.Button(icon_name="document-open-symbolic")
        open_button.set_tooltip_text(self.lang.get_text('MENU', 'open'))
        open_button.add_css_class("flat")
        open_button.connect("clicked", self.on_open_clicked)
        left_box.append(open_button)
        
        # Language menu
        lang_menu = Gio.Menu()
        lang_menu.append(self.lang.get_text('MENU', 'turkish'), "app.set_language::turkish")
        lang_menu.append(self.lang.get_text('MENU', 'english'), "app.set_language::english")
        
        lang_button = Gtk.MenuButton()
        lang_button.set_icon_name("preferences-desktop-locale-symbolic")
        lang_button.set_tooltip_text(self.lang.get_text('MENU', 'language'))
        lang_button.add_css_class("flat")
        lang_button.set_menu_model(lang_menu)
        left_box.append(lang_button)
        
        # Tema değiştirme butonu
        self.theme_button = Gtk.Button()
        self.update_theme_button_icon()
        self.theme_button.set_tooltip_text(self.lang.get_text('MENU', 'theme_switch'))
        self.theme_button.add_css_class("flat")
        self.theme_button.connect("clicked", self.on_theme_clicked)
        left_box.append(self.theme_button)
        
        # Hakkında butonu
        about_button = Gtk.Button(icon_name="help-about-symbolic")
        about_button.set_tooltip_text(self.lang.get_text('MENU', 'about'))
        about_button.add_css_class("flat")
        about_button.connect("clicked", self.on_about_clicked)
        left_box.append(about_button)
        
        header.pack_start(left_box)
        
        # Sağ taraf butonlar
        right_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        
        # Geri al butonu
        self.undo_button = Gtk.Button()
        undo_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        undo_icon = Gtk.Image.new_from_icon_name("edit-undo-symbolic")
        undo_label = Gtk.Label(label=self.lang.get_text('MAIN', 'undo'))
        undo_box.append(undo_icon)
        undo_box.append(undo_label)
        self.undo_button.set_child(undo_box)
        self.undo_button.add_css_class("flat")
        self.undo_button.set_sensitive(False)
        self.undo_button.connect("clicked", self.on_undo_clicked)
        right_box.append(self.undo_button)
        
        # Kaydet butonu
        self.save_button = Gtk.Button()
        save_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        save_icon = Gtk.Image.new_from_icon_name("document-save-symbolic")
        save_label = Gtk.Label(label=self.lang.get_text('MAIN', 'save'))
        save_box.append(save_icon)
        save_box.append(save_label)
        self.save_button.set_child(save_box)
        self.save_button.add_css_class("flat")
        self.save_button.set_sensitive(False)
        self.save_button.connect("clicked", self.on_save_clicked)
        right_box.append(self.save_button)
        
        # Temizle butonu
        self.clean_button = Gtk.Button()
        clean_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        clean_icon = Gtk.Image.new_from_icon_name("edit-clear-all-symbolic")
        clean_label = Gtk.Label(label=self.lang.get_text('MAIN', 'clean_metadata'))
        clean_box.append(clean_icon)
        clean_box.append(clean_label)
        self.clean_button.set_child(clean_box)
        self.clean_button.add_css_class("suggested-action")
        self.clean_button.set_sensitive(False)
        self.clean_button.connect("clicked", self.on_clean_clicked)
        right_box.append(self.clean_button)
        
        header.pack_end(right_box)
        
        # Main Box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.append(header)
        
        # Content
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        
        # Welcome Page
        welcome_page = self.create_welcome_page()
        self.stack.add_named(welcome_page, "welcome")
        
        # Metadata Page
        metadata_page = self.create_metadata_page()
        self.stack.add_named(metadata_page, "metadata")
        
        main_box.append(self.stack)
        self.set_content(main_box)
        
    def create_welcome_page(self):
        page = Adw.StatusPage()
        page.add_css_class("welcome-page")
        page.set_title(self.lang.get_text('MAIN', 'app_title'))
        page.set_description(self.lang.get_text('MAIN', 'welcome_description'))
        
        # Logo ikonu
        try:
            icon_path = Path("/usr/share/pixmaps/metadorlo.png")
            if icon_path.exists():
                page.set_icon_name("metadorlo")
            else:
                page.set_icon_name("edit-clear-all-symbolic")
        except Exception as e:
            self.logger.warning(f"Logo yüklenemedi: {e}")
            page.set_icon_name("edit-clear-all-symbolic")
        
        # Dosya aç butonu
        open_files_button = Gtk.Button()
        open_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        open_icon = Gtk.Image.new_from_icon_name("document-open-symbolic")
        open_label = Gtk.Label(label=self.lang.get_text('MENU', 'open'))
        open_box.append(open_icon)
        open_box.append(open_label)
        open_files_button.set_child(open_box)
        open_files_button.add_css_class("pill")
        open_files_button.add_css_class("suggested-action")
        open_files_button.connect("clicked", self.on_open_clicked)
        page.set_child(open_files_button)
        
        # Sürükle-bırak desteği
        drop_target = Gtk.DropTarget.new(Gio.File, Gdk.DragAction.COPY)
        drop_target.connect("drop", self.on_file_dropped)
        page.add_controller(drop_target)
        
        return page
    
    def on_file_dropped(self, drop_target, value, x, y):
        """Dosya sürüklenip bırakıldığında çalışır"""
        if isinstance(value, Gio.File):
            file_path = value.get_path()
            
            # Dosya tipi kontrolü
            is_supported, error_msg = self.is_supported_file_type(file_path)
            if not is_supported:
                self.show_error_dialog(
                    "Desteklenmeyen Dosya Tipi",
                    f"{error_msg}\n\nLütfen desteklenen dosya tiplerini seçin."
                )
                return False
            
            self.current_files = [file_path]
            self.current_file_index = 0
            self.load_metadata()
            return True
        return False

    def create_metadata_page(self):
        # Ana paned (yan yana bölüm)
        paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        paned.set_shrink_start_child(False)
        paned.set_shrink_end_child(False)
        paned.set_resize_start_child(False)
        paned.set_resize_end_child(True)
        
        # Sol panel - Fotoğraf önizlemesi ve dosya bilgileri
        left_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        left_panel.set_size_request(350, -1)
        left_panel.set_margin_start(12)
        left_panel.set_margin_end(6)
        left_panel.set_margin_top(12)
        left_panel.set_margin_bottom(12)
        
        # Fotoğraf önizleme kartı
        preview_card = Adw.Clamp()
        preview_card.set_maximum_size(320)
        
        self.preview_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.preview_box.add_css_class("card")
        self.preview_box.set_margin_start(12)
        self.preview_box.set_margin_end(12)
        self.preview_box.set_margin_top(12)
        self.preview_box.set_margin_bottom(12)
        
        # Fotoğraf önizlemesi
        self.image_preview = Gtk.Picture()
        self.image_preview.set_size_request(280, 200)
        self.image_preview.add_css_class("preview-image")
        self.image_preview.set_content_fit(Gtk.ContentFit.CONTAIN)
        self.preview_box.append(self.image_preview)
        
        # Dosya bilgileri
        self.file_info_group = Adw.PreferencesGroup()
        self.file_info_group.set_title("Dosya Bilgileri")
        
        self.file_info_row = Adw.ActionRow()
        
        # Navigasyon butonları
        nav_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        
        self.prev_button = Gtk.Button(icon_name="go-previous-symbolic")
        self.prev_button.add_css_class("flat")
        self.prev_button.set_tooltip_text(self.lang.get_text('MAIN', 'previous_file'))
        self.prev_button.connect("clicked", self.on_prev_file_clicked)
        nav_box.append(self.prev_button)
        
        self.next_button = Gtk.Button(icon_name="go-next-symbolic")
        self.next_button.add_css_class("flat")
        self.next_button.set_tooltip_text(self.lang.get_text('MAIN', 'next_file'))
        self.next_button.connect("clicked", self.on_next_file_clicked)
        nav_box.append(self.next_button)
        
        self.file_info_row.add_suffix(nav_box)
        self.file_info_group.add(self.file_info_row)
        
        self.preview_box.append(self.file_info_group)
        preview_card.set_child(self.preview_box)
        left_panel.append(preview_card)
        
        # Sağ panel - Metadata listesi
        right_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        right_panel.set_margin_start(6)
        right_panel.set_margin_end(12)
        right_panel.set_margin_top(12)
        right_panel.set_margin_bottom(12)
        
        # Metadata başlığı
        metadata_header = Adw.HeaderBar()
        metadata_header.set_title_widget(Gtk.Label(label="Metadata Bilgileri"))
        metadata_header.add_css_class("flat")
        right_panel.append(metadata_header)
        
        # Metadata scrolled window
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        self.metadata_list = Gtk.ListBox()
        self.metadata_list.add_css_class("boxed-list")
        self.metadata_list.set_selection_mode(Gtk.SelectionMode.NONE)
        
        scrolled.set_child(self.metadata_list)
        right_panel.append(scrolled)
        
        # Panelleri ekle
        paned.set_start_child(left_panel)
        paned.set_end_child(right_panel)
        paned.set_position(350)
        
        return paned

    def on_open_clicked(self, button):
        dialog = Gtk.FileChooserDialog(
            title=self.lang.get_text('MAIN', 'select_file'),
            transient_for=self,
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.set_select_multiple(True)
        dialog.add_buttons(
            self.lang.get_text('DIALOGS', 'cancel'), Gtk.ResponseType.CANCEL,
            self.lang.get_text('MENU', 'open'), Gtk.ResponseType.ACCEPT
        )
        
        # Desteklenen dosya türleri
        metadata_filter = Gtk.FileFilter()
        metadata_filter.set_name("Desteklenen Dosyalar")
        
        # Resim dosyaları
        image_exts = ['*.jpg', '*.jpeg', '*.png', '*.tiff', '*.tif', '*.bmp', '*.gif', '*.webp', '*.heic', '*.heif']
        # RAW dosyaları
        raw_exts = ['*.raw', '*.cr2', '*.cr3', '*.nef', '*.arw', '*.dng', '*.orf', '*.rw2', '*.pef', '*.srw']
        # Video dosyaları
        video_exts = ['*.mp4', '*.avi', '*.mov', '*.mkv', '*.wmv', '*.flv', '*.webm', '*.m4v']
        # Ses dosyaları
        audio_exts = ['*.mp3', '*.flac', '*.wav', '*.ogg', '*.aac', '*.m4a', '*.wma']
        # Belge dosyaları
        doc_exts = ['*.pdf', '*.docx', '*.doc', '*.xlsx', '*.xls', '*.pptx', '*.ppt']
        
        all_supported = image_exts + raw_exts + video_exts + audio_exts + doc_exts
        
        for ext in all_supported:
            metadata_filter.add_pattern(ext)
            metadata_filter.add_pattern(ext.upper())
        
        dialog.add_filter(metadata_filter)
        
        # Resim dosyaları filtresi
        image_filter = Gtk.FileFilter()
        image_filter.set_name("Resim Dosyaları")
        for ext in image_exts + raw_exts:
            image_filter.add_pattern(ext)
            image_filter.add_pattern(ext.upper())
        dialog.add_filter(image_filter)
        
        # Video dosyaları filtresi
        video_filter = Gtk.FileFilter()
        video_filter.set_name("Video Dosyaları")
        for ext in video_exts:
            video_filter.add_pattern(ext)
            video_filter.add_pattern(ext.upper())
        dialog.add_filter(video_filter)
        
        # Tüm dosyalar filtresi
        all_filter = Gtk.FileFilter()
        all_filter.set_name("Tüm Dosyalar")
        all_filter.add_pattern("*")
        dialog.add_filter(all_filter)
        
        dialog.connect("response", self.on_file_dialog_response)
        dialog.show()
    
    def on_file_dialog_response(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            files = dialog.get_files()
            if files:
                self.current_files = [f.get_path() for f in files]
                self.current_file_index = 0
                self.load_metadata()
        dialog.destroy()
    
    def is_supported_file_type(self, file_path):
        """Dosya tipinin metadata temizleme için desteklenip desteklenmediğini kontrol eder"""
        unsupported_extensions = {'.lnk', '.url', '.desktop', '.exe', '.dll', '.sys', '.bat', '.cmd'}
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext in unsupported_extensions:
            return False, f"'{file_ext}' dosya tipi metadata temizleme için desteklenmiyor."
        
        # MIME type kontrolü
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type:
            unsupported_mimes = {'application/x-ms-shortcut', 'application/x-msdownload'}
            if mime_type in unsupported_mimes:
                return False, f"'{mime_type}' dosya tipi desteklenmiyor."
        
        return True, None

    def load_metadata(self):
        self.changed_metadata.clear()  # Dosya değiştiğinde değişiklikleri temizle
        
        if not self.current_files or self.current_file_index >= len(self.current_files):
            return
        
        current_file = self.current_files[self.current_file_index]
        
        # Dosya tipi kontrolü
        is_supported, error_msg = self.is_supported_file_type(current_file)
        if not is_supported:
            self.logger.warning(f"Desteklenmeyen dosya tipi: {current_file} - {error_msg}")
            self.show_error_dialog(
                "Desteklenmeyen Dosya Tipi",
                f"{error_msg}\n\nLütfen desteklenen dosya tiplerini seçin:\n• Resim dosyaları (JPG, PNG, TIFF, vb.)\n• Video dosyaları (MP4, AVI, MOV, vb.)\n• Ses dosyaları (MP3, FLAC, WAV, vb.)\n• Belge dosyaları (PDF, DOCX, vb.)"
            )
            return
            
        if not self.check_exiftool():
            self.logger.error("ExifTool bulunamadı")
            self.show_error_dialog(
                self.lang.get_text('DIALOGS', 'error_title'),
                self.lang.get_text('DIALOGS', 'exiftool_not_found')
            )
            return
        
        # UI'yi devre dışı bırak
        self.clean_button.set_sensitive(False)
        
        # Asenkron metadata yükleme
        def load_worker():
            try:
                self.logger.info(f"Metadata yükleniyor: {current_file}")
                
                cmd = [
                    'exiftool',
                    '-json',
                    '-G',
                    '-struct',
                    '-duplicates',
                    '-unknown',
                    '-charset', 'filename=utf8',
                    '-charset', 'utf8',
                    current_file
                ]
                self.logger.debug(f"Çalıştırılan komut: {' '.join(cmd)}")
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                self.logger.debug(f"ExifTool çıktısı: {result.stdout}")
                if result.stderr:
                    self.logger.warning(f"ExifTool uyarıları: {result.stderr}")
                
                data = json.loads(result.stdout)
                
                # Ana thread'e geri dön
                GLib.idle_add(self._on_metadata_loaded, data, None)
                
            except subprocess.CalledProcessError as e:
                error_msg = f"ExifTool hatası: {e.stderr}"
                self.logger.error(error_msg)
                GLib.idle_add(self._on_metadata_loaded, None, error_msg)
                
            except json.JSONDecodeError as e:
                error_msg = f"JSON parse hatası: {str(e)}"
                self.logger.error(error_msg)
                GLib.idle_add(self._on_metadata_loaded, None, error_msg)
                
            except Exception as e:
                error_msg = f"Beklenmeyen hata: {str(e)}"
                self.logger.error(error_msg)
                self.logger.error(traceback.format_exc())
                GLib.idle_add(self._on_metadata_loaded, None, error_msg)
        
        thread = threading.Thread(target=load_worker, daemon=True)
        thread.start()
    
    def _on_metadata_loaded(self, data, error):
        """Metadata yükleme tamamlandığında ana thread'de çalışır"""
        if error:
            self.show_error_dialog(self.lang.get_text('DIALOGS', 'error_title'), error)
            return
        
        if data:
            self.metadata = data[0]
            self.load_image_preview()  # Fotoğraf önizlemesini yükle
            self.organize_metadata()
            self.stack.set_visible_child_name("metadata")
            self.clean_button.set_sensitive(True)
            self.logger.info("Metadata başarıyla yüklendi")
        else:
            self.logger.warning("Metadata bulunamadı")
            self.show_error_dialog(
                self.lang.get_text('DIALOGS', 'error_title'), 
                self.lang.get_text('DIALOGS', 'metadata_read_error')
            )
    
    def load_image_preview(self):
        """Dosya önizlemesini yükle"""
        if not self.current_files:
            return
            
        current_file = self.current_files[self.current_file_index]
        file_ext = Path(current_file).suffix.lower()
        
        # Resim dosyaları
        image_extensions = {'.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp', '.gif', '.webp', '.heic', '.heif'}
        # Video dosyaları
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v'}
        # PDF dosyaları
        pdf_extensions = {'.pdf'}
        
        try:
            if file_ext in image_extensions:
                # Resim dosyası - doğrudan yükle (GIF dahil)
                if file_ext == '.gif':
                    # GIF için animasyon desteği
                    pixbuf_animation = GdkPixbuf.PixbufAnimation.new_from_file(current_file)
                    if pixbuf_animation.is_static_image():
                        # Statik GIF
                        pixbuf = pixbuf_animation.get_static_image()
                        pixbuf = pixbuf.scale_simple(280, 200, GdkPixbuf.InterpType.BILINEAR)
                    else:
                        # Animasyonlu GIF - ilk kareyi al
                        pixbuf = pixbuf_animation.get_static_image()
                        pixbuf = pixbuf.scale_simple(280, 200, GdkPixbuf.InterpType.BILINEAR)
                    texture = Gdk.Texture.new_for_pixbuf(pixbuf)
                else:
                    # Diğer resim formatları
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(current_file, 280, 200, True)
                    texture = Gdk.Texture.new_for_pixbuf(pixbuf)
                
                self.image_preview.set_paintable(texture)
                self.image_preview.set_visible(True)
                
            elif file_ext in video_extensions:
                # Video dosyası - ffmpeg ile thumbnail çıkar
                self.load_video_thumbnail(current_file)
                
            elif file_ext in pdf_extensions:
                # PDF dosyası - poppler ile thumbnail çıkar
                self.load_pdf_thumbnail(current_file)
                
            else:
                # Diğer dosyalar için ikon göster
                self.show_file_icon()
                
        except Exception as e:
            self.logger.warning(f"Dosya önizlemesi yüklenemedi: {e}")
            self.show_file_icon()
    
    def load_video_thumbnail(self, video_file):
        """Video dosyası için thumbnail çıkar"""
        try:
            # ffmpeg ile video thumbnail çıkar
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                thumbnail_path = tmp.name
            
            # ffmpeg komutu
            cmd = [
                'ffmpeg', '-i', video_file,
                '-ss', '00:00:01',  # 1. saniyeden
                '-vframes', '1',     # 1 frame
                '-q:v', '2',         # Yüksek kalite
                '-y',                # Üzerine yaz
                thumbnail_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and os.path.exists(thumbnail_path):
                # Thumbnail'i yükle
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(thumbnail_path, 280, 200, True)
                texture = Gdk.Texture.new_for_pixbuf(pixbuf)
                self.image_preview.set_paintable(texture)
                self.image_preview.set_visible(True)
                
                # Geçici dosyayı sil
                os.unlink(thumbnail_path)
            else:
                self.show_file_icon()
                
        except Exception as e:
            self.logger.warning(f"Video thumbnail oluşturulamadı: {e}")
            self.show_file_icon()
    
    def load_pdf_thumbnail(self, pdf_file):
        """PDF dosyası için thumbnail çıkar"""
        try:
            # pdftoppm ile PDF thumbnail çıkar
            import tempfile
            with tempfile.TemporaryDirectory() as tmp_dir:
                # PDF'in ilk sayfasını PNG'ye çevir
                cmd = [
                    'pdftoppm', '-png',
                    '-f', '1', '-l', '1',  # Sadece ilk sayfa
                    '-scale-to-x', '280',   # Genişlik
                    '-scale-to-y', '200',   # Yükseklik
                    pdf_file,
                    os.path.join(tmp_dir, 'page')
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    # Oluşturulan PNG dosyasını bul
                    png_files = list(Path(tmp_dir).glob('page-*.png'))
                    if png_files:
                        thumbnail_path = str(png_files[0])
                        pixbuf = GdkPixbuf.Pixbuf.new_from_file(thumbnail_path)
                        texture = Gdk.Texture.new_for_pixbuf(pixbuf)
                        self.image_preview.set_paintable(texture)
                        self.image_preview.set_visible(True)
                        return
                        
                self.show_file_icon()
                
        except Exception as e:
            self.logger.warning(f"PDF thumbnail oluşturulamadı: {e}")
            self.show_file_icon()
    
    def show_file_icon(self):
        """Dosyalar için işletim sistemi varsayılan ikonlarını göster"""
        try:
            current_file = self.current_files[self.current_file_index]
            
            # İşletim sisteminin varsayılan ikonunu al
            gfile = Gio.File.new_for_path(current_file)
            file_info = gfile.query_info('standard::icon', Gio.FileQueryInfoFlags.NONE, None)
            
            if file_info:
                icon = file_info.get_icon()
                icon_theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
                
                # İkon lookup
                icon_paintable = icon_theme.lookup_by_gicon(icon, 128, 1, Gtk.TextDirection.NONE, 0)
                
                if icon_paintable:
                    self.image_preview.set_paintable(icon_paintable)
                    self.image_preview.set_visible(True)
                    return
            
            # Fallback - genel dosya ikonu
            icon_theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
            icon_paintable = icon_theme.lookup_icon("text-x-generic", None, 128, 1, Gtk.TextDirection.NONE, 0)
            
            if icon_paintable:
                self.image_preview.set_paintable(icon_paintable)
            else:
                self.image_preview.set_paintable(None)
                
        except Exception as e:
            self.logger.warning(f"Dosya ikonu yüklenemedi: {e}")
            # Son fallback
            try:
                icon_theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
                icon_paintable = icon_theme.lookup_icon("application-x-executable", None, 128, 1, Gtk.TextDirection.NONE, 0)
                if icon_paintable:
                    self.image_preview.set_paintable(icon_paintable)
                else:
                    self.image_preview.set_paintable(None)
            except:
                self.image_preview.set_paintable(None)
            
        self.image_preview.set_visible(True)

    
        # Grupları görüntüle
        self.display_grouped_metadata(grouped_data, groups)

    def display_grouped_metadata(self, grouped_data, groups):
        # Clear existing rows
        while True:
            row = self.metadata_list.get_row_at_index(0)
            if row is None:
                break
            self.metadata_list.remove(row)

        # Dosya bilgilerini güncelle
        current_file = self.current_files[self.current_file_index]
        file_name = os.path.basename(current_file)
        
        # Çoklu dosya durumunda dosya sayısını göster
        if len(self.current_files) > 1:
            title = f"{file_name} ({self.current_file_index + 1}/{len(self.current_files)})"
        else:
            title = file_name
            
        self.file_info_row.set_title(title)
        self.file_info_row.set_subtitle(current_file)
        
        # Dosya ikonu ekle
        file_icon = Gtk.Image.new_from_icon_name("text-x-generic-symbolic")
        self.file_info_row.add_prefix(file_icon)

        # Her grubu görüntüle
        for group_name, items in grouped_data.items():
            if items:
                group_info = groups.get(group_name, {
                    'title': group_name,
                    'icon': 'dialog-information-symbolic'
                })

                # File ve Composite grupları için gizli expander kullan
                if group_name in ['File', 'Composite']:
                    # Adw.ExpanderRow ile gizli grup
                    expander = Adw.ExpanderRow()
                    expander.set_title(group_info['title'])
                    expander.set_expanded(False)  # Başlangıçta kapalı
                    
                    # Grup ikonu ekle
                    group_icon = Gtk.Image.new_from_icon_name(group_info['icon'])
                    expander.add_prefix(group_icon)
                    
                    # Grup içindeki metadata'ları ekle
                    for key, value in sorted(items.items()):
                        if isinstance(value, (list, dict)):
                            value = json.dumps(value, indent=2, ensure_ascii=False)
                        elif isinstance(value, bytes):
                            value = str(value)
                        elif value is None:
                            continue

                        display_value = str(value)
                        if len(display_value) > 100:
                            display_value = display_value[:97] + "..."
                        
                        display_key = key.split(':', 1)[-1].strip()
                        display_key = self.lang.get_text('KEYS', display_key, fallback=display_key)
                        
                        row = Adw.ActionRow()
                        row.set_title(display_key)
                        row.set_subtitle(display_value)
                        
                        if 'GPS' in key or 'Location' in key:
                            icon = Gtk.Image.new_from_icon_name("mark-location-symbolic")
                        elif 'Date' in key or 'Time' in key:
                            icon = Gtk.Image.new_from_icon_name("x-office-calendar-symbolic")
                        elif 'Size' in key or 'Width' in key or 'Height' in key:
                            icon = Gtk.Image.new_from_icon_name("view-fullscreen-symbolic")
                        elif 'Camera' in key or 'Make' in key or 'Model' in key:
                            icon = Gtk.Image.new_from_icon_name("camera-photo-symbolic")
                        else:
                            icon = Gtk.Image.new_from_icon_name("dialog-information-symbolic")
                        
                        row.add_prefix(icon)
                        
                        # Buton kutusu
                        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
                        
                        # Düzenle butonu
                        edit_btn = Gtk.Button(icon_name="document-edit-symbolic")
                        edit_btn.add_css_class("flat")
                        edit_btn.set_tooltip_text(self.lang.get_text('MAIN', 'edit'))
                        edit_btn.connect("clicked", self.on_edit_value, key, str(value))
                        btn_box.append(edit_btn)
                        
                        # Kopyala butonu
                        copy_btn = Gtk.Button(icon_name="edit-copy-symbolic")
                        copy_btn.add_css_class("flat")
                        copy_btn.set_tooltip_text(self.lang.get_text('MAIN', 'copy'))
                        copy_btn.connect("clicked", self.on_copy_value, str(value))
                        btn_box.append(copy_btn)
                        
                        row.add_suffix(btn_box)
                        
                        expander.add_row(row)
                    
                    self.metadata_list.append(expander)
                    
                else:
                    # Diğer gruplar için normal görünüm
                    group_widget = Adw.PreferencesGroup()
                    group_widget.set_title(group_info['title'])
                    group_widget.set_margin_top(12)
                    
                    for key, value in sorted(items.items()):
                        if isinstance(value, (list, dict)):
                            value = json.dumps(value, indent=2, ensure_ascii=False)
                        elif isinstance(value, bytes):
                            value = str(value)
                        elif value is None:
                            continue

                        display_value = str(value)
                        if len(display_value) > 100:
                            display_value = display_value[:97] + "..."
                        
                        display_key = key.split(':', 1)[-1].strip()
                        display_key = self.lang.get_text('KEYS', display_key, fallback=display_key)
                        
                        row = Adw.ActionRow()
                        row.set_title(display_key)
                        row.set_subtitle(display_value)
                        
                        if 'GPS' in key or 'Location' in key:
                            icon = Gtk.Image.new_from_icon_name("mark-location-symbolic")
                        elif 'Date' in key or 'Time' in key:
                            icon = Gtk.Image.new_from_icon_name("x-office-calendar-symbolic")
                        elif 'Size' in key or 'Width' in key or 'Height' in key:
                            icon = Gtk.Image.new_from_icon_name("view-fullscreen-symbolic")
                        elif 'Camera' in key or 'Make' in key or 'Model' in key:
                            icon = Gtk.Image.new_from_icon_name("camera-photo-symbolic")
                        else:
                            icon = Gtk.Image.new_from_icon_name("dialog-information-symbolic")
                        
                        row.add_prefix(icon)
                        
                        # Buton kutusu
                        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
                        
                        # Düzenle butonu
                        edit_btn = Gtk.Button(icon_name="document-edit-symbolic")
                        edit_btn.add_css_class("flat")
                        edit_btn.set_tooltip_text(self.lang.get_text('MAIN', 'edit'))
                        edit_btn.connect("clicked", self.on_edit_value, key, str(value))
                        btn_box.append(edit_btn)
                        
                        # Kopyala butonu
                        copy_btn = Gtk.Button(icon_name="edit-copy-symbolic")
                        copy_btn.add_css_class("flat")
                        copy_btn.set_tooltip_text(self.lang.get_text('MAIN', 'copy'))
                        copy_btn.connect("clicked", self.on_copy_value, str(value))
                        btn_box.append(copy_btn)
                        
                        row.add_suffix(btn_box)
                        
                        group_widget.add(row)
                    
                    list_row = Gtk.ListBoxRow()
                    list_row.set_activatable(False)
                    list_row.set_child(group_widget)
                    self.metadata_list.append(list_row)

        # Metadata yoksa mesaj göster
        if not grouped_data:
            self.clean_button.set_sensitive(False)
            self.save_button.set_sensitive(False)
            
            status_page = Adw.StatusPage()
            status_page.set_icon_name("dialog-information-symbolic")
            status_page.set_title(self.lang.get_text('MAIN', 'no_metadata_found'))
            
            no_data_row = Gtk.ListBoxRow()
            no_data_row.set_activatable(False)
            no_data_row.set_child(status_page)
            self.metadata_list.append(no_data_row)
        else:
            self.clean_button.set_sensitive(True)
            self.save_button.set_sensitive(bool(self.changed_metadata))
        
        # Navigasyon butonlarını güncelle
        self.update_navigation_buttons()
    
    def on_copy_value(self, button, value):
        """Değeri panoya kopyalar"""
        clipboard = Gdk.Display.get_default().get_clipboard()
        clipboard.set(value)
    
    def on_edit_value(self, button, key, value):
        """Metadata değerini düzenle"""
        dialog = Adw.MessageDialog.new(self)
        dialog.set_heading(f"{self.lang.get_text('MAIN', 'edit')}: {key.split(':', 1)[-1]}")
        dialog.set_body(self.lang.get_text('MAIN', 'enter_new_value'))
        
        # Entry widget
        entry = Gtk.Entry()
        entry.set_text(value)
        entry.set_margin_start(12)
        entry.set_margin_end(12)
        entry.set_margin_top(12)
        entry.set_margin_bottom(12)
        dialog.set_extra_child(entry)
        
        dialog.add_response("cancel", self.lang.get_text('DIALOGS', 'cancel'))
        dialog.add_response("save", self.lang.get_text('MAIN', 'save'))
        dialog.set_response_appearance("save", Adw.ResponseAppearance.SUGGESTED)
        dialog.set_default_response("save")
        
        def on_response(dialog, response):
            if response == "save":
                new_value = entry.get_text()
                self.update_metadata_value(key, new_value)
            dialog.destroy()
        
        dialog.connect("response", on_response)
        dialog.present()
 
    def on_undo_clicked(self, button):
        """Değişiklikleri geri al"""
        if self.changed_metadata:
            # Değişiklikleri geri al
            self.changed_metadata.clear()
            self.load_metadata()  # Orijinal metadata'yı yeniden yükle
            self.save_button.set_sensitive(False)
            self.undo_button.set_sensitive(False)
    
    def on_save_clicked(self, button):
        """Metadata değişikliklerini dosyaya kaydet"""
        if not self.current_files:
            return
        
        if not self.changed_metadata:
            self.logger.info("Değişiklik yok, kaydetme işlemi atlandı.")
            GLib.idle_add(self._on_save_success, "Değişiklik yapılmadığı için işlem atlandı.")
            return
        
        current_file = self.current_files[self.current_file_index]
        
        def save_worker():
            try:
                cmd = ['exiftool', '-overwrite_original']
                
                for key, value in self.changed_metadata.items():
                    # Salt okunur etiketleri atla
                    if key.startswith('File:') or key.startswith('Composite:'):
                        continue
                    
                    if ':' in key:
                        tag_name = key.split(':', 1)[1]
                        cmd.extend([f'-{tag_name}={value}'])
                
                cmd.append(current_file)
                
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                
                # Değişiklikler kaydedildikten sonra listeyi temizle
                self.changed_metadata.clear()
                
                GLib.idle_add(self._on_save_success)
                
                   
        thread = threading.Thread(target=save_worker, daemon=True)
        thread.start()
    
    def _on_save_success(self, message=None):
        """Kaydetme başarılı"""
        self.save_button.set_sensitive(False)
        self.undo_button.set_sensitive(False)
        dialog = Adw.MessageDialog.new(self)
        dialog.set_heading(self.lang.get_text('DIALOGS', 'success_title'))
        body_text = message if message else self.lang.get_text('DIALOGS', 'save_success')
        dialog.set_body(body_text)
        dialog.add_response("ok", self.lang.get_text('DIALOGS', 'ok'))
        dialog.present()
    
    def _on_save_error(self, error):
        """Kaydetme hatası"""
        self.show_error_dialog(self.lang.get_text('DIALOGS', 'save_error_title'), error)
    
    def on_prev_file_clicked(self, button):
        """Bir önceki dosyaya geç"""
        if self.current_file_index > 0:
            self.current_file_index -= 1
            self.load_metadata()
    
    def on_next_file_clicked(self, button):
        """Bir sonraki dosyaya geç"""
        if self.current_file_index + 1 < len(self.current_files):
            self.current_file_index += 1
            self.load_metadata()
    
    def update_navigation_buttons(self):
        """Navigasyon butonlarının durumunu güncelle"""
        if hasattr(self, 'prev_button') and hasattr(self, 'next_button'):
            self.prev_button.set_sensitive(self.current_file_index > 0)
            self.next_button.set_sensitive(self.current_file_index + 1 < len(self.current_files))
    
    def on_about_clicked(self, button):
        """Hakkında dialogunu göster"""
        self.about_click_count = 0  # Sayacı sıfırla
        
        about = Adw.AboutWindow(transient_for=self)
        about.set_application_name(self.lang.get_text('MAIN', 'app_title'))
        about.set_version("1.0.0")
        about.set_developer_name("Fatih ÖNDER (CekToR)")
        about.set_comments(self.lang.get_text('ABOUT', 'short_description'))
        about.set_license_type(Gtk.License.GPL_3_0)
        about.set_website("https://github.com/cektor")
        about.set_issue_url("https://github.com/cektor/metador/issues")
        about.add_credit_section(self.lang.get_text('ABOUT', 'developer'), ["Fatih ÖNDER (CekToR)"])
        about.add_credit_section(self.lang.get_text('ABOUT', 'thanks'), ["ExifTool", "GTK4", "Libadwaita"])
        
        # Hakkında dialogı için ikon
        try:
            icon_path = Path("/usr/share/pixmaps/metadorlo.png")
            if icon_path.exists():
                about.set_application_icon("metadorlo")
            else:
                about.set_application_icon("edit-clear-all-symbolic")
        except Exception:
            about.set_application_icon("edit-clear-all-symbolic")
        
        # Easter Egg için tıklama olayı ekle
        click_gesture = Gtk.GestureClick.new()
        click_gesture.connect("pressed", self.on_about_logo_clicked)
        about.add_controller(click_gesture)
        
        about.present()
    
    def on_about_logo_clicked(self, gesture, n_press, x, y):
        """Hakkında dialogundaki logoya tıklandığında Easter Egg kontrolü"""
        # Sadece logo alanına tıklandığını kontrol et (yaklaşık logo konumu)
        if 50 <= x <= 150 and 20 <= y <= 120:  # Logo alanı koordinatları
            self.about_click_count += 1
            
            if self.about_click_count >= 3:
                self.show_easter_egg()
                self.about_click_count = 0
    
    def show_easter_egg(self):
        """Easter Egg dialogını göster"""
        dialog = Adw.MessageDialog.new(self)
        dialog.set_heading(self.lang.get_text('EASTER_EGG', 'title'))
        
        # Easter Egg içeriği
        content = f"{self.lang.get_text('EASTER_EGG', 'meaning_title')}\n{self.lang.get_text('EASTER_EGG', 'meaning_text')}\n\n{self.lang.get_text('EASTER_EGG', 'why_title')}\n{self.lang.get_text('EASTER_EGG', 'why_text')}"
        dialog.set_body(content)
        
        dialog.add_response("ok", self.lang.get_text('DIALOGS', 'ok'))
        dialog.set_default_response("ok")
        dialog.present()

    def on_clean_clicked(self, button):
        if not self.current_files:
            return
        
        file_count = len(self.current_files)
        if file_count == 1:
            filename = os.path.basename(self.current_files[0])
            message = self.lang.get_text('DIALOGS', 'clean_message', filename=filename)
        else:
            message = f"{file_count} dosyanın metadata'sını temizlemek istediğinizden emin misiniz?"
        
        dialog = Adw.MessageDialog.new(self)
        dialog.set_heading(self.lang.get_text('DIALOGS', 'clean_title'))
        dialog.set_body(message)
        dialog.add_response("cancel", self.lang.get_text('DIALOGS', 'cancel'))
        dialog.add_response("clean", self.lang.get_text('DIALOGS', 'clean'))
        dialog.set_response_appearance("clean", Adw.ResponseAppearance.DESTRUCTIVE)
        dialog.set_default_response("cancel")
        dialog.set_close_response("cancel")
        dialog.connect("response", self.on_clean_response)
        dialog.present()
    
    def on_clean_response(self, dialog, response):
        if response == "clean":
            self.clean_metadata()
    
    def clean_metadata(self):
        if not self.current_files:
            return
        
        self.clean_file_index = 0
        self.clean_button.set_sensitive(False)
        self.clean_next_file()
    
    def clean_next_file(self):
        if self.clean_file_index >= len(self.current_files):
            # Tüm dosyalar temizlendi
            GLib.idle_add(self._on_all_files_cleaned)
            return
        
        current_file = self.current_files[self.clean_file_index]
        
        # Dosya tipi kontrolü
        is_supported, error_msg = self.is_supported_file_type(current_file)
        if not is_supported:
            self.logger.warning(f"Desteklenmeyen dosya atlanıyor: {current_file} - {error_msg}")
            # Sonraki dosyaya geç
            self.clean_file_index += 1
            GLib.idle_add(self.clean_next_file)
            return
        
        backup_file = f"{current_file}.metadatacleaner.bak"
        
        def clean_worker():
            try:
                self.logger.info(f"Metadata temizleme başlatıldı: {current_file}")
                
                # Yedek dosya oluştur
                self.logger.debug(f"Yedek dosya oluşturuluyor: {backup_file}")
                shutil.copy2(current_file, backup_file)
                
                # Tek komutla optimize edilmiş temizleme
                cmd = [
                    'exiftool',
                    '-all=',                    # Tüm metadata'yı sil
                    '-tagsFromFile', '@',       # Orijinal dosyadan temel etiketleri koru
                    '-FileType',                # Dosya tipini koru
                    '-FileTypeExtension',       # Dosya uzantısını koru
                    '-MIMEType',               # MIME tipini koru
                    '-ImageSize',              # Görüntü boyutunu koru
                    '-overwrite_original',     # Orijinal dosyayı değiştir
                    '-P',                      # Dosya izinlerini koru
                    current_file
                ]
                
                self.logger.debug(f"Temizlik komutu: {' '.join(cmd)}")
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                
                if result.stdout:
                    self.logger.debug(f"ExifTool çıktısı: {result.stdout}")
                if result.stderr:
                    self.logger.warning(f"ExifTool uyarıları: {result.stderr}")
                
                # Yedek dosyayı temizle
                if os.path.exists(backup_file):
                    os.remove(backup_file)
                    self.logger.debug(f"Yedek dosya silindi: {backup_file}")
                
                # Sonraki dosyaya geç
                self.clean_file_index += 1
                GLib.idle_add(self.clean_next_file)
                
            except subprocess.CalledProcessError as e:
                error_msg = f"ExifTool hatası: {e.stderr}"
                self.logger.error(error_msg)
                self.logger.error(f"Hata kodu: {e.returncode}")
                
                # Yedek dosyayı geri yükle
                if os.path.exists(backup_file):
                    self.logger.info("Yedek dosya geri yükleniyor")
                    shutil.copy2(backup_file, current_file)
                    os.remove(backup_file)
                
                GLib.idle_add(self._on_clean_error, error_msg)
                
            except Exception as e:
                error_msg = f"Beklenmeyen hata: {str(e)}"
                self.logger.error(error_msg)
                self.logger.error(traceback.format_exc())
                
                # Yedek dosyayı geri yükle
                if os.path.exists(backup_file):
                    self.logger.info("Yedek dosya geri yükleniyor")
                    shutil.copy2(backup_file, current_file)
                    os.remove(backup_file)
                
                GLib.idle_add(self._on_clean_error, error_msg)
        
        thread = threading.Thread(target=clean_worker, daemon=True)
        thread.start()
    
    def _on_all_files_cleaned(self):
        """Tüm dosyalar temizlendiğinde çalışır"""
        self.clean_button.set_sensitive(True)
        
        # Başarı mesajını göster
        success_dialog = Adw.MessageDialog.new(self)
        success_dialog.set_heading(self.lang.get_text('DIALOGS', 'success_title'))
        
        if len(self.current_files) == 1:
            message = self.lang.get_text('DIALOGS', 'success_message')
        else:
            message = f"{len(self.current_files)} dosyanın metadata'sı başarıyla temizlendi."
            
        success_dialog.set_body(message)
        success_dialog.add_response("ok", self.lang.get_text('DIALOGS', 'ok'))
        success_dialog.set_default_response("ok")
        success_dialog.set_close_response("ok")
        success_dialog.connect("response", self._on_success_dialog_response)
        success_dialog.present()
    
    def _on_clean_error(self, error):
        """Temizleme hatası durumunda çalışır"""
        self.clean_button.set_sensitive(True)
        self.show_error_dialog(self.lang.get_text('DIALOGS', 'clean_error_title'), error)
    
    def _on_success_dialog_response(self, dialog, response):
        """Başarı dialogu kapatıldığında anasayfaya dön"""
        # Durumu sıfırla
        self.current_files = []
        self.current_file_index = 0
        self.metadata = {}
        self.changed_metadata = {}
        self.clean_button.set_sensitive(False)
        self.save_button.set_sensitive(False)
        
        # Anasayfaya dön
        self.stack.set_visible_child_name("welcome")

    def check_exiftool(self):
        try:
            subprocess.run(['exiftool', '-ver'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False


class MetadataCleanerApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id='com.github.metador',
                        flags=Gio.ApplicationFlags.FLAGS_NONE)
        
        # LanguageManager'ı önce başlat
        self.lang = LanguageManager()
        
        # GResource'u yükle
        self.load_resources()
    
 
        
        # Dil değiştirme aksiyonu
        set_lang_action = Gio.SimpleAction.new_stateful(
            "set_language", 
            GLib.VariantType.new("s"),
            GLib.Variant("s", self.lang.get_current_language())
        )
        set_lang_action.connect("activate", self.on_set_language)
        self.add_action(set_lang_action)
        

if __name__ == '__main__':
    app = MetadataCleanerApp()
    app.run(None)
