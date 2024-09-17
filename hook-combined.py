from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# Sammeln Sie alle Submodule von xhtml2pdf und anderen wichtigen Paketen
hiddenimports = collect_submodules('xhtml2pdf')
hiddenimports += collect_submodules('PIL')
hiddenimports += collect_submodules('matplotlib')

# Fügen Sie spezifische Module hinzu, die in Ihrem Projekt verwendet werden
hiddenimports += [
    'sqlite3',
    'logging',
    'tkinter',
    'tkinter.ttk',
    'tkinter.messagebox',
    'tkinter.filedialog',
    'webbrowser',
    'configparser',
    'base64',
    'io',
    'datetime',
    'os',
    'shutil',
]

# Sammeln Sie alle Datendateien von xhtml2pdf und PIL
datas = collect_data_files('xhtml2pdf')
datas += collect_data_files('PIL')

# Matplotlib-spezifische Daten
datas += collect_data_files('matplotlib')

# Fügen Sie tkinter-spezifische Daten hinzu (falls nötig)
# datas += collect_data_files('tkinter')

# Fügen Sie hier spezifische Dateien oder Verzeichnisse hinzu, die Ihr Projekt benötigt
# Beispiel:
# datas += [('pfad/zu/ihren/assets', 'assets')]

# Stellen Sie sicher, dass alle benötigten Schriftarten eingebunden sind
# datas += [('pfad/zu/ihren/fonts', 'fonts')]