import tkinter as tk
import sqlite3
import webbrowser

from tkinter import ttk
from tkinter import messagebox
from detail_window import DetailWindow
from settings import Settings
from settings_window import SettingsWindow
from external_db import ExternalDatabase


class MainWindow(tk.Frame):
    """Klasse für das Hauptfenster der Anwendung."""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.settings = Settings("settings.ini")  # Einstellungen laden
        self.create_menu()
        self.create_widgets()

        # Datenbankpfad laden und Informationen anzeigen
        self.update_auftragsinformationen()
        if self.auftrags_dropdown.get():  # Wenn ein Auftrag ausgewählt ist
            self.on_auftrag_selected()  # Tabelle aktualisieren

        # Event-Handler für das Schließen des Fensters
        ###self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_menu(self):
        """Erstellt die Menüleiste."""
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Einstellungen", command=self.open_settings)
        filemenu.add_separator()
        filemenu.add_command(label="Beenden", command=self.on_close)
        menubar.add_cascade(label="Datei", menu=filemenu)

        infomenu = tk.Menu(menubar, tearoff=0)
        infomenu.add_command(label="Info", command=self.open_info_window)
        menubar.add_cascade(label="Hilfe", menu=infomenu)  # geändert

    def create_widgets(self):
        """Erstellt die Widgets des Hauptfensters."""

        # Dropdown für Auftragsauswahl
        self.auftrags_dropdown = ttk.Combobox(self, state="readonly", width=40)  # Breite auf 40 Zeichen eingestellt
        self.auftrags_dropdown.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.auftrags_dropdown.bind("<<ComboboxSelected>>", self.on_auftrag_selected)

        # Labels für Auftragsnummer, Kundennummer und Kunde
        self.auftragsnummer_label = ttk.Label(self, text="")
        self.auftragsnummer_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.kundennummer_label = ttk.Label(self, text="")
        self.kundennummer_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.kunde_label = ttk.Label(self, text="")
        self.kunde_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)

        # Datenbankpfad laden und Informationen anzeigen
        self.update_auftragsinformationen()

        # Waagentabelle
        self.waagen_table = ttk.Treeview(self, show="headings")
        self.waagen_table["columns"] = (
            "WJ-Nummer", "S/N", "Inventarnummer", "Hersteller", "Modell", "Standort", "Raum")
        for col in self.waagen_table["columns"]:
            self.waagen_table.heading(col, text=col)
            self.waagen_table.column(col, width=100, stretch=tk.YES)

        # Daten aus der Datenbank in die Tabelle einfügen
        self.update_waagen_table()

        # Spalten konfigurieren und Sortierung aktivieren
        for col in self.waagen_table["columns"]:
            self.waagen_table.heading(col, text=col, command=lambda _col=col: self.treeview_sort_column(_col,
                                                                                                        False))  # Sortierfunktion verknüpfen
            self.waagen_table.column(col, width=100, stretch=tk.YES)

        # Scrollbars für die Tabelle erstellen
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.waagen_table.yview)
        self.waagen_table.configure(yscrollcommand=vsb.set)

        # Tabelle und Scrollbars im Hauptfenster platzieren
        self.waagen_table.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")  # Vertikale Scrollbar rechts neben der Tabelle

        # Tabelle im Hauptfenster platzieren
        self.waagen_table.grid(row=0, column=0, sticky="nsew")

        # Hauptfenster konfigurieren
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Doppelklick-Event für die Tabelle
        self.waagen_table.bind("<Double-Button-1>", self.on_waage_double_click)

    def update_waagen_table(self, kundennummer=None):
        """Liest Waagendaten aus der Datenbank und aktualisiert die Tabelle basierend auf der Kundennummer."""
        for item in self.waagen_table.get_children():
            self.waagen_table.delete(item)

        db_path = self.settings.get_setting("DATABASE", "name")
        if db_path:
            db = ExternalDatabase(db_path)
            try:
                if kundennummer:  # Nur wenn eine Kundennummer übergeben wurde
                    waagen = db.get_waagen_by_kunde(kundennummer)
                else:
                    waagen = []  # Leere Liste, wenn keine Kundennummer
                for waage in waagen:
                    self.waagen_table.insert("", tk.END, values=waage)
            except sqlite3.OperationalError as e:
                print(f"Fehler beim Lesen der Datenbank: {e}")
                messagebox.showerror("Fehler",
                                     "Datenbank enthält nicht die erforderliche Tabelle 'kundenwaage' oder 'adress'")  # Fehlermeldung angepasst

    def on_waage_double_click(self, event):
        """Öffnet das Detailfenster beim Doppelklick auf eine Waage"""
        item = self.waagen_table.selection()[0]  # Ausgewähltes Element
        waage_data = self.waagen_table.item(item, "values")  # Waagendaten abrufen
        DetailWindow(self.master, waage_data[0], waage_data)  # Alle Waagendaten übergeben

    def treeview_sort_column(self, col, reverse):
        """Sortiert die Treeview nach der angegebenen Spalte, wobei numerische Werte korrekt behandelt werden."""
        try:
            # Versuche, die Werte als Zahlen zu interpretieren
            l = [(int(self.waagen_table.set(k, col)), k) for k in self.waagen_table.get_children('')]
        except ValueError:
            # Wenn nicht alle Werte Zahlen sind, sortiere lexikographisch
            l = [(self.waagen_table.set(k, col), k) for k in self.waagen_table.get_children('')]

        # Sortierung nach dem ersten Element des Tupels (Spaltenwert)
        l.sort(key=lambda t: t[0], reverse=reverse)  # Korrigierte Sortierung

        # Umordnen der Elemente in der Treeview
        for index, (val, k) in enumerate(l):
            self.waagen_table.move(k, '', index)

        # Sortierreihenfolge umkehren für den nächsten Klick
        self.waagen_table.heading(col, command=lambda _col=col: self.treeview_sort_column(_col, not reverse))

    def open_settings(self):
        """Öffnet das Einstellungsfenster."""
        settings_window = SettingsWindow(self.master, self.settings)
        settings_window.grab_set()

        # Auftragsnummer und Tabelle nach Schließen des Einstellungsfensters aktualisieren
        def update_and_destroy(event, main_window=self):
            main_window.update_auftragsinformationen()
            main_window.on_auftrag_selected()  # Ausgewählten Auftrag laden
            settings_window.destroy()

        settings_window.bind("<Destroy>", update_and_destroy)

    def open_info_window(self):  # neue Methode zum Öffnen des Info-Fensters
        """Öffnet das Info-Fenster."""
        info_window = tk.Toplevel(self.master)
        info_window.title("Info")
        info_window.geometry("250x150")

        # Inhalt des Info-Fensters
        ttk.Label(info_window, text="Versionsnummer: 0.9.1").pack(pady=5)
        ttk.Label(info_window, text="Herausgegeben von: Waagen-Jöhnk KG").pack(pady=5)
        ttk.Label(info_window, text="Kontakt: info@waagen-joehnk.de").pack(pady=5)
        ttk.Label(info_window, text="Webseite:").pack(pady=5)

        # Link zur Webseite
        website_link = ttk.Label(info_window, text="www.waagen-joehnk.de", foreground="blue", cursor="hand2")
        website_link.pack(pady=5)
        website_link.bind("<Button-1>", lambda e: webbrowser.open_new("http://www.waagen-joehnk.de"))

        # Zentrieren des Fensters
        info_window.update_idletasks()
        screen_width = info_window.winfo_screenwidth()
        screen_height = info_window.winfo_screenheight()
        window_width = info_window.winfo_width()
        window_height = info_window.winfo_height()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        info_window.geometry(f"+{x}+{y}")

    def update_auftragsinformationen(self):
        """Liest Auftragsinformationen aus der Datenbank und aktualisiert das Dropdown und die Labels."""
        db_path = self.settings.get_setting("DATABASE", "name")
        if db_path:
            db = ExternalDatabase(db_path)
            try:
                auftraege = db.get_auftragsinformationen()
                if auftraege:
                    # Dropdown-Werte werden als "Auftragsnummer - Firmenname" formatiert
                    self.auftrags_dropdown["values"] = [f"{auftrag[0]} - {auftrag[1]} - {auftrag[2]}" for auftrag in
                                                        auftraege]
                    self.auftrags_dropdown.current(0)
                else:
                    self.auftragsnummer_label.config(text="Keine Aufträge gefunden")
                    self.kundennummer_label.config(text="")
                    self.kunde_label.config(text="")
            except sqlite3.OperationalError as e:
                print(f"Fehler beim Lesen der Datenbank: {e}")
                self.auftragsnummer_label.config(text="Datenbank enthält nicht die erforderlichen Tabellen")
                self.kundennummer_label.config(text="")
                self.kunde_label.config(text="")
        else:
            self.auftragsnummer_label.config(text="Keine Datenbank ausgewählt")
            self.kundennummer_label.config(text="")
            self.kunde_label.config(text="")

    def on_auftrag_selected(self, event=None):
        """Aktualisiert die Labels und die Waagentabelle basierend auf dem ausgewählten Auftrag."""
        selected_value = self.auftrags_dropdown.get()  # Ausgewählter Wert (z.B. "12345 - Firma XYZ")
        auftragsnummer = selected_value.split(" - ")[0]  # Auftragsnummer extrahieren
        db_path = self.settings.get_setting("DATABASE", "name")
        if db_path and auftragsnummer:
            db = ExternalDatabase(db_path)
            kundennummer, kunde = db.get_auftragsdaten(auftragsnummer)
            if kundennummer and kunde:
                self.auftragsnummer_label.config(text=f"Auftragsnummer: {auftragsnummer}")
                self.kundennummer_label.config(text=f"Kundennummer: {kundennummer}")
                self.kunde_label.config(text=f"Kunde: {kunde}")
            else:
                self.auftragsnummer_label.config(text=f"Auftragsnummer: {auftragsnummer}")
                self.kundennummer_label.config(text="Kunde nicht gefunden")
                self.kunde_label.config(text="")

            # Tabelle aktualisieren
            self.update_waagen_table(kundennummer)  # Kundennummer übergeben
        else:
            self.auftragsnummer_label.config(text="Keine Datenbank oder Auftrag ausgewählt")
            self.kundennummer_label.config(text="")
            self.kunde_label.config(text="")
            self.update_waagen_table(None)  # Tabelle leeren

    def on_close(self):
        """Beendet die Anwendung nach Bestätigung."""
        if messagebox.askokcancel("Beenden",
                                  "Möchten Sie die Anwendung wirklich beenden, eventuelle Eingaben werden nicht gespeichert?"):
            self.master.destroy()
