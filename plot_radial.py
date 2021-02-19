import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
import os

with open('select.json') as f:
    data = json.load(f)

#pd.set_option('display.max_columns', None)

# Load the cluster data downloaded
def load_data(cluster_name):
    clu_path = os.getcwd() + '/cluster_tsvs/' + cluster_name.replace(' ', '_') + '.tsv'
    clu_headers = 'sentRA  sentDE   _r   _RAJ2000h _RAJ2000m _RAJ2000s   _DEJ2000h _DEJ2000m _DEJ2000s    RA_ICRS   e_RA   DE_ICRS  e_DE  Source   Plx    e_Plx   pmRA   e_pmRA   pmDE   e_pmDE   Dup   FG  e_FG    Gmag     e_Gmag FBP    e_FBP  BPmag   e_BPmag    FRP   e_FRP   RPmag     e_RPmag  BP-RP   RV   e_RV  Teff   AG   E(BP-RP) Rad  Lum  '.split()

    clu_df = pd.read_csv(clu_path,
                         sep='\s+',
                         skiprows=1,
                         names=clu_headers)
    
    clu_bin_path = os.getcwd() + '/binaries/' + cluster_name + '_binaries.txt'
    
    clu_bin_df = pd.read_csv(clu_path,
                             sep='\s+',
                             names=clu_headers).drop_duplicates()
    
    return clu_df, clu_bin_df

# Takes plain df, adds radial distance column to it
def calculate_dists(clu_df, centerRA, centerDE):
    clu_df['del_RA'] = (clu_df['sentRA'] - centerRA) * np.cos((clu_df['sentDE']+centerDE)/2)
    clu_df['del_DE'] = clu_df['sentDE'] - centerDE
    clu_df['Rad_Dist'] = 60 * np.sqrt(clu_df['del_RA']**2 + clu_df['del_DE']**2)
    return clu_df
    
def get_singles(clu_df, clu_bin_df):
    clu_bin_df['Source'] = clu_bin_df['Source'].astype(str).astype(int)
    clu_df = pd.merge(clu_df, clu_bin_df, how = 'outer', on = ['Source'], indicator=True)
    print(clu_df)

for cluster_name, subdata in data.items():
    centerRA = float(subdata['centerRA'])
    centerDE = float(subdata['centerDE'])
    clu_df, clu_bin_df = load_data(cluster_name)
    clu_df = calculate_dists(clu_df, centerRA, centerDE)
    get_singles(clu_df, clu_bin_df)
    
