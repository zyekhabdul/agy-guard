#!/usr/bin/env bash
set -euo pipefail

PKG_NAME="agy-guard"
PKG_VER="3.0.1"
PKG_ARCH="all"
DIST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK_DIR="$DIST_DIR/build_deb/${PKG_NAME}_${PKG_VER}_${PKG_ARCH}"

echo "==> Building Debian (.deb) package for $PKG_NAME v$PKG_VER..."
rm -rf "$DIST_DIR/build_deb"
mkdir -p "$WORK_DIR/DEBIAN"
mkdir -p "$WORK_DIR/usr/bin"
mkdir -p "$WORK_DIR/usr/lib/python3/dist-packages"
mkdir -p "$WORK_DIR/usr/share/doc/$PKG_NAME"

cat << EOF > "$WORK_DIR/DEBIAN/control"
Package: agy-guard
Version: $PKG_VER
Section: utils
Priority: optional
Architecture: all
Depends: python3 (>= 3.8)
Maintainer: zyekhabdul <zyekhabdulqadirjailani@gmail.com>
Description: Deterministic AI Agent Governance, AST Blast-Radius Scanner & Verification Harness
 Enterprise governance and integrity verification tool for AI coding agents.
EOF

PROJECT_ROOT="$(cd "$DIST_DIR/../.." && pwd)"
cp -r "$PROJECT_ROOT/src/agy_guard" "$WORK_DIR/usr/lib/python3/dist-packages/"

cat << 'EOF' > "$WORK_DIR/usr/bin/agy-guard"
#!/usr/bin/env python3
import sys
from agy_guard.cli import main
if __name__ == '__main__':
    sys.exit(main())
EOF
chmod 755 "$WORK_DIR/usr/bin/agy-guard"

cp "$PROJECT_ROOT/README.md" "$WORK_DIR/usr/share/doc/$PKG_NAME/"
cp "$PROJECT_ROOT/LICENSE" "$WORK_DIR/usr/share/doc/$PKG_NAME/copyright"

dpkg-deb --build --root-owner-group "$WORK_DIR" "$DIST_DIR/${PKG_NAME}_${PKG_VER}_${PKG_ARCH}.deb"
rm -rf "$DIST_DIR/build_deb"

echo "==> Done! Created: $DIST_DIR/${PKG_NAME}_${PKG_VER}_${PKG_ARCH}.deb"
