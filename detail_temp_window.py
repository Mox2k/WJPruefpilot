import os
import tkinter as tk
import subprocess

from tkinter import ttk
from tkinter import messagebox
from tkinter import font
from pdf_temp_generator import PDFGeneratorTemp
from datetime import date
from settings import Settings


class DetailTempWindow(tk.Toplevel):
    """Klasse für das Detailfenster einer Waage."""

    def __init__(self, master=None, waage_id=None, waage_data=None):
        super().__init__(master)
        self.waage_id = waage_id
        self.waage_data = waage_data  # Daten der ausgewählten Waage speichern
        self.title(f"Tempreatur-Justage für Waage {waage_id}")
        self.ist_temp1_entry = None  # Eingabefelder als Instanzvariablen initialisieren
        self.soll_temp1_entry = None
        self.ist_temp2_entry = None
        self.soll_temp2_entry = None
        self.temp_frame = None
        self.create_widgets()
        self.resizable(False, False)  # Größenänderung deaktivieren

    def create_widgets(self):
        """Erstellt die Widgets des Detailfensters."""

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        for i in range(11):
            self.rowconfigure(i, weight=1)

        explanation_font = font.Font(size=8)

        # --- Waagendetails ---
        details_frame = ttk.LabelFrame(self, text="Waagendetails")
        details_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="nsew")

        # Labels für Hersteller, Modell und Seriennummer # neu hinzugefügt
        ttk.Label(details_frame, text=f"Hersteller: {self.waage_data[3]}").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Label(details_frame, text=f"Modell: {self.waage_data[4]}").grid(row=0, column=1, sticky="w", padx=5, pady=5)
        ttk.Label(details_frame, text=f"Seriennummer: {self.waage_data[1]}").grid(row=0, column=2, sticky="w", padx=5, pady=5)

        # --- Temperaturjustage ---
        self.temp_frame = ttk.LabelFrame(self, text="Temperaturjustage")
        self.temp_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        for i in range(8):
            self.temp_frame.rowconfigure(i, weight=1)

        # Ist-Temperatur 1
        ttk.Label(self.temp_frame, text="Ist-Temperatur 1:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.ist_temp1_entry = ttk.Entry(self.temp_frame)
        self.ist_temp1_entry.insert(0, "100")  # Eingabefeld mit Wert vorausfüllen
        self.ist_temp1_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        ttk.Label(self.temp_frame, text="°C", font=explanation_font).grid(row=0, column=2, sticky="w")
        ttk.Label(self.temp_frame, text="Das ist eine Erklärung", font=explanation_font, foreground="gray").grid(
            row=1, column=0, columnspan=3, sticky="w", padx=5, pady=(0, 5))

        # Soll-Temperatur 1
        ttk.Label(self.temp_frame, text="Soll-Temperatur 1:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.soll_temp1_entry = ttk.Entry(self.temp_frame)
        self.soll_temp1_entry.insert(0, "100")  # Eingabefeld mit Wert vorausfüllen
        self.soll_temp1_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        ttk.Label(self.temp_frame, text="°C", font=explanation_font).grid(row=2, column=2, sticky="w")
        ttk.Label(self.temp_frame, text="Das ist eine Erklärung", font=explanation_font, foreground="gray").grid(
            row=3, column=0, columnspan=3, sticky="w", padx=5, pady=(0, 5))

        # Ist-Temperatur 2
        ttk.Label(self.temp_frame, text="Ist-Temperatur 2:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.ist_temp2_entry = ttk.Entry(self.temp_frame)
        self.ist_temp2_entry.insert(0, "160")  # Eingabefeld mit Wert vorausfüllen
        self.ist_temp2_entry.grid(row=4, column=1, sticky="ew", padx=5, pady=5)
        ttk.Label(self.temp_frame, text="°C", font=explanation_font).grid(row=4, column=2, sticky="w")
        ttk.Label(self.temp_frame, text="Das ist eine Erklärung", font=explanation_font, foreground="gray").grid(
            row=5, column=0, columnspan=3, sticky="w", padx=5, pady=(0, 5))

        # Soll-Temperatur 2
        ttk.Label(self.temp_frame, text="Soll-Temperatur 2:").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.soll_temp2_entry = ttk.Entry(self.temp_frame)
        self.soll_temp2_entry.insert(0, "160")  # Eingabefeld mit Wert vorausfüllen
        self.soll_temp2_entry.grid(row=6, column=1, sticky="ew", padx=5, pady=5)
        ttk.Label(self.temp_frame, text="°C", font=explanation_font).grid(row=6, column=2, sticky="w")
        ttk.Label(self.temp_frame, text="Das ist eine Erklärung", font=explanation_font, foreground="gray").grid(
            row=7, column=0, columnspan=3, sticky="w", padx=5, pady=(0, 5))

        # Umgebungstemperatur
        ttk.Label(self.temp_frame, text="Umgebungstemperatur:").grid(row=8, column=0, sticky="w", padx=5, pady=5)
        self.umgebung_temp_entry = ttk.Entry(self.temp_frame)
        self.umgebung_temp_entry.insert(0, "21")  # Standardwert 21°C
        self.umgebung_temp_entry.grid(row=8, column=1, sticky="ew", padx=5, pady=5)
        ttk.Label(self.temp_frame, text="°C", font=explanation_font).grid(row=8, column=2, sticky="w")

        # --- Datum der Prüfung --- (geändert)
        ttk.Label(self.temp_frame, text="Datum der Prüfung:").grid(row=9, column=0, sticky="w", padx=5,
                                                                   pady=5)  # row=11
        self.pruefdatum_entry = ttk.Entry(self.temp_frame)
        self.pruefdatum_entry.insert(0, date.today().strftime("%d.%m.%Y"))  # Heutiges Datum als Standard
        self.pruefdatum_entry.grid(row=9, column=1, sticky="ew", padx=5, pady=5)

        # --- Bemerkungen ---
        ttk.Label(self.temp_frame, text="Bemerkungen:").grid(row=10, column=0, sticky="nw", padx=5, pady=5)
        self.bemerkungen_text = tk.Text(self.temp_frame, width=30, height=3)
        self.bemerkungen_text.grid(row=10, column=1, sticky="ew", padx=5, pady=5)

        # Dropdown-Menü für Temperaturmessgerät
        ttk.Label(self.temp_frame, text="Temperaturmessgerät:").grid(row=11, column=0, sticky="w", padx=5, pady=5)
        self.temp_messgeraet_var = tk.StringVar(
            value=self.get_messgeraet_options("temperaturmessgeraet")[0])  # Erster Wert als Standard
        temp_messgeraet_options = self.get_messgeraet_options("temperaturmessgeraet")
        self.temp_messgeraet_dropdown = ttk.Combobox(self.temp_frame, textvariable=self.temp_messgeraet_var,
                                                     values=temp_messgeraet_options)

        self.temp_messgeraet_dropdown.grid(row=11, column=1, sticky="ew", padx=5, pady=5)

        ttk.Button(self.temp_frame, text="Tempjustage-Prüfprotokoll drucken",
                   command=self.print_tempjustage_protocol).grid(row=12, column=0, columnspan=3, pady=(10, 5), sticky="ew")

        ttk.Label(self.temp_frame,
                  text="Mit den Pfeiltasten ↕ können die Werte um 1 erhöht/verringert werden, mit den Pfeiltasten ↔ um 0.1.",
                  font=explanation_font, foreground="gray").grid(
            row=13, column=0, columnspan=2, sticky="w", padx=5, pady=(0, 5))

        # --- Pfeiltasten-Navigation hinzufügen ---
        for entry in [self.ist_temp1_entry, self.soll_temp1_entry, self.ist_temp2_entry, self.soll_temp2_entry, self.umgebung_temp_entry]:
            entry.bind("<Up>", lambda event, e=entry: self.change_value(e, 1))  # Aufwärtspfeil: Wert erhöhen
            entry.bind("<Down>", lambda event, e=entry: self.change_value(e, -1))  # Abwärtspfeil: Wert verringern
            entry.bind("<Right>",
                       lambda event, e=entry: self.change_value(e, 0.1))  # Rechter Pfeil: Wert um 0.1 erhöhen
            entry.bind("<Left>", lambda event, e=entry: self.change_value(e, -0.1))  # Linker Pfeil: Wert um 0.1 verringern

    def change_value(self, entry, delta):
        """Ändert den Wert im Eingabefeld um den angegebenen Betrag, mit korrekter Rundung."""
        try:
            current_value = float(entry.get())
            new_value = current_value + delta

            # Nachkommastelle nur bei gedrückter Shift-Taste anzeigen, mit korrekter Rundung
            if delta == 0.1 or delta == -0.1:
                new_value_str = f"{new_value:.1f}"  # Formatieren auf eine Dezimalstelle als String
                new_value = float(new_value_str)  # Zurück in float konvertieren
                entry.delete(0, tk.END)
                entry.insert(0, new_value)
            else:
                entry.delete(0, tk.END)
                entry.insert(0, int(new_value))  # Konvertiere in int, um Nachkommastelle zu entfernen
        except ValueError:
            pass  # Ignoriere ungültige Eingaben

    def get_messgeraet_options(self, messgeraet_type):
        """Liest die verfügbaren Messgeräte aus der settings.ini."""
        from settings import Settings
        settings = Settings()  # Create a Settings object
        options = []
        i = 1
        while True:
            key = f"{messgeraet_type}_{i}"
            if key in settings.data:  # Access settings from the data attribute
                options.append(settings.data[key])
                i += 1
            else:
                break
        return options

    def print_tempjustage_protocol(self):
        """Generiert das Tempjustage-Prüfprotokoll."""
        pdf_generator = PDFGeneratorTemp()
        pdf_generator.add_title("Tempjustage-Prüfprotokoll")
        pdf_generator.add_company_and_inspector_data()
        pdf_generator.add_waagen_data(self.waage_data)

        # Prüfdatum und Bemerkungen hinzufügen
        pruefdatum = self.pruefdatum_entry.get()
        bemerkungen = self.bemerkungen_text.get("1.0", tk.END).strip()

        # Temperaturjustage-Daten hinzufügen (Zugriff auf Instanzvariablen)
        temp_data = {
            'ist_temp1': self.ist_temp1_entry.get(),
            'soll_temp1': self.soll_temp1_entry.get(),
            'ist_temp2': self.ist_temp2_entry.get(),
            'soll_temp2': self.soll_temp2_entry.get(),
            'temp_messgeraet': self.temp_messgeraet_var.get(),
            'umgebung_temp': self.umgebung_temp_entry.get()
        }
        pdf_generator.add_tempjustage_data(temp_data)
        pdf_generator.add_pruefdatum_bemerkungen(pruefdatum, bemerkungen)

        # #geändert: Kalibrierscheinnummer generieren
        calibration_number = pdf_generator.get_calibration_number()

        # #neu hinzugefügt: Protokoll-Speicherpfad aus den Einstellungen holen
        settings = Settings()
        protokoll_path = settings.get_protokoll_path()

        # #geändert: PDF-Dateiname mit Kalibrierscheinnummer erstellen
        pdf_filename = f"{calibration_number}.pdf"
        pdf_path = os.path.join(protokoll_path, pdf_filename)

        # #geändert: PDF generieren und speichern
        pdf_generator.generate_pdf(pdf_path)

        try:
            if os.name == 'nt':  # Für Windows
                os.startfile(pdf_path)
            elif os.name == 'posix':  # Für macOS und Linux
                subprocess.call(('open', pdf_path))
        except Exception as e:
            messagebox.showerror("Fehler", f"Konnte PDF nicht öffnen: {str(e)}")

        #messagebox.showinfo("Hinweis", f"Tempjustage-Prüfprotokoll wurde erstellt und als {pdf_filename} gespeichert.")