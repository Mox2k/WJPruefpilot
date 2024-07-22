import os
import configparser
import base64
import io

from weasyprint import HTML
from datetime import datetime, timedelta
from PIL import Image


class PDFGeneratorVDE:

    def __init__(self):
        self.stored_data = {}
        self.data_to_append = {}

    def add_title(self, title):
        self.stored_data['title_data'] = title

    def add_company_and_inspector_data(self):
        """Fügt Firmen- und Prüferdaten aus der Konfigurationsdatei hinzu."""
        config = configparser.ConfigParser()
        config.read('settings.ini')

        firma = config['FIRMA']['firma']
        strasse = config['FIRMA']['strasse']
        plz = config['FIRMA']['plz']
        ort = config['FIRMA']['ort']

        logo_bild = config['FIRMA']['logo']
        pruefer_name = config['PRUEFER']['name']
        unterschrift_bild = config['PRUEFER']['unterschrift']
        stempel_bild = config['FIRMA']['stempel']

        logo_str = ""
        img_str = ""
        stempel_str = ""

        try:
            if not os.path.exists(logo_bild):
                raise FileNotFoundError(f"Logobild nicht gefunden: {logo_bild}")
            if not os.path.exists(unterschrift_bild):
                raise FileNotFoundError(f"Unterschriftsbild nicht gefunden: {unterschrift_bild}")
            if not os.path.exists(stempel_bild):
                raise FileNotFoundError(f"Stempelbild nicht gefunden: {stempel_bild}")

            with Image.open(logo_bild) as logo:
                base_width = 1600
                w_percent = (base_width / float(logo.size[0]))
                h_size = int((float(logo.size[1]) * float(w_percent)))
                logo = logo.resize((base_width, h_size), Image.LANCZOS)

                logo_buffered = io.BytesIO()
                logo.save(logo_buffered, format="PNG", optimize=True, quality=95)
                logo_str = base64.b64encode(logo_buffered.getvalue()).decode('utf-8')

            with Image.open(unterschrift_bild) as img:
                base_height = 600
                h_percent = (base_height / float(img.size[1]))
                w_size = int((float(img.size[0]) * float(h_percent)))
                img = img.resize((w_size, base_height), Image.LANCZOS)

                buffered = io.BytesIO()
                img.save(buffered, format="PNG", optimize=True, quality=95)
                img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

            with Image.open(stempel_bild) as stempel:
                base_width = 800
                w_percent = (base_width / float(stempel.size[0]))
                h_size = int((float(stempel.size[1]) * float(w_percent)))
                stempel = stempel.resize((base_width, h_size), Image.LANCZOS)

                stempel_buffered = io.BytesIO()
                stempel.save(stempel_buffered, format="PNG", optimize=True, quality=95)
                stempel_str = base64.b64encode(stempel_buffered.getvalue()).decode('utf-8')

        except (FileNotFoundError, OSError) as e:
            print(f"Error loading or processing image: {e}")

        self.data_to_append['company_and_inspector_data'] = {
            'firma': firma,
            'strasse': strasse,
            'plz': plz,
            'ort': ort,
            'logo_str': logo_str,
            'pruefer_name': pruefer_name,
            'unterschrift_str': img_str,
            'stempel_str': stempel_str
        }

    def add_waagen_data(self, waage_data):
        kdw_bezeichnung, kdw_snr, kdw_ident_nr, hersteller_name, kdw_modell, kdw_standort, kdw_raum, kdw_luftbewegung, kdw_unruhe, kdw_verschmutzung, \
            kdw_waegebereich1, kdw_waegebereich2, kdw_waegebereich3, kdw_waegebereich4, kdw_teilungswert1, kdw_teilungswert2, \
            kdw_teilungswert3, kdw_teilungswert4, kdw_feuchte_min, kdw_feuchte_max, kdw_dakks_intervall, auf_nummer_bez, \
            kunde_name1, kunde_name2, kunde_name3, kunde_strasse, kunde_plz, kunde_ort, aufheizzyklus, temp_herstellertoleranz = waage_data

        # Erstelle ein Dictionary mit allen Daten
        waage_data_dict = {
            'WJ-Nummer': kdw_bezeichnung,
            'S/N': kdw_snr,
            'Inventarnummer': kdw_ident_nr,
            'Hersteller': hersteller_name,
            'Modell': kdw_modell,
            'Standort': kdw_standort,
            'Raum': kdw_raum,
            'Luftbewegung': kdw_luftbewegung,
            'Unruhe': kdw_unruhe,
            'Verschmutzung': kdw_verschmutzung,
            'Bereich1': kdw_waegebereich1,
            'Bereich2': kdw_waegebereich2,
            'Bereich3': kdw_waegebereich3,
            'Bereich4': kdw_waegebereich4,
            'Teilung1': kdw_teilungswert1,
            'Teilung2': kdw_teilungswert2,
            'Teilung3': kdw_teilungswert3,
            'Teilung4': kdw_teilungswert4,
            'Feuchte Min': kdw_feuchte_min,
            'Feuchte Max': kdw_feuchte_max,
            'DAkkS-Intervall': kdw_dakks_intervall,
            'Auftragsnummer': auf_nummer_bez,
            'Kunde_name1': kunde_name1,
            'Kunde_name2': kunde_name2,
            'Kunde_name3': kunde_name3,
            'Kunde_Strasse': kunde_strasse,
            'Kunde_plz': kunde_plz,
            'Kunde_ort': kunde_ort,
            'Aufheizzyklus': aufheizzyklus,
            'TempHerstellertoleranz': temp_herstellertoleranz
        }

        # Filtere die Daten
        filtered_waage_data = {}
        for key, value in waage_data_dict.items():
            if key.startswith(('Bereich', 'Teilung')):
                if value != '0' and value != 0:
                    filtered_waage_data[key] = value
            else:
                filtered_waage_data[key] = value

        # Speichere die gefilterten Daten
        self.data_to_append['waage_data'] = filtered_waage_data

    def add_vde_pruefung(self, schutzklasse, rpe, riso, ipe, ib, vde_messgeraet,
                         nennspannung, nennstrom, nennleistung, frequenz, cosphi, visuelle_pruefung_daten=None,
                         rpe_bemerkungen=None, riso_bemerkungen=None, ipe_bemerkungen=None, ib_bemerkungen=None,
                         elektrische_pruefung_daten=None):
        """Fügt die VDE-Prüfdaten, elektrischen Daten und visuellen Prüfdaten als Tabelle hinzu."""
        self.data_to_append['vde_data'] = {
            'schutzklasse': schutzklasse,
            'rpe': rpe,
            'riso': riso,
            'ipe': ipe,
            'ib': ib,
            'vde_messgeraet': vde_messgeraet,
            'nennspannung': nennspannung,
            'nennstrom': nennstrom,
            'nennleistung': nennleistung,
            'frequenz': frequenz,
            'cosphi': cosphi,
            'rpe_bemerkungen': rpe_bemerkungen,
            'riso_bemerkungen': riso_bemerkungen,
            'ipe_bemerkungen': ipe_bemerkungen,
            'ib_bemerkungen': ib_bemerkungen,
            'visuelle_pruefung_daten': visuelle_pruefung_daten,
            'elektrische_pruefung_daten': elektrische_pruefung_daten
        }

    def add_pruefdatum_bemerkungen(self, pruefdatum, bemerkungen):
        """Fügt Prüfdatum, Bemerkungen und das Datum ein Jahr später hinzu."""
        pruefdatum_obj = datetime.strptime(pruefdatum, "%d.%m.%Y")
        pruefdatum_str = pruefdatum_obj.strftime("%d.%m.%Y")

        datum_in_einem_jahr = pruefdatum_obj + timedelta(days=365)
        datum_in_einem_jahr_str = datum_in_einem_jahr.strftime("%m.%Y")

        self.data_to_append['pruefdatum'] = pruefdatum_str
        self.data_to_append['datum_in_einem_jahr'] = datum_in_einem_jahr_str
        self.data_to_append['bemerkungen'] = bemerkungen

    def generate_calibration_number(self):
        pruefer_name = self.data_to_append.get('company_and_inspector_data', {}).get('pruefer_name', '')
        initials = ''.join([name[0].upper() for name in pruefer_name.split() if name])
        current_date = datetime.now().strftime("%m%y")
        waage_id = self.data_to_append.get('waage_data', {}).get('WJ-Nummer', '')
        return f"VDE_{initials}_{current_date}_{waage_id}"

    def get_calibration_number(self):
        return self.generate_calibration_number()

    def generate_pdf(self, filename="vde_report.pdf"):
        calibration_number = self.generate_calibration_number()

        Kunde = self.data_to_append.get('waage_data', {}).get('Kunde_name1', '')
        if self.data_to_append.get('waage_data', {}).get('Kunde_name2', '') != "":
            Kunde = self.data_to_append.get('waage_data', {}).get('Kunde_name1', '') + "<br>" + self.data_to_append.get('waage_data', {}).get('Kunde_name2', '')
        elif self.data_to_append.get('waage_data', {}).get('Kunde_name3', '') != "":
            Kunde = self.data_to_append.get('waage_data', {}).get('Kunde_name1', '') + "<br>" + self.data_to_append.get('waage_data', {}).get('Kunde_name2', '') + "<br>" + self.data_to_append.get('waage_data', {}).get('Kunde_name3', '')

        html_template = f"""
        <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: Calibri, sans-serif; font-size: 12px; margin: 0px; }}
                    h1 {{ font-size: 24px; font-weight: bold; margin-top: 0px; margin-bottom: 0px; }}
                    h2 {{ font-size: 22px; margin-top: 0px; margin-bottom: 0px; }}
                    h4 {{ margin-top: 0px; margin-bottom: 0px; }}
                    p {{ font-size: 14px; }}
                    .header {{ display: flex; justify-content: space-between; margin: 5px; margin-bottom: 40px }}
                    .logo {{ width: 200px; }}
                    .details {{ text-align: left; }}
                    table {{ border-collapse: collapse; width: 100%; margin-bottom: 10px; font-size: 14px; }}
                    th, td {{ border: 0px solid #222; padding: 5px; text-align: left; vertical-align: top; }}
                    .border, .border {{ border: 1px solid #222; }}
                    th {{ background-color: #f0f0f5; font-weight: bold; }}
                    .footer {{ display: flex; justify-content: space-between; font-size: 12px; padding: 0 42px 0 42px; }}
                    .check-mark {{ color: green; font-weight: bold; }}
                    .cross-mark {{ color: red; font-weight: bold; }}
                    @media print {{ .pagebreak {{ clear: both; page-break-after: always; }} }}
                    #footer {{ position: fixed; width: 100%; bottom: 0; left: 0; right: 0; }}
                    .page-start {{ page-break-after: always; height: 100%; }}
                    .logo {{ max-width: 100%; width: 150px; height: auto; }}
                    .signature {{ max-height: 150px; width: 220px; height: auto; }}
                </style>
            </head>
            <body>
                <!-- Custom HTML footer -->
                <div id="footer">
                  <div class="footer">
                    <div class="logo" style="width:120px;">
                      <img src="data:image/png;base64,{self.data_to_append.get('company_and_inspector_data', {}).get('logo_str', '')}"
                           alt="Logo" class="logo">
                    </div>
                    <div>
                      <h4>{self.data_to_append.get('company_and_inspector_data', {}).get('firma', '')},
                        {self.data_to_append.get('company_and_inspector_data', {}).get('strasse', '')},
                        {self.data_to_append.get('company_and_inspector_data', {}).get('plz', '')}
                        {self.data_to_append.get('company_and_inspector_data', {}).get('ort', '')}, Germany</h4>
                      +49 4329 911 94 14, waagen-kalibrieren.de
                    </div>
                  </div>
                </div>
{calibration_number}                                                         
            </body>
        </html>
        """

        # Konvertiere das HTML-Template in ein Unicode-Objekt
        html_unicode = html_template.encode('utf-8').decode('utf-8')

        # Generiere das PDF mit der UTF-8 kodierten HTML
        HTML(string=html_unicode).write_pdf(filename)