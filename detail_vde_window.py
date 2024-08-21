import os
import subprocess
import tkinter as tk

from tkinter import ttk
from tkinter import messagebox
from tkinter import font
from pdf_vde_generator import PDFGeneratorVDE
from datetime import date
from settings import Settings


class DetailVDEWindow(tk.Toplevel):
    """Klasse für das Detailfenster einer Waage."""

    def __init__(self, master=None, waage_id=None, waage_data=None, db=None):
        super().__init__(master)
        self.db = db
        self.waage_id = waage_id
        self.kundennummer = self.extract_kundennummer(waage_id)
        self.waage_data = waage_data  # Daten der ausgewählten Waage speichern
        self.title(f"VDE-Prüfung für Waage {waage_id}")
        self.schutzklasse_var = None
        self.rpe_entry = None
        self.riso_entry = None
        self.ipe_ib_entry = None
        self.vde_frame = None
        self.vde_var = tk.IntVar(value=2)  # Standardmäßig VDE 702 ausgewählt
        self.pruefungsart_var = tk.IntVar(value=3)  # Standardmäßig Wiederholungsprüfung

        self.create_widgets()
        self.resizable(False, False)

    def create_widgets(self):
        """Erstellt die Widgets des Detailfensters."""

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        for i in range(11):
            self.rowconfigure(i, weight=1)

        explanation_font = font.Font(size=8)

        # ///////// --- Waagendetails --- /////////
        details_frame = ttk.LabelFrame(self, text="Waagendetails")
        details_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=(10, 0), sticky="nsew")

        # Labels für Hersteller, Modell und Seriennummer
        ttk.Label(details_frame, text=f"Hersteller: {self.waage_data[3]}").grid(row=0, column=0, sticky="w", padx=5,
                                                                                pady=5)
        ttk.Label(details_frame, text=f"Modell: {self.waage_data[4]}").grid(row=0, column=1, sticky="w", padx=5, pady=5)
        ttk.Label(details_frame, text=f"Seriennummer: {self.waage_data[1]}").grid(row=0, column=2, sticky="w", padx=5,
                                                                                  pady=5)

        # ///////// --- VDE-Prüfung --- /////////
        self.vde_frame = ttk.LabelFrame(self, text="VDE-Prüfung")
        self.vde_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # --- Elektrische Daten (inklusive VDE-Prüfungsart und Schutzklasse) ---
        elektrische_daten_frame = ttk.LabelFrame(self.vde_frame, text="Elektrische Daten")
        elektrische_daten_frame.grid(row=0, column=0, columnspan=1, padx=10, pady=10, sticky="nsew")

        # VDE-Prüfungsart Frame
        vde_pruefungsart_frame = ttk.LabelFrame(elektrische_daten_frame, text="Prüfungsart")
        vde_pruefungsart_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # VDE-Prüfung
        ttk.Label(vde_pruefungsart_frame, text="VDE").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        vde_pruefung_frame = ttk.Frame(vde_pruefungsart_frame)
        vde_pruefung_frame.grid(row=0, column=1, sticky="w")

        ttk.Radiobutton(vde_pruefung_frame, text="701",
                        variable=self.vde_var, value=1, command=self.update_pruefungsart).pack(side="left", padx=5)
        ttk.Radiobutton(vde_pruefung_frame, text="702",
                        variable=self.vde_var, value=2, command=self.update_pruefungsart).pack(side="left", padx=5)

        # Prüfungsart
        ttk.Label(vde_pruefungsart_frame, text="Prüfungsart:").grid(row=1, column=0, sticky="nw", padx=5, pady=5)
        pruefungsart_frame = ttk.Frame(vde_pruefungsart_frame)
        pruefungsart_frame.grid(row=1, column=1, sticky="w")

        self.neugeraet_rb = ttk.Radiobutton(pruefungsart_frame, text="Neugerät", variable=self.pruefungsart_var,
                                            value=0)
        self.neugeraet_rb.grid(row=0, column=0, sticky="w", padx=5, pady=2)

        self.erweiterung_rb = ttk.Radiobutton(pruefungsart_frame, text="Erweiterung", variable=self.pruefungsart_var,
                                              value=1)
        self.erweiterung_rb.grid(row=0, column=1, sticky="w", padx=5, pady=2)

        self.instandsetzung_rb = ttk.Radiobutton(pruefungsart_frame, text="Instandsetzung",
                                                 variable=self.pruefungsart_var, value=2)
        self.instandsetzung_rb.grid(row=1, column=0, sticky="w", padx=5, pady=2)

        self.wiederholungspruefung_rb = ttk.Radiobutton(pruefungsart_frame, text="Wiederholungsprüfung",
                                                        variable=self.pruefungsart_var, value=3)
        self.wiederholungspruefung_rb.grid(row=1, column=1, sticky="w", padx=5, pady=2)

        # Schutzklasse
        ttk.Label(elektrische_daten_frame, text="Schutzklasse:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        radio_frame = ttk.Frame(elektrische_daten_frame)
        radio_frame.grid(row=1, column=1, sticky="w")

        self.schutzklasse_var = tk.StringVar(value="2")  # Schutzklasse II als Standardwert
        ttk.Radiobutton(radio_frame, text="I", variable=self.schutzklasse_var, value="1",
                        command=self.update_input_fields).pack(side="left")
        ttk.Radiobutton(radio_frame, text="II", variable=self.schutzklasse_var, value="2",
                        command=self.update_input_fields).pack(side="left")
        ttk.Radiobutton(radio_frame, text="III", variable=self.schutzklasse_var, value="3",
                        command=self.update_input_fields).pack(side="left")

        # Nennspannung
        ttk.Label(elektrische_daten_frame, text="Nennspannung (V):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.nennspannung_entry = ttk.Entry(elektrische_daten_frame)
        self.nennspannung_entry.insert(0, "230")  # Standardwert 230V
        self.nennspannung_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        # Nennstrom
        ttk.Label(elektrische_daten_frame, text="Nennstrom (A):").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.nennstrom_entry = ttk.Entry(elektrische_daten_frame)
        self.nennstrom_entry.insert(0, "-")  # Standardwert -
        self.nennstrom_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        # Nennleistung
        ttk.Label(elektrische_daten_frame, text="Nennleistung (W):").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.nennleistung_entry = ttk.Entry(elektrische_daten_frame)
        self.nennleistung_entry.insert(0, "-")  # Standardwert -
        self.nennleistung_entry.grid(row=4, column=1, sticky="ew", padx=5, pady=5)

        # Frequenz
        ttk.Label(elektrische_daten_frame, text="Frequenz (Hz):").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.frequenz_entry = ttk.Entry(elektrische_daten_frame)
        self.frequenz_entry.insert(0, "50")  # Standardwert 50 Hz
        self.frequenz_entry.grid(row=5, column=1, sticky="ew", padx=5, pady=5)

        # cosPhi
        ttk.Label(elektrische_daten_frame, text="cosPhi:").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.cosphi_entry = ttk.Entry(elektrische_daten_frame)
        self.cosphi_entry.insert(0, "1")  # Standardwert 1
        self.cosphi_entry.grid(row=6, column=1, sticky="ew", padx=5, pady=5)

        self.update_pruefungsart()

        tk.Message(elektrische_daten_frame,
                   text="Schutzleiterwiderstand (RPE): Widerstand zwischen Schutzleiteranschluss und berührbaren Metallteilen.",
                   width=350, font=explanation_font, foreground="gray").grid(  # geändert
            row=0, column=2, sticky="w", padx=5, pady=(5.0))  # geändert
        tk.Message(elektrische_daten_frame,
                   text="Isolationswiderstand (RISO): Widerstand zwischen aktiven Teilen und berührbaren Metallteilen.",
                   width=350, font=explanation_font, foreground="gray").grid(  # geändert
            row=1, column=2, sticky="w", padx=5, pady=(5.0))  # geändert
        tk.Message(elektrische_daten_frame,
                   text="Schutzleiterstrom (IPE): Strom, der im Fehlerfall über den Schutzleiter fließt.",
                   width=350, font=explanation_font, foreground="gray").grid(  # geändert
            row=2, column=2, sticky="w", padx=5, pady=(5.0))  # geändert
        tk.Message(elektrische_daten_frame,
                   text="Berührungsstrom (IB): Strom, der im Fehlerfall über einen Menschen fließen kann.",
                   width=350, font=explanation_font, foreground="gray").grid(  # geändert
            row=3, column=2, sticky="w", padx=5, pady=(5.0))  # geändert
        tk.Message(elektrische_daten_frame,
                   text="Betriebsmittel der Schutzklasse I sind über einen Schutzleiter mit dem Erdpotential verbunden, um im Fehlerfall einen Stromfluss zur Erde zu ermöglichen und so vor gefährlicher Berührungsspannung zu schützen. Geräte der SKI haben einen Schutzkontakt-Stecker!",
                   width=350, font=explanation_font, foreground="gray").grid(  # geändert
            row=4, column=2, sticky="w", padx=5, pady=(5.0))  # geändert
        tk.Message(elektrische_daten_frame,
                   text="Betriebsmittel der Schutzklasse II haben eine doppelte oder verstärkte Isolierung, um gefährliche Berührungsspannungen zu verhindern. Sie benötigen keinen Schutzleiter und haben einen maximalen Berührstrom von 0,5 mA. Geräte der SK II haben meist einen Stecker ohne Schutzleiter.",
                   width=350, font=explanation_font, foreground="gray").grid(  # geändert
            row=5, column=2, sticky="w", padx=5, pady=(5.0))  # geändert
        tk.Message(elektrische_daten_frame,
                   text="Betriebsmittel der Schutzklasse III arbeiten mit ungefährlicher Kleinspannung (SELV/PELV) und sind daher durch ihre Bauart vor gefährlichen Stromschlägen geschützt. Geräte der SK III (SELV - Batterien/Akkus, PELV - Netzteile, Ladegeräte).",
                   width=350, font=explanation_font, foreground="gray").grid(  # geändert
            row=6, column=2, sticky="w", padx=5, pady=(5.0))  # geändert

        # ///////// --- Visuelle Prüfung --- /////////
        visuelle_pruefung_frame = ttk.LabelFrame(self.vde_frame, text="Visuelle Prüfung")
        visuelle_pruefung_frame.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")  # geändert

        # Checkboxen für die visuelle Prüfung
        checkbox_options = [
            "Typenschild/Warnhinweis/Kennzeichnungen",
            "Gehäuse/Schutzabdeckungen",
            "Anschlussleitung/stecker,Anschlussklemmen und -adern",
            "Biegeschutz/Zugentlastung",
            "Leitungshalterungen, Sicherungshalter, usw.",
            "Kühlluftöffnungen/Luftfilter",
            "Schalter, Steuer, Einstell- und Sicherheitsvorrichtungen",
            "Bemessung der zugänglichen Gerätesicherung",
            "Beuteile und Baugruppen",
            "Anzeichen von Überlastung/unsachgemäßem Gebrauch",
            "Sicherheitsbeeinträchtigende Verschmutzung/Korrission/Alterung",
            "Mechanische Gefährdung",
            "Unzulässige Eingriffe und Änderungen"
        ]

        self.visuelle_pruefung_vars = {}

        for i, option in enumerate(checkbox_options):
            var = tk.IntVar(value=1)  # Standardwert auf 1 setzen
            self.visuelle_pruefung_vars[option] = var
            cb = ttk.Checkbutton(visuelle_pruefung_frame, text=option, variable=var)
            cb.grid(row=i, column=0, sticky="w", padx=5, pady=2)

        # ///////// --- Elektrische Prüfung --- /////////
        elektrische_pruefung_frame = ttk.LabelFrame(self.vde_frame, text="Elektrische Prüfung")
        elektrische_pruefung_frame.grid(row=1, column=0, padx=10, pady=10,  # geändert
                                        sticky="nsew")

        # --- Schutzleiterwiderstand ---
        ttk.Label(elektrische_pruefung_frame, text="Schutzleiterwiderstand (RPE): ≤").grid(row=0, column=0, sticky="w",
                                                                                         padx=5,
                                                                                         pady=5)
        self.rpe_entry = ttk.Entry(elektrische_pruefung_frame)
        self.rpe_entry.insert(0, "0.3" if self.schutzklasse_var.get() == "1" else "0")
        self.rpe_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        ttk.Label(elektrische_pruefung_frame, text="Bemerkungen:").grid(row=0, column=2, sticky="w", padx=5,
                                                                        pady=5)
        self.rpe_bemerkungen_entry = ttk.Entry(elektrische_pruefung_frame)
        self.rpe_bemerkungen_entry.grid(row=0, column=3, sticky="ew", padx=5, pady=5)
        self.rpe_check_var = tk.IntVar(value=1)
        ttk.Checkbutton(elektrische_pruefung_frame, text="i.O.", variable=self.rpe_check_var).grid(row=0, column=4,
                                                                                                   sticky="w")
        self.rpe_entry.bind("<KeyRelease>", self.check_values)  # Ereignisbehandlung für Tastatureingaben hinzufügen

        # --- Isolationswiderstand ---
        ttk.Label(elektrische_pruefung_frame, text="Isolationswiderstand (RISO): ≥").grid(row=1, column=0, sticky="w",
                                                                                        padx=5,
                                                                                        pady=5)
        self.riso_entry = ttk.Entry(elektrische_pruefung_frame)
        self.riso_entry.insert(0, "19.99")
        self.riso_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        ttk.Label(elektrische_pruefung_frame, text="Bemerkungen:").grid(row=1, column=2, sticky="w", padx=5,
                                                                        pady=5)
        self.riso_bemerkungen_entry = ttk.Entry(elektrische_pruefung_frame)
        self.riso_bemerkungen_entry.grid(row=1, column=3, sticky="ew", padx=5, pady=5)
        self.riso_check_var = tk.IntVar(value=1)
        ttk.Checkbutton(elektrische_pruefung_frame, text="i.O.", variable=self.riso_check_var).grid(row=1, column=4,
                                                                                                    sticky="w")
        self.riso_entry.bind("<KeyRelease>", self.check_values)  # Ereignisbehandlung für Tastatureingaben hinzufügen

        # --- Schutzleiterstrom ---
        ttk.Label(elektrische_pruefung_frame, text="Schutzleiterstrom (IPE): ≤").grid(row=2, column=0, sticky="w", padx=5,
                                                                                    pady=5)
        self.ipe_entry = ttk.Entry(elektrische_pruefung_frame)
        self.ipe_entry.insert(0, "3.5" if self.schutzklasse_var.get() == "1" else "-")
        self.ipe_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        ttk.Label(elektrische_pruefung_frame, text="Bemerkungen:").grid(row=2, column=2, sticky="w", padx=5,
                                                                        pady=5)
        self.ipe_bemerkungen_entry = ttk.Entry(elektrische_pruefung_frame)
        self.ipe_bemerkungen_entry.grid(row=2, column=3, sticky="ew", padx=5, pady=5)
        self.ipe_check_var = tk.IntVar(value=1)
        ttk.Checkbutton(elektrische_pruefung_frame, text="i.O.", variable=self.ipe_check_var).grid(row=2, column=4,
                                                                                                   sticky="w")
        self.ipe_entry.bind("<KeyRelease>", self.check_values)  # Ereignisbehandlung für Tastatureingaben hinzufügen

        # --- Berührungsstrom ---
        ttk.Label(elektrische_pruefung_frame, text="Berührungsstrom (IB): ≤").grid(row=3, column=0, sticky="w", padx=5,
                                                                                 pady=5)
        self.ib_entry = ttk.Entry(elektrische_pruefung_frame)
        self.ib_entry.insert(0, "0.10" if self.schutzklasse_var.get() == "2" else "-")
        self.ib_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        ttk.Label(elektrische_pruefung_frame, text="Bemerkungen:").grid(row=3, column=2, sticky="w", padx=5,
                                                                        pady=5)
        self.ib_bemerkungen_entry = ttk.Entry(elektrische_pruefung_frame)
        self.ib_bemerkungen_entry.grid(row=3, column=3, sticky="ew", padx=5, pady=5)
        self.ib_check_var = tk.IntVar(value=1)
        ttk.Checkbutton(elektrische_pruefung_frame, text="i.O.", variable=self.ib_check_var).grid(row=3, column=4, sticky = "w")
        self.ib_entry.bind("<KeyRelease>", self.check_values)  # Ereignisbehandlung für Tastatureingaben hinzufügen

        self.update_input_fields()

        # --- Funktion des Gerätes ---
        self.funktion_check_var = tk.IntVar(value=1)
        ttk.Checkbutton(elektrische_pruefung_frame, text="Funktion des Gerätes i.O.",
                        variable=self.funktion_check_var).grid(row=4, column=0, columnspan=2,
                                                               sticky="w")

        # ///////// --- Abschluss Frame --- /////////
        abschluss_frame = ttk.LabelFrame(self.vde_frame, text="Prüfdetails")
        abschluss_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # --- Datum der Prüfung ---
        ttk.Label(abschluss_frame, text="Datum der Prüfung:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.pruefdatum_entry = ttk.Entry(abschluss_frame)
        self.pruefdatum_entry.insert(0, date.today().strftime("%d.%m.%Y"))  # Heutiges Datum als Standard
        self.pruefdatum_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # --- Bemerkungen ---
        ttk.Label(abschluss_frame, text="Bemerkungen:").grid(row=1, column=0, sticky="nw", padx=5, pady=5)
        self.bemerkungen_text = tk.Text(abschluss_frame, width=30, height=3)
        self.bemerkungen_text.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        # Dropdown-Menü für VDE-Messgerät
        ttk.Label(abschluss_frame, text="VDE-Messgerät:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.vde_messgeraet_var = tk.StringVar(
            value=self.get_messgeraet_options("vde-messgeraet")[0])  # Erster Wert als Standard
        vde_messgeraet_options = self.get_messgeraet_options("vde-messgeraet")
        self.vde_messgeraet_dropdown = ttk.Combobox(abschluss_frame, textvariable=self.vde_messgeraet_var,
                                                    values=vde_messgeraet_options)
        self.vde_messgeraet_dropdown.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        ttk.Button(abschluss_frame, text="VDE-Prüfprotokoll drucken", command=self.print_vde_protocol).grid(row=3,
                                                                                                            column=0,
                                                                                                            columnspan=2,
                                                                                                            pady=(
                                                                                                                10, 5),
                                                                                                            sticky="ew")
        ttk.Label(self.vde_frame,
                  text="Mit den Pfeiltasten ↕ können die Werte um 1 erhöht/verringert (+STRG *10) werden, mit den Pfeiltasten ↔ um 0.1 (+STRG /10).",
                  font=explanation_font, foreground="gray").grid(
            row=7, column=0, columnspan=2, sticky="w", padx=5, pady=(0, 5))

        # ///////// --- Pfeiltasten-Navigation für ALLE Entry-Widgets hinzufügen --- /////////
        all_entries = [
            self.nennspannung_entry, self.nennstrom_entry, self.nennleistung_entry,
            self.frequenz_entry, self.cosphi_entry, self.rpe_entry, self.riso_entry,
            self.ipe_entry, self.ib_entry, self.pruefdatum_entry,  # Prüfdatum hinzugefügt
            self.rpe_bemerkungen_entry, self.riso_bemerkungen_entry,
            self.ipe_bemerkungen_entry, self.ib_bemerkungen_entry
        ]

        for entry in all_entries:
            entry.bind("<Up>", lambda event, e=entry: self.change_value(e, 1, event))
            entry.bind("<Down>", lambda event, e=entry: self.change_value(e, -1, event))
            entry.bind("<Left>", lambda event, e=entry: self.change_value(e, 0, event))  # Neu
            entry.bind("<Right>", lambda event, e=entry: self.change_value(e, 0, event))  # Neu

        # --- Tab-Navigation verbessern ---
        for widget in self.winfo_children():  # Alle untergeordneten Widgets durchgehen
            if isinstance(widget, ttk.Entry):
                widget.configure(takefocus=True)  # Sicherstellen, dass Entry-Widgets den Fokus annehmen können

    @staticmethod
    def get_modifiers(event):
        """Ermittelt den Status von Shift und Strg."""
        return (event.state & 0x0004) != 0, (event.state & 0x0002) != 0

    def update_input_fields(self):
        """Aktualisiert die Eingabefelder basierend auf der ausgewählten Schutzklasse."""
        schutzklasse = self.schutzklasse_var.get()

        # Aktivierung/Deaktivierung der Eingabefelder
        self.rpe_entry.config(state="normal" if schutzklasse in ["1", "2"] else "disabled")
        self.riso_entry.config(state="normal")  # Immer aktiv
        self.ipe_entry.config(state="normal" if schutzklasse == "1" else "disabled")
        self.ib_entry.config(state="normal" if schutzklasse == "2" else "disabled")

        # Standardwerte nach Schutzklasse setzen und sicherstellen, dass inaktive Felder "-" enthalten
        fields_to_update = {
            "1": {"rpe": "0.3", "riso": "1", "ipe": "3.5", "ib": "-"},
            "2": {"rpe": "-", "riso": "2", "ipe": "-", "ib": "0.5"},
            "3": {"rpe": "-", "riso": "0.25", "ipe": "-", "ib": "-"},
        }

        for field_name, value in fields_to_update[schutzklasse].items():
            entry = getattr(self, f"{field_name}_entry")
            entry.config(state='normal')  # setze das entry auf normal, damit der wert geändert werden kann
            entry.delete(0, tk.END)
            entry.insert(0, value)
            if value == "-":  # deaktiviere das entry wieder, wenn der wert "-" ist
                entry.config(state='disabled')

        self.check_values()  # Aufruf der neuen Funktion, um die Checkbuttons nach dem Aktualisieren der Eingabefelder zu überprüfen

    def change_value(self, entry, increment, event=None):
        try:
            current_value = float(entry.get())

            shift_pressed, ctrl_pressed = DetailVDEWindow.get_modifiers(event) if event else (False, False)

            if event.keysym == "Left":
                # Nachkommastelle verringern (Pfeil nach links)
                if shift_pressed:
                    increment = -0.01  # Zweite Nachkommastelle
                    format_string = "{:.2f}"  # Zwei Nachkommastellen anzeigen
                else:
                    increment = -0.1  # Erste Nachkommastelle
                    format_string = "{:.1f}"  # Eine Nachkommastelle anzeigen
            elif event.keysym == "Right":
                # Nachkommastelle erhöhen (Pfeil nach rechts)
                if shift_pressed:
                    increment = 0.01  # Zweite Nachkommastelle
                    format_string = "{:.2f}"  # Zwei Nachkommastellen anzeigen
                else:
                    increment = 0.1  # Erste Nachkommastelle
                    format_string = "{:.1f}"  # Eine Nachkommastelle anzeigen
            else:
                # Ganzzahlige Änderung (Pfeile nach oben/unten)
                increment = int(increment)  # Keine Nachkommastellen
                if shift_pressed:
                    increment *= 10  # Mit Shift um 10 erhöhen/verringern
                format_string = "{:.0f}"  # Keine Nachkommastellen anzeigen

            new_value = current_value + increment

            # Sicherstellen, dass die Nachkommastelle nicht unter 0 geht
            if event.keysym == "Left" and increment < 0:
                if shift_pressed and round(new_value, 2) < 0:
                    new_value = round(current_value, 1)  # Auf die erste Nachkommastelle zurücksetzen
                elif round(new_value, 1) < 0:
                    new_value = round(current_value, 0)  # Auf die Ganzzahl zurücksetzen

            if new_value >= 0:  # Negative Werte verhindern
                entry.delete(0, tk.END)
                entry.insert(0, format_string.format(new_value))
        except ValueError:
            pass

    def check_values(self, event=None):
        """
        Überprüft die Eingabewerte in den elektrischen Prüfungsfeldern und aktualisiert die Checkbuttons entsprechend.
        """
        schutzklasse = self.schutzklasse_var.get()

        try:
            rpe = float(self.rpe_entry.get()) if self.rpe_entry.get() not in ["-", ""] else None
            riso = float(self.riso_entry.get()) if self.riso_entry.get() not in ["-", ""] else None
            ipe = float(self.ipe_entry.get()) if self.ipe_entry.get() not in ["-", ""] else None
            ib = float(self.ib_entry.get()) if self.ib_entry.get() not in ["-", ""] else None

            # Grenzwerte nach Schutzklasse festlegen
            grenzwerte = {
                "1": {"rpe": 0.3, "riso": 1.0, "ipe": 3.5},
                "2": {"riso": 2.0, "ib": 0.5},
                "3": {"riso": 0.25},
            }

            # Checkbuttons basierend auf Grenzwerten setzen
            self.rpe_check_var.set(
                1 if rpe is not None and rpe <= grenzwerte[schutzklasse].get("rpe", float('inf')) else 0)
            self.riso_check_var.set(1 if riso is not None and riso >= grenzwerte[schutzklasse].get("riso", 0) else 0)
            self.ipe_check_var.set(
                1 if ipe is not None and ipe <= grenzwerte[schutzklasse].get("ipe", float('inf')) else 0)
            self.ib_check_var.set(1 if ib is not None and ib <= grenzwerte[schutzklasse].get("ib", float('inf')) else 0)

        except ValueError:
            pass  # Bei ungültigen Eingaben (z. B. nicht-numerische Werte) nichts tun

    def extract_kundennummer(self, waage_id):
        return waage_id.rsplit('.', 1)[0] if waage_id else ''

    def update_pruefungsart(self):
        vde_selection = self.vde_var.get()

        if vde_selection == 1:  # VDE 701
            self.neugeraet_rb.config(state="normal")
            self.erweiterung_rb.config(state="normal")
            self.instandsetzung_rb.config(state="normal")
            self.wiederholungspruefung_rb.config(state="disabled")
            if self.pruefungsart_var.get() == 3:  # Wenn Wiederholungsprüfung ausgewählt war
                self.pruefungsart_var.set(0)  # Setze auf Neugerät
        elif vde_selection == 2:  # VDE 702
            self.neugeraet_rb.config(state="disabled")
            self.erweiterung_rb.config(state="disabled")
            self.instandsetzung_rb.config(state="disabled")
            self.wiederholungspruefung_rb.config(state="normal")
            self.pruefungsart_var.set(3)  # Setze auf Wiederholungsprüfung

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

    def print_vde_protocol(self):
        """Generiert das VDE-Prüfprotokoll."""
        pdf_generator = PDFGeneratorVDE()
        pdf_generator.add_title("VDE-Prüfprotokoll")
        pdf_generator.add_company_and_inspector_data()
        pdf_generator.add_waagen_data(self.waage_data)

        pdf_generator.add_kundennummer(self.kundennummer)

        # Prüfdatum und Bemerkungen hinzufügen
        pruefdatum = self.pruefdatum_entry.get()
        bemerkungen = self.bemerkungen_text.get("1.0", tk.END).strip()

        # VDE-Prüfdaten sammeln
        schutzklasse = self.schutzklasse_var.get()
        rpe = self.rpe_entry.get()
        riso = self.riso_entry.get()
        ipe = self.ipe_entry.get()
        ib = self.ib_entry.get()
        vde_messgeraet = self.vde_messgeraet_var.get()

        # Elektrische Prüfdaten sammeln (inklusive Checkbox-Werte)
        rpe_bemerkungen = self.rpe_bemerkungen_entry.get()
        riso_bemerkungen = self.riso_bemerkungen_entry.get()
        ipe_bemerkungen = self.ipe_bemerkungen_entry.get()
        ib_bemerkungen = self.ib_bemerkungen_entry.get()

        # Elektrische Daten sammeln
        nennspannung = self.nennspannung_entry.get()
        nennstrom = self.nennstrom_entry.get()
        nennleistung = self.nennleistung_entry.get()
        frequenz = self.frequenz_entry.get()
        cosphi = self.cosphi_entry.get()

        # Visuelle Prüfdaten sammeln
        visuelle_pruefung_daten = {option: var.get() for option, var in self.visuelle_pruefung_vars.items()}

        # Checkbox-Werte für elektrische Prüfung sammeln
        elektrische_pruefung_daten = {
            "rpe_check_var": self.rpe_check_var.get(),
            "riso_check_var": self.riso_check_var.get(),
            "ipe_check_var": self.ipe_check_var.get(),
            "ib_check_var": self.ib_check_var.get(),
            "funktion_check_var": self.funktion_check_var.get()
        }

        vde_pruefung = {
            'vde_701': self.vde_var.get() == 1,
            'vde_702': self.vde_var.get() == 2,
            'pruefungsart': self.pruefungsart_var.get()
        }

        pdf_generator.add_vde_pruefung(schutzklasse, rpe, riso, ipe, ib, vde_messgeraet,
                                       nennspannung, nennstrom, nennleistung, frequenz, cosphi, visuelle_pruefung_daten,
                                       rpe_bemerkungen, riso_bemerkungen, ipe_bemerkungen, ib_bemerkungen,
                                       elektrische_pruefung_daten, vde_pruefung)

        pdf_generator.add_pruefdatum_bemerkungen(pruefdatum, bemerkungen)

        # Kalibrierscheinnummer generieren
        calibration_number = pdf_generator.get_calibration_number()

        # Protokoll-Speicherpfad aus den Einstellungen holen
        settings = Settings()
        protokoll_path = settings.get_protokoll_path()

        # PDF-Dateiname mit Kalibrierscheinnummer erstellen
        pdf_filename = f"{calibration_number}.pdf"
        pdf_path = os.path.join(protokoll_path, pdf_filename)

        # PDF generieren und speichern
        pdf_generator.generate_pdf(pdf_path)

        # PDF öffnen (Plattform-spezifisch)
        try:
            if os.name == 'nt':
                os.startfile(pdf_path)
            elif os.name == 'posix':
                subprocess.call(('open', pdf_path))
        except Exception as e:
            messagebox.showerror("Fehler", f"Konnte PDF nicht öffnen: {str(e)}")