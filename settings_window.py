import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import os


class SettingsWindow(tk.Toplevel):
    """Klasse für das Einstellungsfenster."""

    def __init__(self, master=None, settings=None):
        super().__init__(master)
        self.settings = settings
        self.title("Einstellungen")
        self.create_widgets()
        self.resizable(False, False)  # Größenänderung deaktivieren

    def create_widgets(self):
        """Erstellt die Widgets des Einstellungsfensters."""
        # Label für den Pfad
        tk.Label(self, text="SimplyCal-Pfad:").grid(row=0, column=0, padx=5, pady=5)

        # Eingabefeld für den Pfad
        self.pfad_entry = tk.Entry(self, width=40)
        self.pfad_entry.grid(row=0, column=1, padx=5, pady=5)

        # Button zum Auswählen des Pfads
        tk.Button(self, text="Durchsuchen...", command=self.browse_directory).grid(row=0, column=2, padx=5, pady=5)

        # Pfad aus der INI-Datei laden und anzeigen
        initial_directory = self.settings.get_setting('PATH', 'directory', '/')
        self.pfad_entry.insert(0, initial_directory)

        # Label und Combobox für Datenbankauswahl
        tk.Label(self, text="SimplyCal-DB:").grid(row=1, column=0, padx=5, pady=5,
                                                  sticky="w")  # Sticky west (linksbündig)
        self.database_combobox = ttk.Combobox(self, state="readonly")
        self.database_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="ew")  # Sticky east-west (volle Breite)

        # Datenbanken laden und anzeigen
        self.update_database_combobox()

        # Ausgewählte Datenbank in der INI-Datei speichern
        self.database_combobox.bind("<<ComboboxSelected>>", self.save_selected_database)

        # Eingabefeld für den Protokoll-Pfad
        tk.Label(self, text="Protokolle Speichern:").grid(row=2, column=0, padx=5, pady=5)
        self.protokoll_entry = tk.Entry(self, width=40)
        self.protokoll_entry.grid(row=2, column=1, padx=5, pady=5)
        self.protokoll_entry.insert(0, self.settings.get_protokoll_path())

        # Button zum Auswählen des Protokoll-Pfads
        tk.Button(self, text="Durchsuchen...", command=self.browse_protokoll_directory).grid(row=2, column=2, padx=5,
                                                                                             pady=5)

        # --- Firmendaten ---
        ttk.LabelFrame(self, text="Firmendaten").grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        self.create_labeled_entry(4, "Firma:", 'FIRMA', 'firma')
        self.create_labeled_entry(5, "Straße:", 'FIRMA', 'strasse')
        self.create_labeled_entry(6, "PLZ:", 'FIRMA', 'plz')
        self.create_labeled_entry(7, "Ort:", 'FIRMA', 'ort')

        # --- Firmenlogo hochladen ---
        tk.Label(self, text="Firmenlogo:").grid(row=8, column=0, padx=5, pady=5, sticky="w")
        tk.Button(self, text="Bild auswählen", command=self.upload_logo).grid(row=8, column=1, padx=5, pady=5)
        self.logo_label = tk.Label(self)  # Label für die Anzeige des Firmenlogos
        self.logo_label.grid(row=9, column=0, columnspan=3, padx=5, pady=5)

        # Firmenlogo laden und anzeigen, wenn vorhanden
        logo_path = self.settings.get_logo_path()
        if logo_path and os.path.exists(logo_path):
            self.load_logo(logo_path)

        # --- Prüfer ---
        ttk.LabelFrame(self, text="Prüfer").grid(row=10, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        self.create_labeled_entry(11, "Prüfer:", 'PRUEFER', 'name')

        # --- Unterschrift hochladen ---
        tk.Label(self, text="Unterschrift:").grid(row=12, column=0, padx=5, pady=5, sticky="w")
        tk.Button(self, text="Bild auswählen", command=self.upload_signature).grid(row=12, column=1, padx=5, pady=5)
        self.signature_label = tk.Label(self)  # Label für die Anzeige der Unterschrift
        self.signature_label.grid(row=13, column=0, columnspan=3, padx=5, pady=5)

        # Unterschrift laden und anzeigen, wenn vorhanden
        signature_path = self.settings.get_signature_path()
        if signature_path and os.path.exists(signature_path):
            self.load_signature(signature_path)

        # --- Messgeräte ---
        ttk.LabelFrame(self, text="Messgeräte").grid(row=14, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        # Bereich für Temperaturmessgeräte
        self.temp_frame = ttk.LabelFrame(self, text="Temperaturmessgeräte")
        self.temp_frame.grid(row=15, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        self.temp_entries = []  # Liste zur Speicherung der Eingabefelder

        # Bereich für VDE-Messgeräte
        self.vde_frame = ttk.LabelFrame(self, text="VDE-Messgeräte")
        self.vde_frame.grid(row=16, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        self.vde_entries = []  # Liste zur Speicherung der Eingabefelder

        # Buttons zum Hinzufügen weiterer Messgeräte
        tk.Button(self.temp_frame, text="+ Temperaturmessgerät", command=self.add_temp_messgeraet_row).grid(row=1,
                                                                                                            column=2,
                                                                                                            padx=5,
                                                                                                            pady=5)
        tk.Button(self.vde_frame, text="+ VDE-Messgerät", command=self.add_vde_messgeraet_row).grid(row=1, column=2,
                                                                                                    padx=5, pady=5)

        # Messgeräte aus den Einstellungen laden und anzeigen
        self.load_messgeraete()

        # Neuer Button zum Speichern aller Einstellungen
        tk.Button(self, text="Einstellungen speichern", command=self.save_all_settings).grid(row=31, column=0,
                                                                                             columnspan=3, padx=5,
                                                                                             pady=10)  # Platzierung unter den Messgeräten

    def update_database_combobox(self):
        """Aktualisiert die Datenbank-Combobox mit den verfügbaren .sqlite-Dateien."""
        directory = self.pfad_entry.get()
        databases = self.settings.get_sqlite_databases(directory)
        self.database_combobox['values'] = databases

        # Vorausgewählte Datenbank setzen (falls vorhanden)
        selected_db = self.settings.get_selected_database()
        if selected_db in databases:
            self.database_combobox.set(selected_db)

    def browse_directory(self):
        """Öffnet einen Dialog zur Auswahl eines Verzeichnisses."""
        directory = filedialog.askdirectory(initialdir=self.settings.get_setting('PATH', 'directory', '/'),
                                            title="Wähle ein Verzeichnis")
        if directory:
            self.pfad_entry.delete(0, tk.END)
            self.pfad_entry.insert(0, directory)

            # Pfad in der INI-Datei speichern
            self.settings.set_setting('PATH', 'directory', directory)
            self.update_database_combobox()  # Combobox nach Pfadänderung aktualisieren

    def browse_protokoll_directory(self):
        """Öffnet einen Dialog zur Auswahl eines Verzeichnisses für die Protokolle."""
        directory = filedialog.askdirectory(initialdir=self.settings.get_protokoll_path(),
                                            title="Wähle ein Verzeichnis für Protokolle")
        if directory:
            self.protokoll_entry.delete(0, tk.END)
            self.protokoll_entry.insert(0, directory)
            self.settings.set_protokoll_path(directory)

    def upload_logo(self):
        """Lädt das Firmenlogo hoch und zeigt es an."""
        filepath = filedialog.askopenfilename(
            initialdir="/",
            title="Firmenlogo auswählen",
            filetypes=(("Bilddateien", "*.png *.jpg *.jpeg"), ("alle Dateien", "*.*"))
        )
        if not filepath:
            return  # Abbrechen, wenn kein Bild ausgewählt wurde

        # Bild kopieren und Pfad in settings.ini speichern
        filename = os.path.basename(filepath)
        new_filepath = os.path.join(os.getcwd(), filename)
        shutil.copy2(filepath, new_filepath)
        self.settings.set_setting('FIRMA', 'logo', filename)

        # Bild anzeigen
        self.load_logo(new_filepath)  # neu hinzugefügt

    def load_logo(self, filepath):
        """Lädt das Firmenlogo aus dem angegebenen Pfad und zeigt es an."""
        img = Image.open(filepath)
        img.thumbnail((200, 100))  # Größe anpassen (optional)
        photo = ImageTk.PhotoImage(img)
        self.logo_label.config(image=photo)
        self.logo_label.image = photo

    def upload_signature(self):
        """Lädt die Unterschrift hoch und zeigt sie an."""
        filepath = filedialog.askopenfilename(
            initialdir="/",
            title="Unterschrift auswählen",
            filetypes=(("Bilddateien", "*.png *.jpg *.jpeg"), ("alle Dateien", "*.*"))
        )
        if not filepath:
            return  # Abbrechen, wenn kein Bild ausgewählt wurde

        # Bild kopieren und Pfad in settings.ini speichern
        filename = os.path.basename(filepath)
        new_filepath = os.path.join(os.getcwd(), filename)
        shutil.copy2(filepath, new_filepath)  # Bild kopieren (anstelle von verschieben)
        self.settings.set_setting('PRUEFER', 'unterschrift', filename)

        # Bild anzeigen
        self.load_signature(new_filepath)

    def load_signature(self, filepath):
        """Lädt die Unterschrift aus dem angegebenen Pfad und zeigt sie an."""
        img = Image.open(filepath)
        img.thumbnail((200, 100))
        photo = ImageTk.PhotoImage(img)
        self.signature_label.config(image=photo)
        self.signature_label.image = photo

    def save_selected_database(self, event=None):
        """Speichert die ausgewählte Datenbank in den Einstellungen."""
        selected_db = self.database_combobox.get()
        self.settings.set_selected_database(selected_db)

    def add_temp_messgeraet_row(self, initial_value=""):
        """Fügt eine neue Zeile für ein Temperaturmessgerät hinzu (optional mit Initialwert)."""
        row = len(self.temp_entries) + 1  # Nächste verfügbare Zeile ermitteln
        temp_entry = tk.Entry(self.temp_frame, width=40)
        temp_entry.grid(row=row, column=0, columnspan=2, padx=5, pady=5)
        temp_entry.insert(0, initial_value)  # Initialwert setzen, falls vorhanden
        self.temp_entries.append(temp_entry)  # Eingabefeld zur Liste hinzufügen

    def add_vde_messgeraet_row(self, initial_value=""):
        """Fügt eine neue Zeile für ein VDE-Messgerät hinzu (optional mit Initialwert)."""
        row = len(self.vde_entries) + 1
        vde_entry = tk.Entry(self.vde_frame, width=40)
        vde_entry.grid(row=row, column=0, columnspan=2, padx=5, pady=5)
        vde_entry.insert(0, initial_value)
        self.vde_entries.append(vde_entry)

    def load_messgeraete(self):
        """Lädt die Messgeräte aus den Einstellungen und fügt sie zu den Eingabefeldern hinzu."""
        messgeraete = self.settings.get_messgeraete()
        for i in range(1, 11):  # Iteriere über mögliche Indizes
            temp_key = f'Temperaturmessgeraet_{i}'
            vde_key = f'VDE-Messgeraet_{i}'
            if temp_key in messgeraete and messgeraete[temp_key]:
                self.add_temp_messgeraet_row(messgeraete[temp_key])
            if vde_key in messgeraete and messgeraete[vde_key]:
                self.add_vde_messgeraet_row(messgeraete[vde_key])

    def create_labeled_entry(self, row, label_text, section, option):
        """Erstellt ein Label und ein Entry-Widget in einer Zeile."""
        tk.Label(self, text=label_text).grid(row=row, column=0, padx=5, pady=5, sticky="w")
        entry = tk.Entry(self, width=40)
        entry.grid(row=row, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        entry.insert(0, self.settings.get_setting(section, option, ''))

        def save_entry_value_on_focus_out(event):
            self.save_entry_value(section, option, entry.get())

        entry.bind("<FocusOut>", save_entry_value_on_focus_out)

    def save_entry_value(self, section, option, value):
        """Speichert den Wert eines Entry-Widgets in den Einstellungen."""
        self.settings.set_setting(section, option, value)

    def save_all_settings(self):
        """Speichert alle Einstellungen auf einmal."""

        # Firmendaten speichern
        firma = self.settings.get_setting('FIRMA', 'firma', '')
        strasse = self.settings.get_setting('FIRMA', 'strasse', '')
        plz = self.settings.get_setting('FIRMA', 'plz', '')
        ort = self.settings.get_setting('FIRMA', 'ort', '')
        self.settings.set_company_data(firma, strasse, plz, ort)

        # Prüferdaten speichern
        pruefer_name = self.settings.get_setting('PRUEFER', 'name', '')
        self.settings.set_pruefer_name(pruefer_name)

        # Messgerätedaten speichern
        messgeraete = {}
        for i, temp_entry in enumerate(self.temp_entries, start=1):
            messgeraete[f'Temperaturmessgeraet_{i}'] = temp_entry.get()
        for i, vde_entry in enumerate(self.vde_entries, start=1):
            messgeraete[f'VDE-Messgeraet_{i}'] = vde_entry.get()
        self.settings.set_messgeraete(messgeraete)

        # Datenbankpfad speichern
        directory = self.pfad_entry.get()
        self.settings.set_setting('PATH', 'directory', directory)

        # Ausgewählte Datenbank speichern
        selected_db = self.database_combobox.get()
        self.settings.set_selected_database(selected_db)

        # Protokoll-Pfad speichern
        protokoll_path = self.protokoll_entry.get()
        self.settings.set_protokoll_path(protokoll_path)
