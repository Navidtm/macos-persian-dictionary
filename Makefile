# Makefile for the English -> Persian Dictionary.app project.
#
# Targets:
#   make build     - generate build/EnglishPersianDictionary.xml from data/words/*.json
#   make validate  - validate data/words/*.json without building anything
#   make test      - run the automated test suite
#   make preview   - render entries to build/preview.html for design review in a browser
#   make package   - build + compile into a .dictionary bundle (macOS + DDK required)
#   make install   - package + copy the bundle into ~/Library/Dictionaries
#   make uninstall - remove the bundle from ~/Library/Dictionaries
#   make release   - build a versioned, end-user-ready ZIP for GitHub Releases
#   make clean     - remove all generated files
#
# See README.md -> "For Contributors / Developers" for full setup
# instructions, including how to get the Dictionary Development Kit that
# `package`, `install`, and `release` need. End users installing a released
# build never need this Makefile at all -- see README.md -> "For Users".

DICT_NAME    := EnglishPersianDictionary
BUILD_DIR    := build
OBJECTS_DIR  := objects
RELEASE_DIR  := release

# Where Apple's Dictionary Development Kit lives. Resolved in this order:
#   1. An explicit override:            make package DDK_ROOT="/some/path"
#   2. A local checkout at ./kit/       (the convention this project's docs
#      recommend for contributors -- see README.md)
#   3. The path Apple used to install it to, before removing it from Xcode
#      itself (kept as a fallback for anyone who still has it there)
DDK_ROOT ?= $(if $(wildcard kit/bin/build_dict.sh),$(CURDIR)/kit,/Applications/Utilities/Dictionary Development Kit)
BUILD_DICT := $(DDK_ROOT)/bin/build_dict.sh

# Release version, used to name the release ZIP and to stamp
# CFBundleShortVersionString in the built Info.plist. Defaults to the most
# recent git tag (v1.2.3 -> 1.2.3); override with `make release VERSION=1.2.3`.
VERSION ?= $(shell git describe --tags --abbrev=0 2>/dev/null | sed 's/^v//')
ifeq ($(VERSION),)
VERSION := 0.0.0-dev
endif

.PHONY: all build validate test preview package install uninstall release clean help

all: build

help:
	@echo "Available targets:"
	@echo "  build     - generate build/EnglishPersianDictionary.xml from data/words/*.json"
	@echo "  validate  - validate data/words/*.json without building"
	@echo "  test      - run the automated test suite"
	@echo "  preview   - render entries to build/preview.html for design review"
	@echo "  package   - compile build/ into a .dictionary bundle (needs the DDK)"
	@echo "  install   - package + copy the bundle into ~/Library/Dictionaries"
	@echo "  uninstall - remove the bundle from ~/Library/Dictionaries"
	@echo "  release   - build a versioned, end-user-ready ZIP for GitHub Releases"
	@echo "  clean     - remove all generated files"

build:
	python3 scripts/build.py

validate:
	python3 scripts/validate.py

test:
	python3 -m unittest discover -s tests -v

preview:
	python3 scripts/preview.py $(WORDS)
	@echo "Open build/preview.html in any web browser to check the design."

package: build
	@bash scripts/check_ddk.sh "$(DDK_ROOT)"
	mkdir -p "$(OBJECTS_DIR)"
	"$(BUILD_DICT)" \
		"$(DICT_NAME)" \
		"$(BUILD_DIR)/$(DICT_NAME).xml" \
		"$(BUILD_DIR)/$(DICT_NAME).css" \
		"$(BUILD_DIR)/$(DICT_NAME)Info.plist" \
		"$(OBJECTS_DIR)"
	@echo ""
	@echo "Built $(OBJECTS_DIR)/$(DICT_NAME).dictionary"

install: package
	bash scripts/install_dictionary.sh "$(OBJECTS_DIR)/$(DICT_NAME).dictionary"

uninstall:
	bash scripts/uninstall_dictionary.sh "$(DICT_NAME)"

# Builds a versioned .dictionary bundle (with CFBundleShortVersionString
# stamped to $(VERSION)) and zips it together with double-clickable
# Install.command / Uninstall.command scripts and a short end-user README.
# This is the ZIP that gets attached to GitHub Releases -- see
# .github/workflows/release.yml.
release:
	@bash scripts/check_ddk.sh "$(DDK_ROOT)"
	DICT_VERSION="$(VERSION)" python3 scripts/build.py
	mkdir -p "$(OBJECTS_DIR)"
	"$(BUILD_DICT)" \
		"$(DICT_NAME)" \
		"$(BUILD_DIR)/$(DICT_NAME).xml" \
		"$(BUILD_DIR)/$(DICT_NAME).css" \
		"$(BUILD_DIR)/$(DICT_NAME)Info.plist" \
		"$(OBJECTS_DIR)"
	bash scripts/make_release_zip.sh "$(VERSION)" "$(OBJECTS_DIR)/$(DICT_NAME).dictionary"

clean:
	rm -rf "$(BUILD_DIR)" "$(OBJECTS_DIR)" "$(RELEASE_DIR)"
