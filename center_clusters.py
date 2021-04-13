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

pd.set_option('display.max_columns', None)

def load_data(cluster_name):
    clu_path = os.getcwd() + '/cluster_tsvs/' + cluster_name.replace(' ', '_') + '.tsv'
    clu_headers = 'sentRA  sentDE   _r   _RAJ2000h _RAJ2000m _RAJ2000s   _DEJ2000h _DEJ2000m _DEJ2000s    RA_ICRS   e_RA   DE_ICRS  e_DE  Source   Plx    e_Plx   pmRA   e_pmRA   pmDE   e_pmDE   Dup   FG  e_FG    Gmag     e_Gmag FBP    e_FBP  BPmag   e_BPmag    FRP   e_FRP   RPmag     e_RPmag  BP-RP   RV   e_RV  Teff   AG   E(BP-RP) Rad  Lum  '.split()

    clu_df = pd.read_csv(clu_path,
                         sep='\s+',
                         skiprows=1,
                         names=clu_headers)
    
    clu_bin_path = os.getcwd() + '/binaries/' + cluster_name + '_binaries.txt'
    
    clu_bin_df = pd.read_csv(clu_bin_path,
                             sep='\s+',
                             names=clu_headers).drop_duplicates()
    
    return clu_df, clu_bin_df
    
def center_cluster(clu_df):
    X = clu_df[['sentRA', 'sentDE']]

    ms = MeanShift(bandwidth=10)
    ms.fit(X)
    cluster_centers = ms.cluster_centers_

    return cluster_centers[0][0], cluster_centers[0][1]

def dist_row(ra, dec, center):
    c = SkyCoord(ra=ra*u.degree, dec=dec*u.degree, frame='icrs')
    return center.separation(c).arcminute

def calculate_dists(center, clu_df):
    clu_df['Rad_Dist'] = dist_row(clu_df['sentRA'], clu_df['sentDE'], center)
    return clu_df

def get_singles(clu_df, clu_bin_df):
    clu_bin_df['Source'] = clu_bin_df['Source'].astype(str).astype(int)
    clu_df['Source'] = clu_df['Source'].astype(int)
    clu_df = pd.merge(clu_df, clu_bin_df['Source'], how = 'outer', on = ['Source'], indicator=True)
    d={"left_only":"Single", "right_only":"WUT", "both":"Binary"}
    clu_df['Type'] = clu_df['_merge'].map(d)
    clu_df = clu_df.drop(['_merge'], axis=1)
    return clu_df

def find_area(s_x, s_y, b_x, b_y):
    diff_s_x = [b-a for a, b in zip(s_x, s_x[1:])]
    diff_b_x = [b-a for a, b in zip(b_x, b_x[1:])]
    s_y, b_y = s_y[:-1], b_y[:-1]
    
    area_s = np.sum(np.multiply(diff_s_x, s_y))
    area_b = np.sum(np.multiply(diff_b_x, b_y))
    
    return area_b - area_s


def plot_radial_dist(clu_df):
    rad_path = os.getcwd() + '/plots/radial_dist/' + cluster_name + '_rad.png'
    bin_df = clu_df[clu_df['Type'] == 'Binary'].sort_values('Rad_Dist')
    sin_df = clu_df[clu_df['Type'] == 'Single'].sort_values('Rad_Dist')

    b_x = bin_df['Rad_Dist']
    b_min, b_max = b_x.min(), b_x.max()
    
    s_x = sin_df[(sin_df['Rad_Dist']<=b_max)&(sin_df['Rad_Dist']>=b_min)]['Rad_Dist']
    the_m = s_x.max() if s_x.max()>b_max else b_max

    b_y = np.arange(b_x.size)/b_x.size
    s_y = np.arange(s_x.size)/s_x.size

    s_x = s_x.append(pd.Series(the_m))
    b_x = b_x.append(pd.Series(the_m))
    
    s_y = np.append(s_y, 1.0)
    b_y = np.append(b_y, 1.0)

    area = find_area(s_x, s_y, b_x, b_y)

    plt.step(s_x, s_y, label='Single Stars')
    plt.step(b_x, b_y, label='Binary Stars')
    
    plt.title(f'Radial Dist for {cluster_name}\nArea = {area:.4f}')
    plt.xlabel('Radial Distance (arcmin)')
    plt.ylabel('% of stars')
    plt.legend()
    plt.savefig(rad_path)
    plt.clf()


for cluster_name, subdata in data.items():
    clu_df, clu_bin_df = load_data(cluster_name)
    x, y = center_cluster(clu_df)
    data[cluster_name]['centerRA'], data[cluster_name]['centerDE'] = x, y
    center = SkyCoord(ra=x*u.degree, dec=y*u.degree, frame='icrs')
    clu_df = calculate_dists(center, clu_df)
    clu_df = get_singles(clu_df, clu_bin_df)
    plot_radial_dist(clu_df)
    path = os.getcwd() + '/clusters/' + cluster_name.replace(' ', '_') + '.csv'
    clu_df.to_csv(path)

with open('select.json', 'w') as f:
    json.dump(data, f, indent=4)
