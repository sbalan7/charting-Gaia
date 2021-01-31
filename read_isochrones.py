import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
import os

with open('select.json') as f:
    data = json.load(f)

pd.set_option('display.max_columns', None)

# Load the isochrone and cluster data downloaded
def load_data(isochrone, cluster_name):
    iso_path = os.getcwd() + '/isochrones/' + isochrone + '.dat'
    iso_headers = 'Zini     MH   logAge Mini        int_IMF         Mass   logL    logTe  logg  label   McoreTP C_O  period0  period1  period2  period3  period4  pmode  Mloss  tau1m   X   Y   Xc  Xn  Xo  Cexcess  Z 	 mbolmag  Gmag    G_BPmag  G_RPmag'.split()
    
    iso_df = pd.read_csv(iso_path,
                         sep='\s+',
                         skiprows=13,
                         header=0,
                         names=iso_headers)
    iso_df.drop(iso_df.tail(1).index, inplace=True)
    
    clu_path = os.getcwd() + '/cluster_tsvs/' + cluster_name + '.tsv'
    clu_headers = 'sentRA  sentDE   _r   _RAJ2000h _RAJ2000m _RAJ2000s   _DEJ2000h _DEJ2000m _DEJ2000s    RA_ICRS   e_RA   DE_ICRS  e_DE  Source   Plx    e_Plx   pmRA   e_pmRA   pmDE   e_pmDE   Dup   FG  e_FG    Gmag     e_Gmag FBP    e_FBP  BPmag   e_BPmag    FRP   e_FRP   RPmag     e_RPmag  BP-RP   RV   e_RV  Teff   AG   E(BP-RP) Rad  Lum  '.split()

    clu_df = pd.read_csv(clu_path,
                         sep='\s+',
                         skiprows=1,
                         names=clu_headers)
    
    return iso_df, clu_df

def plot_isochrone(iso_df, clu_df, ag, bprp, d):
    final_path = os.getcwd() + '/plots/' + cluster_name + '.png'
    Gmag = iso_df['Gmag']
    G_BPmag = iso_df['G_BPmag']
    G_RPmag = iso_df['G_RPmag']
    
    # Magnitude calculation
    gmag = Gmag + (5 * np.log10(d)) - 5 + ag + 0.1
    bprp = G_BPmag - G_RPmag + bprp + 0.05
    
    # Some missing sources in the data cause outliers, and are removed
    cleaned_clu = clu_df[(clu_df['Gmag'] < 90) & (clu_df['BP-RP'] < 90)]
    star_gmag = cleaned_clu['Gmag']
    star_bprp = cleaned_clu['BP-RP']

    gmag_binary = gmag - 0.752 
    # Plot stars and isochrones
    fig = plt.figure(figsize=(10, 6))
    s = plt.scatter(star_bprp, star_gmag, color='red', marker='.')
    p = plt.plot(bprp, gmag, color='black', linewidth=1, label='Isochrone')
    p = plt.plot(bprp, gmag_binary, color='blue', linewidth=1, label='Binary Track')
    plt.xlim([-1, 5])
    plt.ylim([-1, 20])

    ax = s.axes
    ax.invert_yaxis()
    ax.set_xlabel(r'$BP-RP$', fontsize=12)
    ax.set_ylabel(r'$G_{mag}$', fontsize=12)
    ax.set_title(f'Star Distribution in {cluster_name}')
    ax.grid(True)
    plt.label()
    plt.savefig(final_path)

# Findging the mean and median value of AG and E(BP-RP)
def find_ag_e_bprp(clu_df, show_plot='n'):
    ag = clu_df[clu_df['AG'] <= 90]
    ag = ag['AG']
    ag_mean = ag.mean()
    ag_median = ag.median()

    bprp = clu_df[clu_df['E(BP-RP)'] <= 90]
    bprp = bprp['E(BP-RP)']
    bprp_mean = bprp.mean()
    bprp_median = bprp.median()
    
    if show_plot != 'n':
        fig = plt.figure(figsize=(12, 4))
        fig.canvas.set_window_title('Plot')

        ax1 = fig.add_subplot(1,2,1)
        ax1.hist(ag)
        ax1.axvline(ag_mean, color='k', linestyle='dashed', linewidth=1)
        ax1.axvline(ag_median, color='k', linestyle='dashed', linewidth=1)
        ax1.title.set_text(f'Extinction Estimate (AG) for {cluster_name}\nMean: {ag_mean:.4f} Median: {ag_median}')

        ax2 = fig.add_subplot(1,2,2)
        ax2.hist(bprp)
        ax2.axvline(bprp_mean, color='k', linestyle='dashed', linewidth=1)
        ax2.axvline(bprp_median, color='k', linestyle='dashed', linewidth=1)
        ax2.title.set_text(f'Redenning Estimate E(BP-RP) for {cluster_name}\nMean: {bprp_mean:.4f} Median: {bprp_median}')

        plt.show()
        
    return ag_median, bprp_median

cluster_name = 'NGC_6405'
isochrone = '0.1gy'

for cluster_name, subdata in data.items():
    d = int(subdata['distance'])
    isochrone = subdata['isochrone']
    iso_df, clu_df = load_data(isochrone, cluster_name)
    ag, bprp = find_ag_e_bprp(clu_df)
    plot_isochrone(iso_df, clu_df, ag, bprp, d)
