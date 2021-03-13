from astropy.modeling.models import KingProjectedAnalytic1D
from astropy.modeling.fitting import LinearLSQFitter
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
    clu_headers = ['sentRA', 'sentDE', '_r', '_RAJ2000h', '_RAJ2000m', '_RAJ2000s', '_DEJ2000h', '_DEJ2000m', '_DEJ2000s', 'RA_ICRS', 'e_RA', 'DE_ICRS', 'e_DE', 'Source', 'Plx', 'e_Plx', 'pmRA', 'e_pmRA', 'pmDE', 'e_pmDE', 'Dup', 'FG', 'e_FG', 'Gmag', 'e_Gmag', 'FBP', 'e_FBP', 'BPmag', 'e_BPmag', 'FRP', 'e_FRP', 'RPmag', 'e_RPmag', 'BP-RP', 'RV', 'e_RV', 'Teff', 'AG', 'E(BP-RP)', 'Rad', 'Lum', 'Rad_Dist', 'Type']

    clu_df = pd.read_csv(clu_path,
                         skiprows=1,
                         names=clu_headers)
    
    return clu_df

def bin_stars(bins, cluster_name):
    clu_df = load_data(cluster_name)
    
    base_r = max(clu_df['Rad_Dist']) / np.sqrt(bins)
    
    counts = []
    cu_counts = []

    for i in range(bins): 
        curr_r = np.sqrt(i+1) * base_r
        print(curr_r)
        cu_counts.append(np.sum(clu_df['Rad_Dist']<curr_r))
    
    for i in range(len(cu_counts)):
        if i > 0:
            counts.append(cu_counts[i] - cu_counts[i-1])
        elif i == 0:
            counts.append(cu_counts[i])
    
    return counts, base_r

def plot_kings_profile(counts, base_r, cluster_name):
    bins = len(counts)
    print(counts)
    amplitude = counts[0]/(np.pi*base_r*base_r)
    r_c = 7.59
    fig = plt.figure()
    ax = plt.gca()

    for r_t in [85, 95, 105]:
        r = np.linspace(5e-3, r_t, 100)
        fit = LinearLSQFitter()
        kp = KingProjectedAnalytic1D()
        sig = kp(r)
        
        radii = np.array([np.sqrt(i+1)*base_r for i in range(bins)])
        surf_d = counts / (radii*radii*np.pi)
    
        ax.plot(r, sig/sig[0], label=str(r_t))
        ax.scatter(radii, surf_d, marker='.', color='#39ff14')
        
        ax.set_yscale('log')
        ax.set_xscale('log')
        ax.set_ylim([1e-5, 1e-1])
        ax.set_xlim([10, 400])
    
    plt.xlabel('log(radii)')
    plt.ylabel('log(surface density)')
    plt.legend()
    plt.title(f'{cluster_name}, $r_c = {r_c}$')
    plt.show()

cluster_name = 'NGC_752'
counts, base_r = bin_stars(25, cluster_name)
plot_kings_profile(counts, base_r, cluster_name)

