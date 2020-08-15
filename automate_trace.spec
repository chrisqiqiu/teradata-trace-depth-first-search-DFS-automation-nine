# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['automate_trace.py'],
             pathex=['C:\\Users\\cqiu\\Desktop\\projects\\teradata-migration\\teradata_trace\\automation'],
             binaries=[('C:\\Users\\cqiu\\Desktop\\projects\\teradata-migration\\teradata_trace\\automation\\env\\Lib\\site-packages\\teradatasql', 'teradatasql')],
             datas=[],
             hiddenimports=[],
             hookspath=[],
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
          name='automate_trace',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='trace_shoe.ico')
