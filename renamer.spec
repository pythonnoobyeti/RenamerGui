# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['renamer.py'],
             pathex=['D:\\My_stuff\\Programming\\Python\\My_try\\renamer\\v0.3'],
             binaries=[('D:\\My_stuff\\Programming\\Python\\My_try\\renamer\\v0.3\\times-new-roman.ttf', '.')],
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
          Tree('D:\\My_stuff\\Programming\\Python\\My_try\\renamer\\v0.3\\poppler', prefix='poppler\\'),
          Tree('D:\\My_stuff\\Programming\\Python\\My_try\\renamer\\v0.3\\tesseract', prefix='tesseract\\'),
          a.zipfiles,
          a.datas,
          [],
          name='renamer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='D:\\My_stuff\\Programming\\Python\\My_try\\renamer\\v0.3\\subway.ico')