#!/usr/bin/env bash
#
# Remove a previously installed .dictionary bundle from
# ~/Library/Dictionaries.
#
# Usage:
#   scripts/uninstall_dictionary.sh EnglishPersianDictionary
#
set -euo pipefail

DICT_NAME="${1:-EnglishPersianDictionary}"
DEST_PATH="$HOME/Library/Dictionaries/$DICT_NAME.dictionary"

if [[ ! -d "$DEST_PATH" ]]; then
  echo "Nothing to remove: $DEST_PATH does not exist."
  exit 0
fi

echo "Removing $DEST_PATH ..."
rm -rf "$DEST_PATH"

echo "Restarting Dictionary.app ..."
killall Dictionary >/dev/null 2>&1 || true

echo "Done."
