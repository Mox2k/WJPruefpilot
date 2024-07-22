import tkinter as tk

from tkinter import ttk
from detail_temp_window import DetailTempWindow
from detail_vde_window import DetailVDEWindow


class DetailWindow(tk.Toplevel):
    """Klasse für das Detailfenster einer Waage."""

    def __init__(self, master=None, waage_id=None, waage_data=None):
        super().__init__(master)
        self.waage_id = waage_id
        self.waage_data = waage_data
        self.title(f"Details für Waage {waage_id}")
        self.create_widgets()
        self.resizable(False, False)

        # Zentrierung innerhalb des Elternfensters (master)
        self.update_idletasks()
        self.geometry("+%d+%d" % (
            master.winfo_x() + (master.winfo_width() - self.winfo_width()) // 2,
            master.winfo_y() + (master.winfo_height() - self.winfo_height()) // 2
        ))

    def create_widgets(self):
        """Erstellt die Widgets des Detailfensters."""

        self.columnconfigure(0, weight=1)  # Spalte 0 dehnbar machen
        self.rowconfigure(1, weight=1)  # Zeile 1 dehnbar machen (für Buttons)
        self.rowconfigure(2, weight=1)  # Zeile 2 dehnbar machen (für Buttons)

        # --- Waagendetails ---
        details_frame = ttk.LabelFrame(self, text="Waagendetails")
        details_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 0))

        # Labels für Hersteller, Modell und Seriennummer
        ttk.Label(details_frame, text=f"Hersteller: {self.waage_data[3]}").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Label(details_frame, text=f"Modell: {self.waage_data[4]}").grid(row=0, column=1, sticky="w", padx=5, pady=5)
        ttk.Label(details_frame, text=f"Seriennummer: {self.waage_data[1]}").grid(row=0, column=2, sticky="w", padx=5, pady=5)

        # Buttons für neue Fenster
        button_frame = ttk.Frame(self)  # Neuer Frame für die Buttons
        button_frame.grid(row=1, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)

        ttk.Button(button_frame, text="Temperaturjustage", command=self.open_temp_window).pack(fill="both", expand=True)  # Button im Frame, füllt ihn aus
        ttk.Button(button_frame, text="VDE-Prüfung", command=self.open_vde_window).pack(fill="both", expand=True)  # Button im Frame, füllt ihn aus

    def open_temp_window(self):
        DetailTempWindow(self, self.waage_id, self.waage_data)

    def open_vde_window(self):
        DetailVDEWindow(self, self.waage_id, self.waage_data)
