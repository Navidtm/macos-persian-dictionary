#!/bin/bash
#
# Double-click this file in Finder to install the English-Persian
# dictionary into Dictionary.app for the current user. No Terminal,
# Python, Xcode, or developer tools required.
#
set -euo pipefail
cd "$(dirname "$0")"

DICT_BUNDLE="EnglishPersianDictionary.dictionary"
DEST_DIR="$HOME/Library/Dictionaries"

if [[ ! -d "$DICT_BUNDLE" ]]; then
  echo "ERROR: '$DICT_BUNDLE' not found next to this script."
  echo "Make sure you extracted the full ZIP before running Install.command."
  read -n 1 -s -r -p "Press any key to close this window..."
  echo ""
  exit 1
fi

echo "Installing English-Persian dictionary for $(whoami)..."
mkdir -p "$DEST_DIR"
rm -rf "$DEST_DIR/$DICT_BUNDLE"
cp -R "$DICT_BUNDLE" "$DEST_DIR/"

echo "Restarting Dictionary.app..."
killall Dictionary >/dev/null 2>&1 || true
open -a Dictionary

echo ""
echo "Done! In Dictionary.app, open Dictionary > Settings (or Preferences)"
echo "and enable \"English-Persian\" in the list of dictionaries."
echo ""
read -n 1 -s -r -p "Press any key to close this window..."
echo ""
