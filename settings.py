import configparser
import os


class Settings:
    """Klasse zum Lesen und Schreiben von Einstellungen aus einer INI-Datei."""

    def __init__(self, config_file='settings.ini'):  # Standardname für die INI-Datei
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.data = {}
        self.load_settings()
        # Versuchen, die INI-Datei zu laden, falls sie existiert
        try:
            self.config.read(self.config_file)
        except configparser.Error:
            pass  # Wenn die Datei nicht vorhanden ist oder fehlerhaft ist, weitermachen

    def get_setting(self, section, option, default=None):
        """Liest eine Einstellung oder gibt den Standardwert zurück."""
        if not self.config.has_section(section):
            return default
        return self.config.get(section, option, fallback=default)

    def set_setting(self, section, option, value):
        """Schreibt eine Einstellung in die INI-Datei."""
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, value)
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def get_sqlite_databases(self, directory):
        """Gibt eine Liste aller sqlite-Dateien im angegebenen Verzeichnis zurück."""
        databases = []
        for file in os.listdir(directory):
            if file.endswith(".sqlite"):
                databases.append(file)
        return databases

    def set_selected_database(self, database_name):
        """Speichert den Namen der ausgewählten Datenbank in der INI-Datei."""
        self.set_setting('DATABASE', 'name', database_name)

    def get_selected_database(self):
        """Liest den Namen der ausgewählten Datenbank aus der INI-Datei."""
        return self.get_setting('DATABASE', 'name', None)

    def set_company_data(self, firma, strasse, plz, ort):
        """Speichert die Firmendaten in der INI-Datei."""
        self.set_setting('FIRMA', 'firma', firma)
        self.set_setting('FIRMA', 'strasse', strasse)
        self.set_setting('FIRMA', 'plz', plz)
        self.set_setting('FIRMA', 'ort', ort)

    #wird später auf dem PDF ausgegeben
    def get_company_data(self):
        """Liest die Firmendaten aus der INI-Datei."""
        return {
            'firma': self.get_setting('FIRMA', 'firma', ''),
            'strasse': self.get_setting('FIRMA', 'strasse', ''),
            'plz': self.get_setting('FIRMA', 'plz', ''),
            'ort': self.get_setting('FIRMA', 'ort', ''),
        }

    def get_pruefer_name(self):
        """Liest den Namen des Prüfers aus der INI-Datei."""
        return self.get_setting('PRUEFER', 'name', '')

    def set_pruefer_name(self, name):
        """Speichert den Namen des Prüfers in der INI-Datei."""
        self.set_setting('PRUEFER', 'name', name)

    def get_messgeraete(self):
        """Liest die Messgeräte-Daten aus der INI-Datei."""
        messgeraete = {}
        for i in range(1, 11):
            messgeraete[f'Temperaturmessgeraet_{i}'] = self.get_setting('MESSGERAETE', f'Temperaturmessgeraet_{i}', '')
            messgeraete[f'VDE-Messgeraet_{i}'] = self.get_setting('MESSGERAETE', f'VDE-Messgeraet_{i}', '')
        return messgeraete

    def set_messgeraete(self, messgeraete):
        """Speichert die Messgeräte-Daten in der INI-Datei."""
        for name, wert in messgeraete.items():
            self.set_setting('MESSGERAETE', name, wert)

    def get_logo_path(self):
        """Liest den Pfad zum Firmenlogo aus der INI-Datei."""
        filename = self.get_setting('FIRMA', 'logo', '')
        if filename:
            return os.path.join(os.getcwd(), filename)  # Pfad im Programmverzeichnis
        else:
            return None

    def get_signature_path(self):
        """Liest den Pfad zur Unterschrift aus der INI-Datei."""
        filename = self.get_setting('PRUEFER', 'unterschrift', '')
        if filename:
            return os.path.join(os.getcwd(), filename)  # Pfad im Programmverzeichnis
        else:
            return None

    def set_protokoll_path(self, path):
        """Speichert den Pfad für die Protokolle in der INI-Datei."""
        self.set_setting('PATH', 'protokolle', path)

    # #neu hinzugefügt
    def get_protokoll_path(self):
        """Liest den Pfad für die Protokolle aus der INI-Datei."""
        return self.get_setting('PATH', 'protokolle', os.path.join(os.getcwd(), 'Protokolle'))

    def load_settings(self):
        """Liest die Einstellungen aus der settings.ini Datei."""
        config = configparser.ConfigParser()
        config.read('settings.ini')  # Use the correct path to your settings.ini file
        for section in config.sections():
            for key, value in config.items(section):
                self.data[key] = value
