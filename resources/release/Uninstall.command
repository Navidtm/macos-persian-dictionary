#!/bin/bash
#
# Double-click this file in Finder to remove the English-Persian dictionary
# that Install.command added for the current user.
#
set -euo pipefail

DICT_BUNDLE="EnglishPersianDictionary.dictionary"
DEST_PATH="$HOME/Library/Dictionaries/$DICT_BUNDLE"

if [[ ! -d "$DEST_PATH" ]]; then
  echo "Nothing to remove: $DEST_PATH does not exist."
  read -n 1 -s -r -p "Press any key to close this window..."
  echo ""
  exit 0
fi

echo "Removing $DEST_PATH ..."
rm -rf "$DEST_PATH"

echo "Restarting Dictionary.app..."
killall Dictionary >/dev/null 2>&1 || true

echo "Done."
read -n 1 -s -r -p "Press any key to close this window..."
echo ""
