import configparser
import base64
import io

from weasyprint import HTML
from datetime import datetime, timedelta
from PIL import Image


class PDFGeneratorVDE:

    def __init__(self):
        self.html_content = """
        <html>
        <head>
            <style>
                body { font-family: Arial; }
                h1 { font-size: 16pt; font-weight: bold; }
                p { font-size: 14px; }
            </style>
        </head>
        <body>
        """

    def add_title(self, title):
        self.html_content += f"<h1>{title}</h1>"

    def add_company_and_inspector_data(self):
        """Fügt Firmen- und Prüferdaten aus der Konfigurationsdatei hinzu."""
        config = configparser.ConfigParser()
        config.read('settings.ini')

        firma = config['FIRMA']['firma']
        strasse = config['FIRMA']['strasse']
        plz = config['FIRMA']['plz']
        ort = config['FIRMA']['ort']

        # neu hinzugefügt: Logo aus der Konfigurationsdatei lesen
        logo_bild = config['FIRMA']['logo']

        pruefer_name = config['PRUEFER']['name']
        unterschrift_bild = config['PRUEFER']['unterschrift']

        try:
            # Bild öffnen und skalieren (Unterschrift)
            img = Image.open(unterschrift_bild)
            img.thumbnail((150, 150))

            # Bild in RGB konvertieren (neu hinzugefügt)
            img = img.convert("RGB")

            # Bild im Speicher zwischenspeichern (Unterschrift)
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

            # neu hinzugefügt: Bild öffnen und skalieren (Logo)
            logo = Image.open(logo_bild)
            logo.thumbnail((150, 150))  # Oder passe die Größe nach Bedarf an

            # Bild im Speicher zwischenspeichern (Logo)
            logo_buffered = io.BytesIO()
            logo.save(logo_buffered, format="JPEG")
            logo_str = base64.b64encode(logo_buffered.getvalue()).decode('utf-8')

            # geändert
            self.html_content += f"""
            <div style="text-align: center;">
              <h2>{firma}</h2>
              <img src="data:image/jpeg;base64,{logo_str}" alt="Logo" width="150">
              <p>{strasse}<br>{plz} {ort}</p>
            </div>
            <div style="text-align: right;">
              <p><b>Prüfer:</b> {pruefer_name}</p>
              <img src="data:image/jpeg;base64,{img_str}" alt="Unterschrift" width="150">
            </div>
            """

        except (FileNotFoundError, OSError) as e:
            print(f"Error loading or processing image: {e}")

    def add_waagen_data(self, waage_data):
        kdw_bezeichnung, kdw_snr, kdw_ident_nr, adr_name1, kdw_modell, kdw_standort, kdw_raum, kdw_luftbewegung, kdw_unruhe, kdw_verschmutzung, \
            kdw_waegebereich1, kdw_waegebereich2, kdw_waegebereich3, kdw_waegebereich4, kdw_teilungswert1, kdw_teilungswert2, \
            kdw_teilungswert3, kdw_teilungswert4, kdw_feuchte_min, kdw_feuchte_max, kdw_dakks_intervall, auf_nummer_bez, adr_name2, \
            adr_name3, adr_strasse, adr_plz, adr_ort = waage_data

        self.html_content += f"""
        <table>
            <tr><th>WJ-Nummer:</th><td>{kdw_bezeichnung}</td></tr>
            <tr><th>S/N:</th><td>{kdw_snr}</td></tr>
            <tr><th>Inventarnummer:</th><td>{kdw_ident_nr}</td></tr>
            <tr><th>Hersteller:</th><td>{adr_name1}</td></tr>
            <tr><th>Modell:</th><td>{kdw_modell}</td></tr>
            <tr><th>Standort:</th><td>{kdw_standort}</td></tr>
            <tr><th>Raum:</th><td>{kdw_raum}</td></tr>
            <tr><th>Luftbewegung:</th><td>{kdw_luftbewegung}</td></tr>
            <tr><th>Unruhe:</th><td>{kdw_unruhe}</td></tr>
            <tr><th>Verschmutzung:</th><td>{kdw_verschmutzung}</td></tr>
            <tr><th>Bereich1:</th><td>{kdw_waegebereich1}</td></tr>
            <tr><th>Bereich2:</th><td>{kdw_waegebereich2}</td></tr>
            <tr><th>Bereich3:</th><td>{kdw_waegebereich3}</td></tr>
            <tr><th>Bereich4:</th><td>{kdw_waegebereich4}</td></tr>
            <tr><th>Teilung1:</th><td>{kdw_teilungswert1}</td></tr>
            <tr><th>Teilung2:</th><td>{kdw_teilungswert2}</td></tr>
            <tr><th>Teilung3:</th><td>{kdw_teilungswert3}</td></tr>
            <tr><th>Teilung4:</th><td>{kdw_teilungswert4}</td></tr>
            <tr><th>Feuchte Min:</th><td>{kdw_feuchte_min} rel.%</td></tr>
            <tr><th>Feuchte Max:</th><td>{kdw_feuchte_max} rel.%</td></tr>
            <tr><th>DAkkS-Intervall:</th><td>{kdw_dakks_intervall} Monate</td></tr>
            <tr><th>Auftragsnummer:</th><td>{auf_nummer_bez}</td></tr>
            <tr><th>Adresse:</th><td>{adr_name1} {adr_name2} {adr_name3} {adr_strasse} {adr_plz} {adr_ort}</td></tr>
        </table>
        """

    def add_vde_pruefung(self, schutzklasse, rpe, riso, ipe, ib, vde_messgeraet,
                         nennspannung, nennstrom, nennleistung, frequenz, cosphi, visuelle_pruefung_daten=None,
                         rpe_bemerkungen=None, riso_bemerkungen=None, ipe_bemerkungen=None, ib_bemerkungen=None,
                         elektrische_pruefung_daten=None):
        """Fügt die VDE-Prüfdaten, elektrischen Daten und visuellen Prüfdaten (falls vorhanden) als Tabelle hinzu."""

        self.html_content += f"""
        <h2>VDE-Prüfung</h2>
        <table>
            <tr><th>Schutzklasse:</th><td>{schutzklasse}</td></tr>
            <tr><th>Schutzleiterwiderstand (RPE):</th><td>{rpe}</td></tr>
            <tr><th>Bemerkungen RPE:</th><td>{rpe_bemerkungen if rpe_bemerkungen else "-"}</td></tr>
            <tr><th>Isolationswiderstand (RISO):</th><td>{riso}</td></tr>
            <tr><th>Bemerkungen RISO:</th><td>{riso_bemerkungen if riso_bemerkungen else "-"}</td></tr>
            <tr><th>Schutzleiterstrom (IPE):</th><td>{ipe}</td></tr>
            <tr><th>Bemerkungen IPE:</th><td>{ipe_bemerkungen if ipe_bemerkungen else "-"}</td></tr>
            <tr><th>Berührungsstrom (IB):</th><td>{ib}</td></tr>
            <tr><th>Bemerkungen IB:</th><td>{ib_bemerkungen if ib_bemerkungen else "-"}</td></tr>
            <tr><th>VDE-Messgerät:</th><td>{vde_messgeraet}</td></tr>
            <tr><th>Nennspannung (V):</th><td>{nennspannung}</td></tr>
            <tr><th>Nennstrom (A):</th><td>{nennstrom}</td></tr>
            <tr><th>Nennleistung (W):</th><td>{nennleistung}</td></tr>
            <tr><th>Frequenz (Hz):</th><td>{frequenz}</td></tr>
            <tr><th>cosPhi:</th><td>{cosphi}</td></tr>
        </table>
        """

        if visuelle_pruefung_daten:
            self.html_content += "<h2>Visuelle Prüfung</h2><table>"

            for option, ergebnis in visuelle_pruefung_daten.items():
                self.html_content += f"""
                    <tr>
                        <th>{option}:</th>
                        <td><input type="checkbox" {"checked" if ergebnis == 1 else ""}> i.O.</td> 
                        <td><input type="checkbox" {"checked" if ergebnis == 0 else ""}> n.i.O.</td> 
                    </tr>
                    """

            self.html_content += "</table>"

            # Mapping von Variablennamen zu Anzeigenamen
            option_mapping = {
                "rpe_check_var": "Schutzleiterwiderstand (RPE)",
                "riso_check_var": "Isolationswiderstand (RISO)",
                "ipe_check_var": "Schutzleiterstrom (IPE)",
                "ib_check_var": "Berührungsstrom (IB)",
                "funktion_check_var": "Funktion des Gerätes"
            }

            # Elektrische Prüfung (Checkboxen)
            self.html_content += """
                <h2>Elektrische Prüfung</h2>
                <table>
                """

            if elektrische_pruefung_daten:
                for option, ergebnis in elektrische_pruefung_daten.items():
                    # Anzeigenamen aus dem Mapping verwenden
                    option_name = option_mapping.get(option, option)
                    check_value = ergebnis

                    self.html_content += f"""
                            <tr>
                                <th>{option_name}:</th>
                                <td><input type="checkbox" {"checked" if check_value == 1 else ""}> i.O.</td> 
                                <td><input type="checkbox" {"checked" if check_value == 0 else ""}> n.i.O.</td> 
                            </tr>
                            """
            self.html_content += "</table>"

    def add_pruefdatum_bemerkungen(self, pruefdatum, bemerkungen):
        """Fügt Prüfdatum, Bemerkungen und das Datum ein Jahr später hinzu."""

        # Formatiere das Prüfdatum
        pruefdatum_obj = datetime.strptime(pruefdatum, "%d.%m.%Y")
        pruefdatum_str = pruefdatum_obj.strftime("%d.%m.%Y")

        # Berechne das Datum in einem Jahr
        datum_in_einem_jahr = pruefdatum_obj + timedelta(days=365)
        datum_in_einem_jahr_str = datum_in_einem_jahr.strftime("%m.%Y")

        # Füge die Informationen zum HTML-Inhalt hinzu
        self.html_content += f"<p><b>Datum der Prüfung:</b> {pruefdatum_str}</p>"
        if bemerkungen:
            self.html_content += f"<p><b>Bemerkungen:</b> {bemerkungen}</p>"
        self.html_content += f"<p><b>Datum in einem Jahr:</b> {datum_in_einem_jahr_str}</p>"

    def generate_pdf(self, filename="report.pdf"):
        self.add_company_and_inspector_data()
        self.html_content += "</body></html>"
        HTML(string=self.html_content).write_pdf(filename)
