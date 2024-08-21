import os
import configparser
import base64
import io
import matplotlib.pyplot as plt

from xhtml2pdf import pisa
from datetime import datetime, timedelta
from PIL import Image


class PDFGeneratorTemp:

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

    def add_tempjustage_data(self, temp_data):
        try:
            # Daten extrahieren
            ist_temp1 = float(temp_data['ist_temp1'])
            soll_temp1 = float(temp_data['soll_temp1'])
            ist_temp2 = float(temp_data['ist_temp2'])
            soll_temp2 = float(temp_data['soll_temp2'])
            temp_messgeraet = temp_data['temp_messgeraet']
            umgebung_temp = temp_data['umgebung_temp']

            # Daten für das Diagramm
            labels = ["Prüfpunkt 1", "Prüfpunkt 2"]
            ist_values = [ist_temp1, ist_temp2]
            soll_values = [soll_temp1, soll_temp2]

            # Diagramm erstellen
            plt.figure(figsize=(7, 3), dpi=300)  # Reduzierte Größe und DPI
            plt.box(on=True)
            plt.rcParams['font.family'] = 'Calibri'
            plt.rcParams['font.size'] = 8  # Kleinere Basisschriftgröße

            plt.plot(labels, ist_values, marker='x', linestyle='--', color='red', label='AS-Found-Temperatur',
                     linewidth=1.5)
            plt.plot(labels, soll_values, marker='x', linestyle='--', color='green', label='AS-Left-Temperatur',
                     linewidth=1.5)

            x_offset = 0.05

            for i, value in enumerate(ist_values):
                plt.axhline(y=value, color='red', linestyle='dotted', linewidth=0.8)
                plt.text(-0.2 - x_offset, value, f'{value:.1f} °C', va='center', ha='right', fontsize=10,
                         color='red')

            for i, value in enumerate(soll_values):
                plt.axhline(y=value, color='green', linestyle='dotted', linewidth=0.8)
                plt.text(-0.2 + x_offset, value, f'{value:.1f} °C', va='center', ha='left', fontsize=10,
                         color='green')

            plt.xlim(-0.5 - x_offset, 1.5 + x_offset)
            plt.ylim(min(ist_values + soll_values) - 10, max(ist_values + soll_values) + 10)

            plt.ylabel("Temperatur (°C)", fontsize=8)
            plt.xticks(labels, fontsize=8)
            plt.legend(fontsize=8)
            plt.grid(axis='y', linestyle='--', alpha=0.5)
            plt.tick_params(axis='y', labelsize=8)

            # Diagramm speichern
            chart_buffer = io.BytesIO()
            plt.savefig(chart_buffer, format="png", dpi=300, bbox_inches='tight', pad_inches=0.1)
            chart_buffer.seek(0)
            chart_str = base64.b64encode(chart_buffer.getvalue()).decode("utf-8")

            # Daten speichern
            self.data_to_append['temp_data'] = {
                'ist_temp1': ist_temp1,
                'soll_temp1': soll_temp1,
                'ist_temp2': ist_temp2,
                'soll_temp2': soll_temp2,
                'temp_messgeraet': temp_messgeraet,
                'umgebung_temp': umgebung_temp,
                'chart_str': chart_str
            }
            plt.close()

        except (KeyError, ValueError, TypeError) as e:
            print(f"Error in add_tempjustage_data: {e}")

    def add_pruefdatum_bemerkungen(self, pruefdatum, bemerkungen):
        """Fügt Prüfdatum, Bemerkungen und das Datum ein Jahr später hinzu."""

        # Formatiere das Prüfdatum
        pruefdatum_obj = datetime.strptime(pruefdatum, "%d.%m.%Y")
        pruefdatum_str = pruefdatum_obj.strftime("%d.%m.%Y")

        # Berechne das Datum in einem Jahr
        datum_in_einem_jahr = pruefdatum_obj + timedelta(days=365)
        datum_in_einem_jahr_str = datum_in_einem_jahr.strftime("%m.%Y")

        # Speichere pruefdaten und bemerkungen
        self.data_to_append['pruefdatum'] = pruefdatum_str
        self.data_to_append['datum_in_einem_jahr'] = datum_in_einem_jahr_str
        self.data_to_append['bemerkungen'] = bemerkungen

    def generate_calibration_number(self):
        pruefer_name = self.data_to_append.get('company_and_inspector_data', {}).get('pruefer_name', '')
        initials = ''.join([name[0].upper() for name in pruefer_name.split() if name])
        current_date = datetime.now().strftime("%m%y")
        waage_id = self.data_to_append.get('waage_data', {}).get('WJ-Nummer', '')
        return f"TK_{initials}_{current_date}_{waage_id}"

    def get_calibration_number(self):
        return self.generate_calibration_number()

    def generate_pdf(self, filename="report.pdf"):
        calibration_number = self.generate_calibration_number()

        Abweichung1 = round(float(self.data_to_append.get('temp_data', {}).get('ist_temp1', '0')) - float(
            self.data_to_append.get('temp_data', {}).get('soll_temp1', '0')), 2)
        Abweichung2 = round(float(self.data_to_append.get('temp_data', {}).get('ist_temp2', '0')) - float(
            self.data_to_append.get('temp_data', {}).get('soll_temp2', '0')), 2)

        if Abweichung1 == 0:
            Abweichung_Text = "Im Zuge der Kalibrierung wurde keine Abweichung in der Heizkennlinie des Feuchtebestimmers festgestellt."
            Abweichung_Text_eng = "During the calibration, no deviation was detected in the heating characteristic of the moisture analyzer."
        else:
            Abweichung_Text = "Im Zuge der Kalibrierung wurde eine Abweichung in der Heizkennlinie des Feuchtebestimmers festgestellt. Diese Abweichung wurde gemäß den spezifischen Vorgaben des Herstellers korrigiert, um die Genauigkeit der Messungen sicherzustellen."
            Abweichung_Text_eng = "During the calibration, a deviation in the heating characteristic of the moisture analyzer was detected. This deviation was corrected according to the manufacturer's specific instructions to ensure the accuracy of the measurements."

        Aufheizzyklus = self.data_to_append.get('waage_data', {}).get('Aufheizzyklus', '')
        if Aufheizzyklus == "None":
            Aufheizzyklus = 15

        TempHerstellertoleranz = self.data_to_append.get('waage_data', {}).get('TempHerstellertoleranz', '')
        toleranz_text = "Herstellerzoleranz"
        toleranz_text_eng = "Manufacturer's tolerance"
        if TempHerstellertoleranz == "None":
            TempHerstellertoleranz = 5.0
            toleranz_text = "Tolleranz"
            toleranz_text_eng = "Tolerance"

        # Mindestens eine Nachkommastelle
        try:
            TempHerstellertoleranz = float(TempHerstellertoleranz)
            if TempHerstellertoleranz.is_integer():
                TempHerstellertoleranz = format(TempHerstellertoleranz, '.1f')
        except ValueError:
            # Falls der Wert keine gültige Zahl ist, bleibt er unverändert
            pass

        Kunde = self.data_to_append.get('waage_data', {}).get('Kunde_name1', '')

        if self.data_to_append.get('waage_data', {}).get('Kunde_name2', '') != "":
            Kunde = self.data_to_append.get('waage_data', {}).get('Kunde_name1', '') + "<br>" + self.data_to_append.get(
                'waage_data', {}).get('Kunde_name2', )
        elif self.data_to_append.get('waage_data', {}).get('Kunde_name3', '') != "":
            Kunde = self.data_to_append.get('waage_data', {}).get('Kunde_name1', '') + "<br>" + self.data_to_append.get(
                'waage_data', {}).get('Kunde_name2', ) + "<br>" + self.data_to_append.get('waage_data', {}).get(
                'Kunde_name3', )

        html_template = f"""
        <html><!-- DIN A4 21x29,7 cm -->
            <head>
            <style>
                @page {{ size: a4 portrait;
                    @frame header_frame {{
                        -pdf-frame-content: header_content_1;
                        left: 2cm; 
                        right: 2cm;
                        top: 2cm; 
                    }}
                    @frame content_frame {{
                        left: 2cm;
                        right: 2cm;
                        top: 5cm;
                    }}
                    @frame footer_frame {{
                        -pdf-frame-content: footer_content;
                        left: 2cm;
                        right: 2cm;
                        bottom: 0cm;
                        height: 2cm;
                    }}
                }} 
                @page second_template {{ size: a4 portrait;
                    @frame header_frame {{
                        -pdf-frame-content: header_content_2;
                        left: 2cm; 
                        right: 2cm;
                        top: 2cm; 
                    }}
                    @frame content_frame {{
                        left: 2cm;
                        right: 2cm;
                        top: 4cm;
                    }}
                    @frame footer_frame {{
                        -pdf-frame-content: footer_content;
                        left: 2cm;
                        right: 2cm;
                        bottom: 0cm;
                        height: 2cm;
                    }}
                }}
                @page third_template {{  size: a4 portrait;
                    @frame header_frame {{
                        -pdf-frame-content: header_content_3;
                        left: 2cm; 
                        right: 2cm;
                        top: 2cm; 
                    }}
                    @frame content_frame {{
                        left: 2cm;
                        right: 2cm;
                        top: 4cm;
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
                h1 {{ font-size: 24px; font-weight: bold; margin-top: 0px; margin-bottom: 0px; }}
                h2 {{ font-size: 22px; margin-top: 0px; margin-bottom: 0px; }}
                h4 {{ margin-top: 0px; margin-bottom: 0px; }}
                p {{ font-size: 12px; }}
                .logo {{ width: 200px; }}
                table {{ border-collapse: collapse; width: 100%; margin-bottom: 10px; font-size: 12px; line-height: 1.2; }}
                th, td {{ border: 0px solid #222; padding: 0px; text-align: left; vertical-align: top; padding-bottom: 5px; }}
                .border, .border {{ border: 1px solid #222; padding: 4px;}}
                th {{ background-color: #f0f0f5; font-weight: bold; }}
                .grafik {{ background-color: #f0f8ff; height: 250px; margin-bottom: 20px; display: flex;
                    align-items: center; justify-content: center; font-size: 18px; }}
                .check-mark {{ color: green; font-weight: bold; }}
                .cross-mark {{ color: red; font-weight: bold; }}
                .logo {{ max-width: 100%; width: 150px; height: auto; }}
                .signature {{ max-height: 120px; width: 180px; height: auto; }}
                .chart {{ width: 100%; max-width: 800px; height: auto; }}
            </style>
            </head>
            
            <body>
            
                <!-- Header für Seite 1 -->
                <div id="header_content_1">
                    <div>
                        <table>
                            <tr>
                                <td width="60%">
                                    <h1>{self.data_to_append.get('company_and_inspector_data', {}).get('firma', '')}</h1>
                                    <p>
                                    Kalibrierlaboratorium für elektronische Waagen<br>
                                    <i>Calibration laboratory for Electronic Balances / Scales</i><br>
                                    </p>
                                </td>
                                <td width="40%" style="text-align: right;">
                                    <img src="data:image/png;base64,{self.data_to_append.get('company_and_inspector_data', {}).get('logo_str', '')}"
                                        alt="Logo" class="logo" style="width:250px;">
                                </td>
                            </tr>
                        </table>
                    </div>
                </div>
        
                <!-- Header für Seite 2 -->
                <div id="header_content_2">
                    <table>
                        <tr>
                            <td width="8%">Seite<br><small><i>Page</i></small></td>
                            <td width="5%"><pdf:pagenumber><br><small><i><pdf:pagenumber></i></small></td>
                            <td width="25%">zum Kalibrierschein<br><small><i>of the calibration certificate</i></small></td>
                            <td width="30%">{calibration_number}</td>
                            <td width="5%">vom</td>
                            <td width="5%">{self.data_to_append.get('pruefdatum', '')}</td>
                        </tr>
                      </table>
                </div>
        
                <!-- Header für Seite 3 -->
                <div id="header_content_3">
                    <table>
                        <tr>
                            <td width="8%">Seite<br><small><i>Page</i></small></td>
                            <td width="5%"><pdf:pagenumber><br><small><i><pdf:pagenumber></i></small></td>
                            <td width="25%">zum Kalibrierschein<br><small><i>of the calibration certificate</i></small></td>
                            <td width="30%">{calibration_number}</td>
                            <td width="5%">vom</td>
                            <td width="5%">{self.data_to_append.get('pruefdatum', '')}</td>
                        </tr>
                      </table>
                </div>
                
                <div id="content">
                    <!-- Content Seite 1 -->
                    <table>
                        <tr>
                            <td width="70%"><h2>Prüfprotokoll Temperaturkalibrierung</h2><small><i>Test protocol temperature calibration</i></small></td>
                            <td width="30%" style="vertical-align: middle; text-align: center;"><b>{calibration_number}</b></td>
                        </tr>
                    </table>
                    
                    <hr class="solid">

                    <table style="border-top: 1px solid;">
                        <tr>
                            <td style="width:30%; padding-top:5px;">Gegenstand<br><small><i>Object</i></small></td>
                            <td style="width:30%; padding-top:5px;">Feuchtebestimmer<br><small><i>Moisture analyzer</i></small></td>
                            <td rowspan="5" style="width:40%; padding-top:5px; text-align:justify; line-height: 12px;">
                            
                              Dieses Kalibrierzertifikat bestätigt, dass das vorliegende Messgerät wie vorgesehen funktioniert und die Messergebnisse präzise in den international anerkannten SI-Einheiten angegeben sind. Die durchgeführte Kalibrierung wurde mit Methoden durchgeführt, die auf nationale Standards zurückgeführt werden können, was die Genauigkeit und Verlässlichkeit der Messungen gewährleistet. Es liegt in der Verantwortung des Verwenders, das Gerät in den empfohlenen regelmäßigen Abständen erneut kalibrieren zu lassen, um eine gleichbleibend hohe Messqualität sicherzustellen.
                              <br><br><i><small>This calibration certificate confirms that the present measuring device functions as intended and the measurement results are precisely stated in the internationally recognized SI units. The calibration was performed using methods that can be traced back to national standards, ensuring the accuracy and reliability of the measurements. It is the responsibility of the user to have the device recalibrated at the recommended regular intervals to maintain a consistently high measurement quality.</i>
                              </small></td>
                        </tr>
                        <tr>
                            <td>Hersteller<br><small><i>Manufacturer</i></small></td>
                            <td>{self.data_to_append.get('waage_data', {}).get('Hersteller', '')}</td>
                        </tr>
                        <tr>
                            <td>Typ<br><small><i>Type</i></small></td>
                            <td>{self.data_to_append.get('waage_data', {}).get('Modell', '')}</td>
                        </tr>
                        <tr>
                            <td>Fabrikat/Serien-Nr.<br><small><i>Serial number</i></small></td>
                            <td>{self.data_to_append.get('waage_data', {}).get('S/N', '')}</td>
                        </tr>
                        <tr>
                            <td>Auftraggeber<br><small><i>Customer</i></small></td>
                            <td>{Kunde}<br>
                            {self.data_to_append.get('waage_data', {}).get('Kunde_Strasse', '')}<br>
                            {self.data_to_append.get('waage_data', {}).get('Kunde_plz', '')}<br>
                            {self.data_to_append.get('waage_data', {}).get('Kunde_ort', '')}<br></td>
                        </tr>
                    </table>
                    <table>
                        <tr>
                            <td style="width:250px">Auftragsnummer<br><small><i>Order No.</i></small></td>
                            <td>{self.data_to_append.get('waage_data', {}).get('Auftragsnummer', '')}</td>
                        </tr>
                        <tr>
                            <td>Anzahl Seiten des Kalibrierscheins<br><small><i>Number of pages of the certificate</i></small></td>
                            <td>3</td>
                        </tr>
                        <tr>
                            <td>Datum der Kalibrierung<br><small><i>Date of calibration</i></small></td>
                            <td>{self.data_to_append.get('pruefdatum', '')}</td>
                        </tr>
                    </table>
                    
                    <div><p>Dieser Kalibrierschein darf ausschließlich im Original weitergegeben werden.
                    Für Auszüge oder Änderungen ist die Genehmigung des ausstellenden Kalibrierlaboratoriums einzuholen.
                    Kalibrierscheine ohne Unterschrift haben keine Gültigkeit.</p>
                    <p><small><i>This calibration certificate may only be passed on in its original form.
                    Permission from the issuing calibration laboratory must be obtained for any extracts or changes. Calibration
                    certificates without a signature are invalid.</i></small></p></div>
                    
                    <div style="bottom: 0px">
                        <hr style="margin-top: 20px;" class="solid">
                        <table>
                            <tr>
                                <td rowspan="2"><img src="data:image/png;base64,{self.data_to_append.get('company_and_inspector_data', {}).get('stempel_str', '')}"
                                       alt="Stempel" style="width:120px; height:auto;"></td>
                                </td>
                                <td>Datum<br><small><i>Date</i></small></td>
                                <td>Prüfer<br><small><i>Person in charge</i></small><br>
                                <img
                                  src="data:image/png;base64,{self.data_to_append.get('company_and_inspector_data', {}).get('unterschrift_str', '')}"
                                  alt="Unterschrift" class="signature"></td>
                            </tr>
                            <tr>
                                <td style="padding:0px;">{self.data_to_append.get('pruefdatum', '')}</td>
                                <td style="padding:0px;">{self.data_to_append.get('company_and_inspector_data', {}).get('pruefer_name', '')}</td>
                            </tr>
                        </table>
                        <hr class="solid">
                    </div>
                    
                    <!-- Content Seite 1 ENDE -->
                    <pdf:nexttemplate name="second_template"/>
                    <pdf:nextpage/>
                    <!-- Content Seite 2 -->
                    
                    <table>
                        <tr>
                            <td style="width:30%;"><h2>Prüfbedingungen</h2><small><i>Test conditions</i></small></td>
                            <td></td>
                        </tr>
                        <tr>
                            <td>Datum der Kalibrierung:<br><small><i>Date of calibration</i></small></td>
                            <td>{self.data_to_append.get('pruefdatum', '')}</td>
                        </tr>
                        <tr>
                            <td>Umgebungstemperatur:<br><small><i>Ambient temperature</i></small></td>
                            <td>{self.data_to_append.get('temp_data', {}).get('umgebung_temp', '')} °C</td>
                        </tr>
                        <tr>
                            <td>Ort der Kalibrierung:<br><small><i>Location of calibration</i></small></td>
                            <td>Standort: {self.data_to_append.get('waage_data', {}).get('Standort', '')}</br>
                            {self.data_to_append.get('waage_data', {}).get('Raum', '')}
                            </td>
                        </tr>
                        <tr>
                            <td>Messbedingungen:<br><small><i>Measurement conditions</i></small></td>
                            <td>Unruhe - {self.data_to_append.get('waage_data', {}).get('Unruhe', '')}<br>Luftbewegung -
                            {self.data_to_append.get('waage_data', {}).get('Luftbewegung', '')}<br>Verschmutzung -
                            {self.data_to_append.get('waage_data', {}).get('Verschmutzung', '')}
                            </td>
                        </tr>
                    </table>
                    <table>
                        <tr>
                            <td style="width:30%;">Verwendete Messmittel<br><small><i>Measuring equipment used</i></small></td>
                            <td>{self.data_to_append.get('temp_data', {}).get('temp_messgeraet', '')}</td>
                        </tr>
                    </table>
                    <table>
                        <tr>
                            <td style="width:30%;">Kalibrierverfahren<br><small><i>Calibration method</i></small></td>
                            <td>Das Temperaturkalibrierset wird in die Kammer des Feuchtebestimmers eingesetzt und diese verschlossen.
                            Anschließend wird die Heizkammer anhand des vorgegebenen Heizprofils auf die jeweilige Prüftemperatur
                            erwärmt. Nach Ablauf der festgelegten Zeit erfolgt die Ablesung des angezeigten Wertes des
                            Temperaturkalibriersets und der Abgleich mit der Ist-Temperatur. Die ermittelte Messgröße
                            bezieht sich dabei ausschließlich auf die Temperatur des Sensors im Kalibrierset, unter Berücksichtigung
                            seiner Position, Wärmekapazität und Reflexionsgrad. Es wird keine Aussage über die exakte Temperatur
                            innerhalb der Heizkammer oder der Probe getroffen.
                            <br><br><small><i>The temperature calibration set is inserted into the chamber of the moisture analyzer and
                            the chamber is closed. Subsequently, the heating chamber is heated to the respective test temperature
                            using the specified heating profile. After the defined time has elapsed, the displayed value of the
                            temperature calibration set is read and compared with the actual temperature. The measured variable
                            refers exclusively to the temperature of the sensor in the calibration set, taking into account its
                            position, heat capacity and degree of reflection. No statement is made about the exact temperature
                            inside the heating chamber or the temperature of the sample itself.</i></small></td>
                        </tr>
                    </table>
                    <table>
                        <tr>
                            <td style="width:30%;">Aufheizphase:<br><small><i>Heating phase</i></small></td>
                            <td style="width:10%;">{Aufheizzyklus} min</td>
                            <td>je Aufheizzyklus<br><small><i>per heating cycle</i></small></td>
                        </tr>
                    </table>
                    <table>
                        <tr>
                            <td style="width:30%;">Heizprofil<br><small><i>Heating profile</i></small></td>
                            <td>Temperaturkalibriermodus<br><small><i>Temperature calibration mode</i></small></td>
                        </tr>
                        <tr>
                            <td style="width:30%;">Bemerkungen<br><small><i>Remarks</i></small></td>
                            <td>{self.data_to_append.get('bemerkungen', '')}</td>
                        </tr>
                    </table>

                    <!-- Content Seite 2 ENDE -->
                    <pdf:nexttemplate name="third_template"/>
                    <pdf:nextpage/>
                    <!-- Content Seite 3 -->
                    
                    <table>
                        <tr>
                            <td style="width:200px;"><h2>Messergebnisse</h2><small><i>Measurement results</i></small></td>
                            <td></td>
                        </tr>
                    </table>
                    
                    <table class="border">
                        <tr class="border">
                            <th class="border">Prüfpunkt<br><small><i>Test point</i></small></th>
                            <th class="border">Soll-Temp<br><small><i>Target-Temp</i></small></th>
                            <th class="border">Ist-Temp<br><small><i>Actual-Temp</i></small></th>
                            <th class="border">Abweichung<sup><small>1</small></sup><br><small><i>Deviation<sup><small>1</small></sup></i></small></th>
                            <th class="border">Justiert auf <sup><small>2</small></sup><br><small><i>Adjusted to<sup><small>2</small></sup></i></small></th>
                            <th class="border">Toleranz <sup><small>3</small></sup><br><small><i>Tolerance<sup><small>3</small></sup></i></small></th>
                            <th class="border">Konformität <sup><small>4</small></sup><br><small><i>Conformity<sup><small>4</small></sup></i></small></th>
                        </tr>
                        <tr class="border">
                            <td class="border" style="text-align:center;">1</td>
                            <td class="border">{self.data_to_append.get('temp_data', {}).get('soll_temp1', '')} °C</td>
                            <td class="border">{self.data_to_append.get('temp_data', {}).get('ist_temp1', '')} °C</td>
                            <td class="border">{Abweichung1} °C</td>
                            <td class="border">{self.data_to_append.get('temp_data', {}).get('soll_temp1', '')} °C</td>
                            <td class="border">{TempHerstellertoleranz} °C</td>
                            <td class="border" style="text-align:center;"><span class="check-mark">&#10004;</span></td>
                        </tr>
                        <tr class="border">
                            <td class="border" style="text-align:center;">2</td>
                            <td class="border">{self.data_to_append.get('temp_data', {}).get('soll_temp2', '')} °C</td>
                            <td class="border">{self.data_to_append.get('temp_data', {}).get('ist_temp2', '')} °C</td>
                            <td class="border">{Abweichung2} °C</td>
                            <td class="border">{self.data_to_append.get('temp_data', {}).get('soll_temp2', '')} °C</td>
                            <td class="border">{TempHerstellertoleranz} °C</td>
                            <td class="border" style="text-align:center;"><span class="check-mark">&#10004;</span></td>
                        </tr>
                    </table>
                    
                    <div>
                        <p class="check-mark">&#10003; Abweichungen liegen innerhalb der Toleranz.</p>
                        <p>{Abweichung_Text}<br><small><i>{Abweichung_Text_eng}</i></small></p>
                    </div>

                    <table>
                        <tr>
                            <td style="width:1%;"><sup><small>1)</small></sup></td>
                            <td><small>Die Differenz zwischen der angezeigten Temperatur des Geräts und dem Sollwert vor der Justage.
                            <br><i>The difference between the temperature displayed by the device and the target temperature before
                            the adjustment.</i></small></td>
                        </tr>
                        <tr>
                            <td style="width:1%;"><sup><small>2)</small></sup></td>
                            <td><small>Die Temperatur, auf die das Gerät während der Kalibrierung justiert wurde.
                            <br><i>The temperature to which the device was adjusted during calibration.</i></small></td>
                        </tr>
                        <tr>
                            <td style="width:1%;"><sup><small>3)</small></sup></td>
                            <td><small>{toleranz_text} lt. Spezifikation.
                            <br><i>{toleranz_text_eng} according to specification.</i></small></td>
                        </tr>
                        <tr>
                            <td style="width:1%;"><sup><small>4)</small></sup></td>
                            <td><small>Bewertungskriterium: | [Abweichung nach Justage] | ≤ [Toleranz]
                            <br><i>Assessment criterion: | [Error after adjustment] | ≤ [Tolerance]</i>
                            <br>Gibt an, ob die Abweichung innerhalb der zulässigen Toleranz liegt (<span class="check-mark">&#10004;</span>
                            = ja, <span class="cross-mark">&#10008;</span> = nein).
                            <br><i>Indicates whether the deviation is within the permissible tolerance (<span class="check-mark">&#10004;</span>
                            = yes, <span class="cross-mark">&#10008;</span> = no).</i></small></td>
                        </tr>
                    </table>
                    <div>
                        <img src="data:image/png;base64,{self.data_to_append.get('temp_data', {}).get('chart_str', '')}"
                        alt="Temperaturvergleich" class="chart">
                    </div>
                    <div>Die roten Punkte zeigen die tatsächlich gemessenen Temperaturen vor der Justage, die grünen Punkte zeigen die Temperaturen auf die justiert wurde.
                        Der Abstand zwischen roter und grüner Linie kann als Indikator zur Abschätzung der Genauigkeit des Gerätes dienen.
                        <br><small><i>The red points show the actually measured temperatures before adjustment, the green points show the temperatures to which the device was adjusted.
                        The distance between the red and green lines can serve as an indicator for estimating the accuracy of the device.</i></small>
                    </div>
                    
                    <!-- Content Seite 3 ENDE -->
                
                </div>
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