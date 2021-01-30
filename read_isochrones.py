import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

cluster_name = 'NGC_6405'
isochrone = '0.2gy'

pd.set_option('display.max_columns', None)

# Load the isochrone and cluster data downloaded
def load_data():
    iso_path = os.getcwd() + '/isochrones/' + isochrone + '.dat'
    iso_headers = 'Zini MH logAge Mini int_IMF Mass logL logTe logg label McoreTP C_O period0 period1 period2 period3 period4 pmode Mloss tau1m X Y Xc Xn Xo Cexcess Z mbolmag Gmag G_BPmag G_RPmag B_Tmag V_Tmag Jmag Hmag Ksmag'.split(' ')

    iso_df = pd.read_csv(iso_path,
                    sep='\s+',
                    skiprows=1,
                    names=iso_headers)
    iso_df.drop(iso_df.tail(1).index,inplace=True)

    clu_path = os.getcwd() + '/cluster_tsvs/' + cluster_name + '.tsv'
    clu_headers = 'sentRA  sentDE   _r   _RAJ2000h _RAJ2000m _RAJ2000s   _DEJ2000h _DEJ2000m _DEJ2000s    RA_ICRS   e_RA   DE_ICRS  e_DE  Source   Plx    e_Plx   pmRA   e_pmRA   pmDE   e_pmDE   Dup   FG  e_FG    Gmag     e_Gmag FBP    e_FBP  BPmag   e_BPmag    FRP   e_FRP   RPmag     e_RPmag  BP-RP   RV   e_RV  Teff   AG   E(BP-RP) Rad  Lum  '.split()

    clu_df = pd.read_csv(clu_path,
                    sep='\s+',
                    skiprows=1,
                    names=clu_headers)

    return iso_df, clu_df

# Take mean of parallax and inverted, common distance for magnitude calculation
def calc_dist(clu_df):
    plx = clu_df[clu_df['Plx'] <= 9]
    plx = clu_df['Plx']
    return 1/plx.mean()

def plot_isochrone(iso_df, clu_df, ag, bprp, d):
    Gmag = iso_df['Gmag']
    G_BPmag = iso_df['G_BPmag']
    G_RPmag = iso_df['G_RPmag']
    
    # Magnitude calculation
    gmag = Gmag + 5 * np.log(d) - 5 + ag
    bprp = G_BPmag - G_RPmag + bprp

    # Some missing sources in the data cause outliers, and are removed
    cleaned_clu = clu_df[(clu_df['Gmag'] < 90) & (clu_df['BP-RP'] < 90)]
    star_gmag = cleaned_clu['Gmag']
    star_bprp = cleaned_clu['BP-RP']

    # Plot stars and isochrones
    fig = plt.figure(figsize=(10, 6))
    s = plt.scatter(star_bprp, star_gmag, color='red', marker='.')
    p = plt.plot(bprp, gmag, color='black', linewidth=1)

    ax = s.axes
    ax.invert_yaxis()
    ax.set_xlabel(r'$BP-RP$', fontsize=12)
    ax.set_ylabel(r'$G_{mag}$', fontsize=12)
    ax.set_title(f'Star Distribution in {cluster_name}')
    ax.grid(True)
    plt.show()

# Findging the mean and median value of AG and E(BP-RP)
def find_ag_e_bprp(clu_df):
    ag = clu_df[clu_df['AG'] <= 90]
    ag = ag['AG']
    ag_mean = ag.mean()
    ag_median = ag.median()

    bprp = clu_df[clu_df['E(BP-RP)'] <= 90]
    bprp = bprp['E(BP-RP)']
    bprp_mean = bprp.mean()
    bprp_median = bprp.median()
    '''
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
    '''
    return ag_median, bprp_median

iso_df, clu_df = load_data()
d = calc_dist(clu_df)
ag, bprp = find_ag_e_bprp(clu_df)
plot_isochrone(iso_df, clu_df, ag, bprp, d)