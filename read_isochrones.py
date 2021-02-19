import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import mplcursors
import json
import sys
import os

with open('select.json') as f:
    data = json.load(f)

pd.set_option('display.max_columns', None)

# Load the isochrone and cluster data downloaded
def load_data(cluster_name):
    iso_path = os.getcwd() + '/isochrones/' + cluster_name.replace(' ', '_') + '.dat'
    iso_headers = 'Zini     MH   logAge Mini        int_IMF         Mass   logL    logTe  logg  label   McoreTP C_O  period0  period1  period2  period3  period4  pmode  Mloss  tau1m   X   Y   Xc  Xn  Xo  Cexcess  Z 	 mbolmag  Gmag    G_BPmag  G_RPmag'.split()
    
    iso_df = pd.read_csv(iso_path,
                         sep='\s+',
                         skiprows=13,
                         header=0,
                         names=iso_headers)
    iso_df.drop(iso_df.tail(1).index, inplace=True)
    
    clu_path = os.getcwd() + '/cluster_tsvs/' + cluster_name.replace(' ', '_') + '.tsv'
    clu_headers = 'sentRA  sentDE   _r   _RAJ2000h _RAJ2000m _RAJ2000s   _DEJ2000h _DEJ2000m _DEJ2000s    RA_ICRS   e_RA   DE_ICRS  e_DE  Source   Plx    e_Plx   pmRA   e_pmRA   pmDE   e_pmDE   Dup   FG  e_FG    Gmag     e_Gmag FBP    e_FBP  BPmag   e_BPmag    FRP   e_FRP   RPmag     e_RPmag  BP-RP   RV   e_RV  Teff   AG   E(BP-RP) Rad  Lum  '.split()

    clu_df = pd.read_csv(clu_path,
                         sep='\s+',
                         skiprows=1,
                         names=clu_headers)
    
    return iso_df, clu_df

def plot_isochrone(iso_df, clu_df, tup, d, cluster_name, say_what='save', w=False):
    def text(sel, w):
        row = cleaned_clu[(cleaned_clu['Gmag'] == sel.target[1]) & (cleaned_clu['BP-RP'] == sel.target[0])]
        row['Source'] = row['Source'].astype(int)
        if w:
            f.write(row.to_string(header=False, index=False))
            f.write('\n')
        try:
            t = f"Source: {int(row['Source'])}\nRA: {float(row['sentRA'])}\nDE: {float(row['sentDE'])}"
        except TypeError:
            t = f"Source: nan\nRA: nan\nDE: nan"
        print(t)
        print(row.to_string(header=False, index=False))
        return t
    
    AG, g_corr, BPRP, b_corr, diff_corr = tup
    
    # Remove outliers in isochrone data
    cleaned_iso = iso_df.loc[(iso_df['Gmag'] > -5) & (iso_df['Gmag'] < 20)]
    Gmag = cleaned_iso['Gmag']
    G_BPmag = cleaned_iso['G_BPmag']
    G_RPmag = cleaned_iso['G_RPmag']
    
    # Magnitude calculation
    gmag = Gmag + (5 * np.log10(d)) - 5 + AG + g_corr
    bprp = G_BPmag - G_RPmag + BPRP + b_corr
    
    # Some missing sources in the data cause outliers, and are removed
    cleaned_clu = clu_df[(clu_df['Gmag'] < 90) & (clu_df['BP-RP'] < 90)]
    star_gmag = cleaned_clu['Gmag']
    star_bprp = cleaned_clu['BP-RP']
    
    x_wid = [np.mean(star_bprp.nsmallest(5))-0.5, np.mean(star_bprp.nlargest(5))+0.5]
    y_wid = [np.mean(star_gmag.nsmallest(5))-0.5, np.mean(star_gmag.nlargest(5))+0.5]

    gmag_binary = gmag - diff_corr

    # Plot stars and isochrones
    fig, ax = plt.subplots(figsize=(12, 8))
    sc = plt.scatter(star_bprp, star_gmag, color='red', marker='.', alpha=0.6)
    p = plt.plot(bprp, gmag, color='black', linewidth=1, label='Isochrone')
    p = plt.plot(bprp, gmag_binary, color='blue', linewidth=1, label='Binary Track')
    
    plt.xlim(x_wid)
    plt.ylim(y_wid)

    ax_ = sc.axes
    ax_.invert_yaxis()
    ax_.set_xlabel(r'$BP-RP$', fontsize=12)
    ax_.set_ylabel(r'$G_{mag}$', fontsize=12)
    ax_.set_title(f'Star Distribution in {cluster_name}')
    ax_.grid(True)
    plt.legend()

    if say_what == 'show':
        crs = mplcursors.cursor(ax,hover=True)
        @crs.connect("add")
        def _(sel):
            sel.annotation.get_bbox_patch().set(fc="white", alpha=1)
        crs.connect("add", lambda sel: sel.annotation.set_text(
            '{}'.format(text(sel, w))))
        plt.show()
    elif say_what == 'save':
        final_path = os.getcwd() + '/plots/tracks/' + cluster_name + '.png'
        plt.savefig(final_path)


# Findging the mean and median value of AG and E(BP-RP)
def find_ag_e_bprp(clu_df, cluster_name, show_plot='n'):
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


for cluster_name, subdata in data.items():
    if len(sys.argv) > 2:
        binary_path = os.getcwd() + '/binaries/' + cluster_name+'_binaries.txt'
        f = open(binary_path, 'w')
        w = True
    d = int(subdata['distance'])
    iso_df, clu_df = load_data(cluster_name)
    ag, bprp = find_ag_e_bprp(clu_df, cluster_name)
    tup = (ag, float(subdata['g_corr']), bprp, float(subdata['b_corr']), float(subdata['diff_corr']))
    if len(sys.argv) > 2:
        plot_isochrone(iso_df, clu_df, tup, d, cluster_name, sys.argv[1], w)
    elif len(sys.argv) > 1:
        plot_isochrone(iso_df, clu_df, tup, d, cluster_name, sys.argv[1])
    else:
        plot_isochrone(iso_df, clu_df, tup, d, cluster_name)
    if len(sys.argv) > 2:        
        f.close()