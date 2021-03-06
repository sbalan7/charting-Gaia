from astropy.coordinates import SkyCoord
from sklearn.cluster import MeanShift
import matplotlib.pyplot as plt
import astropy.units as u
import pandas as pd
import numpy as np
import json
import os


with open('select.json', 'r') as f:
    data = json.load(f)

def load_data(cluster_name):
    clu_path = os.getcwd() + '/cluster_tsvs/' + cluster_name.replace(' ', '_') + '.tsv'
    clu_headers = 'sentRA  sentDE   _r   _RAJ2000h _RAJ2000m _RAJ2000s   _DEJ2000h _DEJ2000m _DEJ2000s    RA_ICRS   e_RA   DE_ICRS  e_DE  Source   Plx    e_Plx   pmRA   e_pmRA   pmDE   e_pmDE   Dup   FG  e_FG    Gmag     e_Gmag FBP    e_FBP  BPmag   e_BPmag    FRP   e_FRP   RPmag     e_RPmag  BP-RP   RV   e_RV  Teff   AG   E(BP-RP) Rad  Lum  '.split()

    clu_df = pd.read_csv(clu_path,
                         sep='\s+',
                         skiprows=1,
                         names=clu_headers)
    
    return clu_df
    
def center_cluster(clu_df):
    X = clu_df[['sentRA', 'sentDE']]

    ms = MeanShift(bandwidth=10)
    ms.fit(X)
    cluster_centers = ms.cluster_centers_

    return cluster_centers[0][0], cluster_centers[0][1]

def dist_row(ra, dec, center):
    c = SkyCoord(ra=ra*u.degree, dec=dec*u.degree, frame='icrs')
    return center.separation(c).arcsecond

def calculate_dists(center, clu_df):
    clu_df['Rad_Dist'] = clu_df.apply(lambda row: dist_row(clu_df['sentRA'], clu_df['sentDE'], center), axis=1)
    return clu_df


for cluster_name, subdata in data.items():
    clu_df = load_data(cluster_name)
    x, y = center_cluster(clu_df)
    data[cluster_name]['centerRA'], data[cluster_name]['centerDE'] = x, y
    center = SkyCoord(ra=x*u.degree, dec=y*u.degree, frame='icrs')
    clu_df = calculate_dists(center, clu_df)
    path = os.getcwd() + '/clusters/' + cluster_name.replace(' ', '_') + '.csv'
    clu_df.to_csv(path)

with open('select.json', 'w') as f:
    json.dump(data, f)
