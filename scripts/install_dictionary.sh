#!/usr/bin/env bash
#
# Install a built .dictionary bundle into ~/Library/Dictionaries and
# restart Dictionary.app so it picks up the change.
#
# Usage:
#   scripts/install_dictionary.sh objects/EnglishPersianDictionary.dictionary
#
set -euo pipefail

BUNDLE_PATH="${1:-}"

if [[ -z "$BUNDLE_PATH" ]]; then
  echo "Usage: $0 <path-to-.dictionary-bundle>" >&2
  exit 1
fi

if [[ ! -d "$BUNDLE_PATH" ]]; then
  echo "ERROR: '$BUNDLE_PATH' does not exist. Run 'make package' first." >&2
  exit 1
fi

if [[ "$(uname)" != "Darwin" ]]; then
  echo "ERROR: installing into Dictionary.app is only supported on macOS." >&2
  exit 1
fi

DEST_DIR="$HOME/Library/Dictionaries"
mkdir -p "$DEST_DIR"

BUNDLE_NAME="$(basename "$BUNDLE_PATH")"
DEST_PATH="$DEST_DIR/$BUNDLE_NAME"

echo "Installing $BUNDLE_NAME to $DEST_DIR ..."
rm -rf "$DEST_PATH"
cp -R "$BUNDLE_PATH" "$DEST_PATH"

echo "Restarting Dictionary.app ..."
killall Dictionary >/dev/null 2>&1 || true

echo ""
echo "Done. Open Dictionary.app, then go to Dictionary > Settings (or"
echo "Preferences) and enable 'English-Persian' in the list of dictionaries."
