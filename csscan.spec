# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('gui/database/csscan_db.db', 'gui/database'), ('login/database/cs_scanner_users.db', 'login/database'), ('login/database/UserDatabaseManager.py', 'login/database'), ('login/auth_module.py', 'login'), ('login/sessionmanager.py', 'login'), ('login/license/license.key', 'login/license'), ('login/license/key.key', 'login/license'), ('settings.json', '.'), ('gui/themes/default.json', 'gui/themes'), ('gui/themes/bright_theme.json', 'gui/themes'), ('gui/themes/dracula.json', 'gui/themes'), ('gui/images/svg_icons', 'gui/images/svg_icons'), ('gui/images/svg_images', 'gui/images/svg_images'), ('gui/uis/pages/page_3/database_detail.xlsx', 'gui/uis/pages/page_3'), ('gui/uis/pages/page_3/linux_detail.xlsx', 'gui/uis/pages/page_3'), ('gui/uis/pages/page_3/windows_detail.xlsx', 'gui/uis/pages/page_3'), ('gui/uis/pages/page_4/database_template.xlsx', 'gui/uis/pages/page_4'), ('gui/uis/pages/page_4/linux_template.xlsx', 'gui/uis/pages/page_4'), ('gui/uis/pages/page_4/windows_template.xlsx', 'gui/uis/pages/page_4'), ('login/create_admin_account', 'login')],
    hiddenimports=['cryptography.hazmat.primitives.kdf.pbkdf2'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='csscan',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='csscan',
)
app = BUNDLE(
    coll,
    name='csscan.app',
    icon='icon.ico',
    bundle_identifier=None,
)
