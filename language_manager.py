import configparser
import os
from gi.repository import Gio, GLib

class LanguageManager:
    def __init__(self):
        self.current_language = 'turkish'
        self.translations = {}
        # Önce sistem konumunu dene, sonra yerel konumu
        system_lang_dir = '/usr/share/metador/languages'
        local_lang_dir = os.path.join(os.path.dirname(__file__), 'languages')
        
        if os.path.exists(system_lang_dir):
            self.languages_dir = system_lang_dir
        else:
            self.languages_dir = local_lang_dir
        
        # GSettings kullanımı (schema yoksa fallback)
        self.app_settings = None
        try:
            # Schema'nın varlığını kontrol et
            schema_source = Gio.SettingsSchemaSource.get_default()
            if schema_source and schema_source.lookup('com.github.metador', False):
                self.app_settings = Gio.Settings.new('com.github.metador')
                self.current_language = self.app_settings.get_string('current-language')
            else:
                raise Exception("Schema not found")
        except Exception:
            # Schema yoksa basit dosya sistemi
            self.app_settings = None
            self.settings_file = os.path.join(GLib.get_user_config_dir(), 'metador', 'settings')
            self.load_settings()
        
        self.load_translations()
    
    def load_settings(self):
        """Ayarları yükle (fallback)"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    self.current_language = f.read().strip()
            except:
                self.current_language = 'turkish'
        else:
            self.current_language = 'turkish'
    
    def save_settings(self):
        """Ayarları kaydet"""
        if self.app_settings:
            self.app_settings.set_string('current-language', self.current_language)
        else:
            # Fallback dosya sistemi
            try:
                os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
                with open(self.settings_file, 'w') as f:
                    f.write(self.current_language)
            except:
                pass
    
    def load_translations(self):
        """Çeviri dosyalarını yükle"""
        # Dinamik dil listesi oluştur
        available_langs = self.get_available_language_files()
        
        for lang in available_langs:
            # Önce GResource'tan yüklemeyi dene
            try:
                resource_path = f"/com/github/metador/languages/{lang}.ini"
                resource_bytes = Gio.resources_lookup_data(resource_path, Gio.ResourceLookupFlags.NONE)
                content = resource_bytes.get_data().decode('utf-8')
                
                config = configparser.ConfigParser()
                config.read_string(content)
                self.translations[lang] = {}
                for section in config.sections():
                    self.translations[lang][section] = dict(config[section])
            except:
                # Fallback: dosya sisteminden yükle
                lang_file = os.path.join(self.languages_dir, f'{lang}.ini')
                if os.path.exists(lang_file):
                    config = configparser.ConfigParser()
                    config.read(lang_file, encoding='utf-8')
                    self.translations[lang] = {}
                    for section in config.sections():
                        self.translations[lang][section] = dict(config[section])
    
    def get_text(self, section, key, fallback=None, **kwargs):
        """Çeviri metnini al"""
        try:
            text = self.translations[self.current_language][section][key]
            if kwargs:
                return text.format(**kwargs)
            return text
        except KeyError:
            # Fallback to English if Turkish translation not found
            try:
                text = self.translations['english'][section][key]
                if kwargs:
                    return text.format(**kwargs)
                return text
            except KeyError:
                # Eğer İngilizce'de de yoksa, 'fallback' değerini veya anahtarı döndür
                if fallback:
                    return fallback
                return f"{section}.{key}"
    
    def set_language(self, language):
        """Dili değiştir"""
        if language in self.translations:
            self.current_language = language
            self.save_settings()
            return True
        return False
    
    def get_available_languages(self):
        """Mevcut dilleri dinamik olarak al"""
        return list(self.translations.keys())
    
    def get_current_language(self):
        """Mevcut dili al"""
        return self.current_language
    
    def get_available_language_files(self):
        """Mevcut dil dosyalarını dinamik olarak bul"""
        langs = []
        
        # Önce GResource'tan deneyin
        try:
            resource_path = "/com/github/metador/languages"
            children = Gio.resources_enumerate_children(resource_path, Gio.ResourceLookupFlags.NONE)
            resource_langs = [child.split('.')[0] for child in children if child.endswith('.ini')]
            if resource_langs:
                langs.extend(lang for lang in resource_langs if lang not in langs)
            else:
                # Fallback (eğer GResource taraması başarısız olursa)
                langs.extend(['turkish', 'english'])
        except Exception as e:
            # Hata durumunda veya GResource bulunamazsa
            pass
        
        # Dosya sisteminden de kontrol et
        if os.path.exists(self.languages_dir):
            for file in os.listdir(self.languages_dir):
                if file.endswith('.ini'):
                    lang_name = file[:-4]  # .ini uzantısını kaldır
                    if lang_name not in langs:
                        langs.append(lang_name)
        
        # En az türkçe ve ingilizce olsun
        if 'turkish' not in langs:
            langs.append('turkish')
        if 'english' not in langs:
            langs.append('english')
            
        return langs
    
