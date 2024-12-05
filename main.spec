# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\matth\\PycharmProjects\\csf-coding-olympiad-2025\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets'), ('assets/fonts', 'assets/fonts')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PowerIsland',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    company_name="Island Swallowtails",
    copyright="Copyright (c) 2024 Island Swallowtails Team",
    description="Raising awareness about sustainable energy generation",
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="energy_icon.ico"
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PowerIsland',
)
