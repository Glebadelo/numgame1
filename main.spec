# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:/Users/glebb/OneDrive/Programming/TrirdYear/python/numgame'],
             binaries=[],
             datas=[('login_screen.ui', '.'),
             ('signup_screen.ui', '.'),
             ('game_screen.ui', '.'),
             ('gamemenu_screen.ui', '.'),
             ('leaderboard_screen.ui', '.'),
             ('users_db.db', '.')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='NumGame',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon='C:/Users/glebb/OneDrive/Programming/TrirdYear/python/numgame/icon.ico')
