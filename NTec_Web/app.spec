# -*- mode: python -*-
import sys
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

# Collect all Flask templates & static files
datas = [
    ('templates/**/*', 'templates'),
    ('static/**/*',    'static'),
]

# Collect dynamic imports from python-can, etc.
hidden_imports = collect_submodules('can')

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ntec5',
    debug=False,
    strip=False,
    upx=True,
    console=False,        # False → hide console window on Windows
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='ntec5'
)