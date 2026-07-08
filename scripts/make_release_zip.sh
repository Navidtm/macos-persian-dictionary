#!/usr/bin/env bash
#
# Assemble a release/EnglishPersianDictionary-vX.Y.Z.zip that an end user
# can download, extract, and install with two double-clicks -- no Python,
# Make, Xcode, or Dictionary Development Kit required on their machine.
#
# Usage:
#   scripts/make_release_zip.sh <version> <path-to-.dictionary-bundle>
#
# Called by `make release`; not normally run directly.
#
set -euo pipefail

VERSION="${1:?Usage: $0 <version> <path-to-.dictionary-bundle>}"
BUNDLE_PATH="${2:?Usage: $0 <version> <path-to-.dictionary-bundle>}"

if [[ ! -d "$BUNDLE_PATH" ]]; then
  echo "ERROR: '$BUNDLE_PATH' does not exist. Run 'make package' first." >&2
  exit 1
fi

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RELEASE_DIR="$REPO_ROOT/release"
STAGING_DIR="$RELEASE_DIR/staging"
ZIP_NAME="EnglishPersianDictionary-v${VERSION}.zip"
ZIP_PATH="$RELEASE_DIR/$ZIP_NAME"

rm -rf "$STAGING_DIR"
mkdir -p "$STAGING_DIR"

cp -R "$BUNDLE_PATH" "$STAGING_DIR/"
cp "$REPO_ROOT/resources/release/Install.command" "$STAGING_DIR/"
cp "$REPO_ROOT/resources/release/Uninstall.command" "$STAGING_DIR/"
cp "$REPO_ROOT/resources/release/README.txt" "$STAGING_DIR/"
chmod +x "$STAGING_DIR/Install.command" "$STAGING_DIR/Uninstall.command"

rm -f "$ZIP_PATH"
( cd "$STAGING_DIR" && zip -r -X "$ZIP_PATH" . -x '*.DS_Store' >/dev/null )

rm -rf "$STAGING_DIR"

echo ""
echo "Created $ZIP_PATH"
