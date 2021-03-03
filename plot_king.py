import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
import os
'''
with open('select.json') as f:
    data = json.load(f)

pd.set_option('display.max_columns', None)
'''
def load_data(cluster_name):
    clu_path = os.getcwd() + '/clusters/' + cluster_name.replace(' ', '_') + '.csv'
    clu_headers = ['Index','sentRA','sentDE','_r','_RAJ2000h','_RAJ2000m','_RAJ2000s','_DEJ2000h','_DEJ2000m','_DEJ2000s','RA_ICRS','e_RA','DE_ICRS','e_DE','Source','Plx','e_Plx','pmRA','e_pmRA','pmDE','e_pmDE','Dup','FG','e_FG','Gmag','e_Gmag','FBP','e_FBP','BPmag','e_BPmag','FRP','e_FRP','RPmag','e_RPmag','BP-RP','RV','e_RV','Teff','AG','E(BP-RP)','Rad','Lum','del_RA','del_DE','Rad_Dist','Type']

    clu_df = pd.read_csv(clu_path,
                         skiprows=1,
                         names=clu_headers)
    
    return clu_df

def bin_stars(bins, cluster_name):
    clu_df = load_data(cluster_name)
    
    _ = [np.sqrt(i+1) for i in range(bins)]
    base_r = max(clu_df['Rad_Dist']) / np.sum(_)

    counts = []
    cu_counts = []

    for i in range(bins): 
        curr_r = np.sqrt(i+1) * base_r
        cu_counts.append(np.sum(clu_df['Rad_Dist']<curr_r))

    for i in range(len(cu_counts)):
        if i > 0:
            counts.append(cu_counts[i] - cu_counts[i-1])
        elif i == 0:
            counts.append(cu_counts[i])
    
    return counts, base_r

def plot_kings_profile(counts, base_r):
    bins = len(counts)
    print(counts)
    radii = [np.sqrt(i+1)*base_r for i in range(bins)]
    log_radii = np.log10(radii)
    
    log_surf_d = np.log10(counts)-2*log_radii
    log_surf_d = [_-np.log10(np.pi) for _ in log_surf_d]
    plt.plot(log_surf_d, log_radii, marker='.')
    plt.show()

cluster_name = 'NGC_2287'
counts, base_r = bin_stars(25, cluster_name)
plot_kings_profile(counts, base_r)

