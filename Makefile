#!/usr/bin/make -f

# Metadata Cleaner Build System

.PHONY: all build install clean gresource schema

all: build

# GResource dosyasını derle
gresource:
	glib-compile-resources --target=metadatacleaner.gresource metadatacleaner.gresource.xml

# GSettings schema'yı derle (geliştirme için)
schema:
	mkdir -p schemas
	cp com.github.metadatacleaner.gschema.xml schemas/
	glib-compile-schemas schemas/

# Tüm kaynakları derle
build: gresource schema

# Temizlik
clean:
	rm -f metadatacleaner.gresource
	rm -rf schemas/

# Çalıştır (geliştirme)
run: build
	GSETTINGS_SCHEMA_DIR=./schemas python3 metadata_cleaner.py

# Kurulum (sistem geneli)
install: build
	# Ana uygulama
	install -Dm755 metadata_cleaner.py $(DESTDIR)/usr/bin/metadata-cleaner
	install -Dm644 language_manager.py $(DESTDIR)/usr/share/metadata-cleaner/language_manager.py
	
	# Kaynaklar
	install -Dm644 metadatacleaner.gresource $(DESTDIR)/usr/share/metadata-cleaner/metadatacleaner.gresource
	
	# GSettings schema
	install -Dm644 com.github.metadatacleaner.gschema.xml $(DESTDIR)/usr/share/glib-2.0/schemas/com.github.metadatacleaner.gschema.xml
	
	# Desktop dosyası (opsiyonel)
	# install -Dm644 com.github.metadatacleaner.desktop $(DESTDIR)/usr/share/applications/com.github.metadatacleaner.desktop