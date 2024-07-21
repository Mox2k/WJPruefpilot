import tkinter as tk
from main_window import MainWindow


def main():
    """Hauptfunktion zum Starten der Anwendung."""
    root = tk.Tk()
    root.title("Prüfpilot")
    root.iconphoto(True, tk.PhotoImage(file="WJ-Icon.png"))
    app = MainWindow(root)
    app.pack(fill=tk.BOTH, expand=True)
    root.geometry("1000x450")
    root.mainloop()


if __name__ == "__main__":
    main()
