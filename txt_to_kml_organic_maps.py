# -*- coding: utf-8 -*-
import csv, re, datetime, sys, os

def txt_to_kml():
        
        if len(sys.argv) == 2:
                txt_file = sys.argv[1]
                directory = re.compile(r'(.*)\\[^\\]*$').search(sys.argv[0]).group(1)
                list_name = re.compile(r'([^\\]+)\.(txt|csv)$').search(txt_file).group(1)
        else:
                directory = re.compile(r'(.*)\\[^\\]*$').search(sys.argv[0]).group(1)
                for f in os.listdir(directory):
                        if f not in ('README.txt', 'Template List.txt') and (f.endswith('.txt') or f.endswith('.csv')):
                                txt_file = fr"{directory}\{f}"
                                list_name = re.compile(r'(.*)\.(txt|csv)$').search(f).group(1)
        if 'txt_file' not in locals():
                print('No list file found. Please make one first')
                return
        creation_time = datetime.datetime.now()        
        template = []
        with open(fr"{directory}\Template DO NOT DELETE.kml", 'r', encoding='utf-8') as kml_template:
                template += kml_template.readlines()
        with open(txt_file,"r", encoding='utf-8', newline='') as txt:
                reader = csv.DictReader(txt, delimiter=',')
                fieldnames = reader.fieldnames
                txt_rows = tuple(reader)
                creation_times = tuple((creation_time+datetime.timedelta(seconds=i+1)).strftime("%Y-%m-%dT%H:%M:%SZ") for i in range(len(txt_rows)))
                with open(fr'{directory}\{list_name}.kml', 'w', encoding='utf-8') as kml:
                        #Style info
                        kml.writelines(template[:115])
                        #List info
                        kml.writelines([f'  <name>{list_name}</name>\n', f'  <description>{f"{list_name} List"}</description>\n'] + template[117:120] + [f'      <mwm:lang code="default">{list_name}</mwm:lang>\n'] + template[121:125] + [f'      <mwm:lang code="default">{f"{list_name} List"}</mwm:lang>\n', '    </mwm:description>\n'] + [f'    <mwm:lastModified>{creation_time.strftime("%Y-%m-%dT%H:%M:%SZ")}</mwm:lastModified>\n'] + template[128:130])
                        #List points
                        for k, row in enumerate(txt_rows):
                                kml.writelines(['  <Placemark>\n'] + [f'    <name>{row[fieldnames[0]]}</name>\n', f'    <description>{row[fieldnames[1]]}</description>\n', f'    <TimeStamp><when>{creation_times[k]}</when></TimeStamp>\n', f'    <styleUrl>#placemark-{row[fieldnames[4]]}</styleUrl>\n', f'    <Point><coordinates>{row["Longitude"]},{row["Latitude"]}</coordinates></Point>\n'] + template[136:141] + [f'        <mwm:lang code="default">{row[fieldnames[1]]}</mwm:lang>\n'] + template[142:144] + [f'        <mwm:lang code="default">{row[fieldnames[0]]}</mwm:lang>\n'] + template[145:150])
                        #List end
                        kml.writelines(template[170:])
        print("Done! Don't forget to place the KML file in your phone and then load it to Organic Maps.\nBonne voyage!")
#******************************************************************

txt_to_kml()