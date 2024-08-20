import os
import configparser
import base64
import io

from xhtml2pdf import pisa
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

        logo_bild = config['FIRMA']['logo']  # Dies sollte 'logo.png' sein
        pruefer_name = config['PRUEFER']['name']
        unterschrift_bild = config['PRUEFER']['unterschrift']
        stempel_bild = config['FIRMA']['stempel']

        # Initialisiere logo_str, img_str und stempel_str mit leeren Strings
        logo_str = ""
        img_str = ""
        stempel_str = ""

        try:
            # Funktion zum Konvertieren von Palettenbildern mit Transparenz in RGBA
            def convert_to_rgba(img):
                if img.mode == 'P':
                    return img.convert('RGBA')
                return img

            # Überprüfen Sie, ob die Dateien existieren
            if not os.path.exists(logo_bild):
                raise FileNotFoundError(f"Logobild nicht gefunden: {logo_bild}")
            if not os.path.exists(unterschrift_bild):
                raise FileNotFoundError(f"Unterschriftsbild nicht gefunden: {unterschrift_bild}")
            if not os.path.exists(stempel_bild):
                raise FileNotFoundError(f"Stempelbild nicht gefunden: {stempel_bild}")

            # Bild öffnen und Größe anpassen (Logo)
            with Image.open(logo_bild) as logo:
                logo = convert_to_rgba(logo)
                # Berechne neue Größe unter Beibehaltung des Seitenverhältnisses
                base_width = 1600
                w_percent = (base_width / float(logo.size[0]))
                h_size = int((float(logo.size[1]) * float(w_percent)))
                logo = logo.resize((base_width, h_size), Image.LANCZOS)

                # Bild im Speicher zwischenspeichern (Logo)
                logo_buffered = io.BytesIO()
                logo.save(logo_buffered, format="PNG", optimize=True, quality=95)
                logo_str = base64.b64encode(logo_buffered.getvalue()).decode('utf-8')

            # Bild öffnen und Größe anpassen (Unterschrift)
            with Image.open(unterschrift_bild) as img:
                img = convert_to_rgba(img)
                # Berechne neue Größe unter Beibehaltung des Seitenverhältnisses
                base_height = 600
                h_percent = (base_height / float(img.size[1]))
                w_size = int((float(img.size[0]) * float(h_percent)))
                img = img.resize((w_size, base_height), Image.LANCZOS)

                # Bild im Speicher zwischenspeichern (Unterschrift)
                buffered = io.BytesIO()
                img.save(buffered, format="PNG", optimize=True, quality=95)
                img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

            # Bild öffnen und Größe anpassen (Stempel)
            with Image.open(stempel_bild) as stempel:
                stempel = convert_to_rgba(stempel)
                # Berechne neue Größe unter Beibehaltung des Seitenverhältnisses
                base_width = 800
                w_percent = (base_width / float(stempel.size[0]))
                h_size = int((float(stempel.size[1]) * float(w_percent)))
                stempel = stempel.resize((base_width, h_size), Image.LANCZOS)

                # Bild im Speicher zwischenspeichern (Stempel)
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
                         elektrische_pruefung_daten=None, vde_pruefung=None):
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
            'elektrische_pruefung_daten': elektrische_pruefung_daten,
            'vde_pruefung': vde_pruefung
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

        vde_pruefung = self.data_to_append['vde_data']['vde_pruefung']

        # #geändert: VDE-Prüfung und Prüfungsart als Text
        vde_text = ""
        if vde_pruefung['vde_701']:
            vde_text = "DIN VDE 701 "
            if vde_pruefung['pruefungsart']['Neugerät']:
                vde_text += " - Neugerät"
            elif vde_pruefung['pruefungsart']['Erweiterung']:
                vde_text += " - Erweiterung"
            elif vde_pruefung['pruefungsart']['Instandsetzung']:
                vde_text += " - Instandsetzung"
        elif vde_pruefung['vde_702']:
            vde_text = "DIN VDE 702 - Wiederholungsprüfung"
        else:
            vde_text = "Keine VDE-Prüfung ausgewählt"

        #Funktion zur Umwandlung in römische Zahlen
        def to_roman(num):
            roman_numerals = {1: 'I', 2: 'II', 3: 'III'}
            return roman_numerals.get(num, str(num))

        #Schutzklasse in römische Zahlen umwandeln
        schutzklasse = self.data_to_append['vde_data']['schutzklasse']
        schutzklasse_roman = to_roman(int(schutzklasse))


        #Symbole für Häkchen und Kreuz
        haken = "&#x2714;"  # Unicode für ein dickeres Häkchen
        kreuz = "&#x2718;"  # Unicode für ein dickeres Kreuz

        #Visuelle Prüfungsdaten in Variablen packen
        visuelle_pruefung_daten = self.data_to_append['vde_data']['visuelle_pruefung_daten']

        typenschild = haken if visuelle_pruefung_daten.get("Typenschild/Warnhinweis/Kennzeichnungen",
                                                           0) == 1 else kreuz
        gehaeuse = haken if visuelle_pruefung_daten.get("Gehäuse/Schutzabdeckungen", 0) == 1 else kreuz
        anschlussleitung = haken if visuelle_pruefung_daten.get(
            "Anschlussleitung/stecker,Anschlussklemmen und -adern", 0) == 1 else kreuz
        biegeschutz = haken if visuelle_pruefung_daten.get("Biegeschutz/Zugentlastung", 0) == 1 else kreuz
        leitungshalterungen = haken if visuelle_pruefung_daten.get("Leitungshalterungen, Sicherungshalter, usw.",
                                                                   0) == 1 else kreuz
        kuehlluft = haken if visuelle_pruefung_daten.get("Kühlluftöffnungen/Luftfilter", 0) == 1 else kreuz
        schalter = haken if visuelle_pruefung_daten.get("Schalter, Steuer, Einstell- und Sicherheitsvorrichtungen",
                                                        0) == 1 else kreuz
        bemessung = haken if visuelle_pruefung_daten.get("Bemessung der zugänglichen Gerätesicherung",
                                                         0) == 1 else kreuz
        bauteile = haken if visuelle_pruefung_daten.get("Beuteile und Baugruppen", 0) == 1 else kreuz
        ueberlastung = haken if visuelle_pruefung_daten.get("Anzeichen von Überlastung/unsachgemäßem Gebrauch",
                                                            0) == 1 else kreuz
        verschmutzung = haken if visuelle_pruefung_daten.get(
            "Sicherheitsbeeinträchtigende Verschmutzung/Korrission/Alterung", 0) == 1 else kreuz
        mechanische_gefaehrdung = haken if visuelle_pruefung_daten.get("Mechanische Gefährdung", 0) == 1 else kreuz
        unzulaessige_eingriffe = haken if visuelle_pruefung_daten.get("Unzulässige Eingriffe und Änderungen",
                                                                          0) == 1 else kreuz

        html_template = f"""
        <html><!-- DIN A4 21x29,7 cm -->
            <head>
            <style>
                @page {{ size: a4 portrait;
                    @frame header_frame {{
                        -pdf-frame-content: header_content_1;
                        left: 1cm;
                        right: 1cm;
                        top: 1cm;
                    }}
                    @frame content_frame {{
                        left: 1cm;
                        right: 1cm;
                        top: 1cm;
                    }}
                    @frame footer_frame {{
                        -pdf-frame-content: footer_content;
                        left: 2cm;
                        right: 2cm;
                        bottom: 0cm;
                        height: 2cm;
                    }}
                }}

                body {{ font-size: 12px; line-height: 1.2; }}
                h1 {{ font-size: 24px; margin-top: 0px; margin-bottom: 0px; }}
                h2 {{ font-size: 22px; margin-top: 0px; margin-bottom: 0px; }}
                h4 {{ margin-top: 0px; margin-bottom: 0px; }}
                p {{ font-size: 14px; }}
                bold {{ font-weight: bold; }}
                table {{ border-collapse: collapse; width: 100%; margin-bottom: 0px; font-size: 12px; }}
                th, td {{ border-collapse: collapse; border: 1px solid; padding: 3px; text-align: left; vertical-align: top; }}
                th {{ border-collapse: collapse; background-color: #f0f0f5; font-weight: bold; }}
                .logo {{ max-width: 100%; width: 180px; height: auto; }}
                .signature {{ max-height: 150px; width: 220px; height: auto; }}
                .border, .border {{ border-collapse: collapse; border: 1px solid black;}}
                .bordernull {{ border: 0;}}
                .haken {{ color: green; font-size: 14px; }}
                .kreuz {{ color: red; font-size: 14px; }}
            
            </style>
            </head>
            <body>

                <!-- Header -->
                <div id="header_content_1">
                </div>

                <!-- Content -->
                <div id="content">

                    <table class="border">
                        <tr>
                            <td style="border-right: 0;"><b>Erst- und Wiederholungsprüfung<br>
                            ortsveränderlicher elektrischer Geräte<br>
                            <small>Prüf- und Messprotokoll</small></b></td>
                            <td style="border-left: 0; text-align: right;">
                                <img src="data:image/png;base64,{self.data_to_append.get('company_and_inspector_data', {}).get('logo_str', '')}"
                                    alt="Logo" class="logo">
                            </td>
                        </tr>
                    </table>

                    <table class="border">
                        <tr>
                            <td style="border-right:0; width: 20%;">Nr.</td>
                            <td style="border-left:0; width: 30%;"><b>{calibration_number}</b></td>
                            <td style="border-right:0; width: 20%;">Kunden-Nr.</td>
                            <td style="border-left:0; width: 30%;">XXX</td>
                        </tr>
                    </table>

                    <table class="border">
                        <tr>
                            <td style="width: 50%;">Auftraggeber:<br>
                            <b>{Kunde}<br>
                            {self.data_to_append.get('waage_data', {}).get('Kunde_Strasse', '')}<br>
                            {self.data_to_append.get('waage_data', {}).get('Kunde_plz', '')} {self.data_to_append.get('waage_data', {}).get('Kunde_ort', '')}</b></td>
                            <td style="width: 50%;">Auftragnehmer:<br>
                            <b>{self.data_to_append.get('company_and_inspector_data', {}).get('firma', '')}<br>
                            {self.data_to_append.get('company_and_inspector_data', {}).get('strasse', '')}<br>
                            {self.data_to_append.get('company_and_inspector_data', {}).get('plz', '')} {self.data_to_append.get('company_and_inspector_data', {}).get('ort', '')}</b></td>
                        </tr>
                    </table>

                    <table class="border">
                        <tr>
                            <td>Prüfung nach: {vde_text}</td>
                        </tr>
                    </table>

                    <table class="border">
                        <tr>
                            <td class="bordernull"><b>Gerätedaten</b></td>
                        </tr>
                        <tr class="bordernull">
                            <td class="bordernull" style="width: 15%;">Herrsteller:</td>
                            <td class="bordernull" style="width: 30%;">{self.data_to_append.get('waage_data', {}).get('Hersteller', '')}</td>
                            <td class="bordernull" style="width: 15%;">Nennspannung:</td>
                            <td class="bordernull">{self.data_to_append.get('vde_data', {}).get('nennspannung', '')} V</td>
                            <td class="bordernull" style="width: 20%;">co Phi: {self.data_to_append.get('vde_data', {}).get('cosphi', '')}</td>
                        </tr>
                        <tr class="bordernull">
                            <td class="bordernull">Typ:</td>
                            <td class="bordernull">{self.data_to_append.get('waage_data', {}).get('Modell', '')}</td>
                            <td class="bordernull">Nennstrom:</td>
                            <td class="bordernull">{self.data_to_append.get('vde_data', {}).get('nennstrom', '')} A</td>
                            <td class="bordernull" style="width: 20%;">Schutzklasse: {schutzklasse_roman}</td>
                        </tr>
                        <tr class="bordernull">
                            <td class="bordernull">Ser-Nr.:</td>
                            <td class="bordernull">{self.data_to_append.get('waage_data', {}).get('S/N', '')}</td>
                            <td class="bordernull">Nennleistung:</td>
                            <td class="bordernull">{self.data_to_append.get('vde_data', {}).get('nennleistung', '')} W</td>
                            <td class="bordernull" style="width: 20%;"></td>
                        </tr>
                        <tr class="bordernull">
                            <td class="bordernull">Inv.-Nr.:</td>
                            <td class="bordernull">{self.data_to_append.get('waage_data', {}).get('Inventarnummer', '')}</td>
                            <td class="bordernull">Frequenz:</td>
                            <td class="bordernull">{self.data_to_append.get('vde_data', {}).get('frequenz', '')} Hz</td>
                            <td class="bordernull" style="width: 20%;"></td>
                        </tr>
                    </table>

                    <table class="border">
                        <tr class="bordernull">
                            <th style="width: 23.333%; text-align: center;">Sichtprüfung</th>
                            <th style="width: 10%; text-align: center;">i.O./n.i.O.</th>
                            <th style="width: 23.333%; text-align: center;">Sichtprüfung</th>
                            <th style="width: 10%; text-align: center;">i.O./n.i.O.</th>
                            <th style="width: 23.333%; text-align: center;">Sichtprüfung</th>
                            <th style="width: 10%; text-align: center;">i.O./n.i.O.</th>
                        </tr>
                        <tr class="bordernull">
                            <td class="bordernull" style="border-right: 1; width: 23.333%;"><small>Typenschild/ Warnhinweis/ Kennzeichnungen</small></td>
                            <td style="border-bottom: 0; width: 10%; text-align: center;"><span class="{('haken' if typenschild == haken else 'kreuz')}">{typenschild}</span></td>
                            <td class="bordernull" style="width: 23.333%;"><small>Kühlluftöffnungen/ Luftfilter</small></td>
                            <td style="border-bottom: 0; width: 10%; text-align: center;"><span class="{('haken' if kuehlluft == haken else 'kreuz')}">{kuehlluft}</span></td>
                            <td class="bordernull" style="width: 23.333%;"><small>Anzeichen von Überlastung/ unsachgemäßem Gebrauch</small></td>
                            <td style="border-bottom: 0; width: 10%; text-align: center;"><span class="{('haken' if ueberlastung == haken else 'kreuz')}">{ueberlastung}</span></td>
                        </tr>
                        <tr class="bordernull">
                            <td class="bordernull" style="width: 23.333%;"><small>Gehäuse/Schutzabdeckungen</small></td>
                            <td style="border-top: 0; border-bottom: 0; width: 10%; text-align: center;"><span class="{('haken' if gehaeuse == haken else 'kreuz')}">{gehaeuse}</span></td>
                            <td class="bordernull" style="width: 23.333%;"><small>Schalter, Steuer, Einstell- und Sicherheitsvorrichtungen</small></td>
                            <td style="border-top: 0; border-bottom: 0; width: 10%; text-align: center;"><span class="{('haken' if schalter == haken else 'kreuz')}">{schalter}</span></td>
                            <td class="bordernull" style="width: 23.333%;"><small>Sicherheitsbeeinträchtigende
                            Verschmutzung/Korrission/Alterung</small></td>
                            <td style="border-top: 0; border-bottom: 0; width: 10%; text-align: center;"><span class="{('haken' if verschmutzung == haken else 'kreuz')}">{verschmutzung}</span></td>
                        </tr>
                        <tr class="bordernull">
                            <td class="bordernull" style="width: 23.333%;"><small>Anschlussleitung/stecker, Anschlussklemmen und -adern</small></td>
                            <td style="border-top: 0; border-bottom: 0; width: 10%; text-align: center;"><span class="{('haken' if anschlussleitung == haken else 'kreuz')}">{anschlussleitung}</span></td>
                            <td class="bordernull" style="width: 23.333%;"><small>Bemessung der zugänglichen Gerätesicherung</small></td>
                            <td style="border-top: 0; border-bottom: 0; width: 10%; text-align: center;"><span class="{('haken' if bemessung == haken else 'kreuz')}">{bemessung}</span></td>
                            <td class="bordernull" style="width: 23.333%;"><small>Mechanische Gefährdung</small></td>
                            <td style="border-top: 0; border-bottom: 0; width: 10%; text-align: center;"><span class="{('haken' if mechanische_gefaehrdung == haken else 'kreuz')}">{mechanische_gefaehrdung}</span></td>
                        </tr>
                        <tr class="bordernull">
                            <td class="bordernull" style="width: 23.333%;"><small>Biegeschutz/ Zugentlastung</small></td>
                            <td style="border-top: 0; border-bottom: 0; width: 10%; text-align: center;"><span class="{('haken' if biegeschutz == haken else 'kreuz')}">{biegeschutz}</span></td>
                            <td class="bordernull" style="width: 23.333%;"><small>Beuteile und Baugruppen</small></td>
                            <td style="border-top: 0; border-bottom: 0; width: 10%; text-align: center;"><span class="{('haken' if bauteile == haken else 'kreuz')}">{bauteile}</span></td>
                            <td class="bordernull" style="width: 23.333%;"><small>Unzulässige Eingriffe und Änderungen</small></td>
                            <td style="border-top: 0; border-bottom: 0; width: 10%; text-align: center;"><span class="{('haken' if unzulaessige_eingriffe == haken else 'kreuz')}">{unzulaessige_eingriffe}</span></td>
                        </tr>
                        <tr class="bordernull">
                            <td class="bordernull" style="width: 23.333%;"><small>Leitungshalterungen, Sicherungshalter, usw.</small></td>
                            <td style="border-top: 0;width: 10%; text-align: center;"><span class="{('haken' if leitungshalterungen == haken else 'kreuz')}">{leitungshalterungen}</span></td>
                            <td class="bordernull" style="width: 23.333%;"></td>
                            <td style="border-top: 0; width: 10%; text-align: center;"></td>
                            <td class="bordernull" style="width: 23.333%;"></td>
                            <td style="border-top: 0; width: 10%; text-align: center;"></td>
                        </tr>
                    </table>

                    <table class="border">
                        <tr>
                            <th style="text-align: center;">Messungen</th>
                            <th style="text-align: center;">Grenzwert</th>
                            <th style="text-align: center;">Messwert</th>
                            <th style="text-align: center;">i.O./n.i.O.</th>
                            <th style="text-align: center;">Bemerkung</th>
                        </tr>
                        <tr>
                            <td style="width: 20%; text-align: right;"><small>Schutzleiterwiderstand (RPE)</small></td>
                            <td style="width: 20%; text-align: right;">RPE</td>
                            <td style="width: 20%; text-align: right;">{self.data_to_append.get('vde_data', {}).get('rpe', '')}</td>
                            <td style="width: 10%; text-align: center;">XX</td>
                            <td style="width: 30%;">{self.data_to_append.get('vde_data', {}).get('rpe_bemerkungen', '')}</td>
                        </tr>
                        <tr>
                            <td style="width: 20%; text-align: right;"><small>Isolationswiderstand (RISO)</small></td>
                            <td style="width: 20%; text-align: right;">RISO</td>
                            <td style="width: 20%; text-align: right;">{self.data_to_append.get('vde_data', {}).get('riso', '')}</td>
                            <td style="width: 10%;text-align: center;">XX</td>
                            <td style="width: 30%;">{self.data_to_append.get('vde_data', {}).get('riso_bemerkungen', '')}</td>
                        </tr>
                        <tr>
                            <td style="width: 20%; text-align: right;"><small>Schutzleiterstrom (IPE)</small></td>
                            <td style="width: 20%; text-align: right;">IPE</td>
                            <td style="width: 20%; text-align: right;">{self.data_to_append.get('vde_data', {}).get('ipe', '')}</td>
                            <td style="width: 10%;text-align: center;">XX</td>
                            <td style="width: 30%;">{self.data_to_append.get('vde_data', {}).get('ipe_bemerkungen', '')}</td>
                        </tr>
                        <tr>
                            <td style="width: 20%; text-align: right;"><small>Berührungsstrom (IB)</small></td>
                            <td style="width: 20%; text-align: right;">IB</td>
                            <td style="width: 20%; text-align: right;">{self.data_to_append.get('vde_data', {}).get('ib', '')}</td>
                            <td style="width: 10%; text-align: center;">XX</td>
                            <td style="width: 30%;">{self.data_to_append.get('vde_data', {}).get('ib_bemerkungen', '')}</td>
                        </tr>
                    </table>

                    <table class="border">
                        <tr class="bordernull">
                            <th style="width: 20%;">Funktionsprüfung:</th>
                            <th style="width: 20%; text-align: center;">i.O./n.i.O.</th>
                            <td class="bordernull" style="border-bottom: 0; width: 60%;"></td>
                        </tr>
                        <tr class="bordernull">
                            <td style="width: 20%;">Funktion des Gerätes</td>
                            <td style="width: 20%; text-align: center;">XX</td>
                            <td class="bordernull" style="border-top: 0; width: 60%;"></td>
                        </tr>
                    </table>
                    
                    <table class="border">
                        <tr>
                            <td style="width: 25%;">Verwendetes Messgerät:</td>
                            <td style="width: 75%;">{self.data_to_append.get('vde_data', {}).get('vde_messgeraet', '')}</td>
                        </tr>
                    </table>


                    <table class="border">
                        <tr>
                            <td style="width: 50%; height: 2.5cm;">Mängel/Bemerkungen:<br>
                            {self.data_to_append.get('bemerkungen', '')}
                            </td>
                            <td class="bordernull" style="width: 35%;">Das elektrische Gerät entspricht den anerkannten
                            Regeln der Elektrotechnik. Ein sicherer Gebrauch bei
                            bestimmungsgemäßer Anwendung ist gewährleistet
                            </td>
                            <td class="bordernull" style="text-align: center; vertical-align: middle; width: 15%">XX</td>
                        </tr>
                    </table>
                    
                    <table class="border">
                        <tr>
                            <td class="bordernull" rowspan="2" style="vertical-align: bottom; width: 30%;">Nächster Prüftermin<br>{self.data_to_append.get('datum_in_einem_jahr', '')}
                            </td>
                            
                            
                            <td class="bordernull" style="width: 35%;">Prüfer/In: {self.data_to_append.get('company_and_inspector_data', {}).get('pruefer_name', '')}</td>
                            
                            
                            <td class="bordernull" style="width: 35%;"><img
                                  src="data:image/png;base64,{self.data_to_append.get('company_and_inspector_data', {}).get('unterschrift_str', '')}"
                                  alt="Unterschrift" class="signature"></td>
                        </tr>
                        <tr>
                            
                            <td class="bordernull" style="width: 35%;">Datum: {self.data_to_append.get('pruefdatum', '')}</td>
                            <td class="bordernull" style="width: 35%;">Unterschrift</td>
                            <td class="bordernull" style="width: 30%;"></td>
                        </tr>
                    </table>



                </div>

                <!-- Footer -->
                <div id="footer_content">
                    <table>
                        <tr>
                            <td width="50%">
                                <img src="data:image/png;base64,{self.data_to_append.get('company_and_inspector_data', {}).get('logo_str', '')}"
                                     alt="Logo" style="width:120px; height:auto;">
                            </td>
                            <td width="50%" style="text-align: right; font-size: 10px;">
                                <h4>{self.data_to_append.get('company_and_inspector_data', {}).get('firma', '')},
                                {self.data_to_append.get('company_and_inspector_data', {}).get('strasse', '')},
                                {self.data_to_append.get('company_and_inspector_data', {}).get('plz', '')}, 
                                {self.data_to_append.get('company_and_inspector_data', {}).get('ort', '')},Germany<br>
                                +49 4329 911 94 14, waagen-kalibrieren.de</h4>
                            </td>
                        </tr>
                    </table>
                </div>

            </body>
        </html>
        """

        # HTML in PDF umwandeln mit xhtml2pdf
        result_file = open(filename, "w+b")
        pisa_status = pisa.CreatePDF(html_template, dest=result_file)
        result_file.close()

        if pisa_status.err:
            return False
        return True
