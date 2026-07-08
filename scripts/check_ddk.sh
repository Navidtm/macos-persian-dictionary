#!/usr/bin/env bash
#
# Verify that Apple's Dictionary Development Kit is available at the given
# path, printing a helpful, accurate error message if not. Shared by the
# `package` and `release` Makefile targets so the message only lives in one
# place.
#
# Usage:
#   scripts/check_ddk.sh "/path/to/Dictionary Development Kit"
#
set -euo pipefail

DDK_ROOT="${1:-}"
BUILD_DICT="$DDK_ROOT/bin/build_dict.sh"

if [[ -x "$BUILD_DICT" ]]; then
  exit 0
fi

cat >&2 <<EOF

ERROR: Dictionary Development Kit not found at:
  $BUILD_DICT

Apple no longer distributes the DDK through Xcode (it was removed from
Additional Tools after Xcode 9, back in 2017), so it won't be in
Xcode > Settings > Components on any current Xcode install.

Get a preserved copy instead, e.g.:
  git clone https://github.com/nanoskript/dictionary-development-kit.git kit

If you clone it to ./kit (as above), the Makefile finds it automatically.
Otherwise point commands at it explicitly:
  make package DDK_ROOT="/path/to/dictionary-development-kit"

On Apple Silicon, if you hit 'bad CPU type in executable', install Rosetta
once with: softwareupdate --install-rosetta --agree-to-license

EOF
exit 1
