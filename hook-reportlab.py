# benötigt für pyinstaller
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = collect_submodules('reportlab')