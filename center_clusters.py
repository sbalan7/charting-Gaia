import pandas as pd
import json
import os


with open('select.json', 'r') as f:
    data = json.load(f)

def center_cluster(cluster_name):
    clu_path = os.getcwd() + '/cluster_tsvs/' + cluster_name.replace(' ', '_') + '.tsv'
    clu_headers = 'sentRA  sentDE   _r   _RAJ2000h _RAJ2000m _RAJ2000s   _DEJ2000h _DEJ2000m _DEJ2000s    RA_ICRS   e_RA   DE_ICRS  e_DE  Source   Plx    e_Plx   pmRA   e_pmRA   pmDE   e_pmDE   Dup   FG  e_FG    Gmag     e_Gmag FBP    e_FBP  BPmag   e_BPmag    FRP   e_FRP   RPmag     e_RPmag  BP-RP   RV   e_RV  Teff   AG   E(BP-RP) Rad  Lum  '.split()

    clu_df = pd.read_csv(clu_path,
                         sep='\s+',
                         skiprows=1,
                         names=clu_headers)

    return str(clu_df['sentRA'].mean()), str(clu_df['sentDE'].mean())

for cluster_name, subdata in data.items():
    data[cluster_name]['centerRA'], data[cluster_name]['centerDE'] = center_cluster(cluster_name)

with open('select.json', 'w') as f:
    json.dump(data, f)
