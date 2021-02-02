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
    
    clu_path = os.getcwd() + '/cluster_tsvs/' + cluster_name.replace(' ', '_') + '.tsv'
    clu_headers = 'sentRA  sentDE   _r   _RAJ2000h _RAJ2000m _RAJ2000s   _DEJ2000h _DEJ2000m _DEJ2000s    RA_ICRS   e_RA   DE_ICRS  e_DE  Source   Plx    e_Plx   pmRA   e_pmRA   pmDE   e_pmDE   Dup   FG  e_FG    Gmag     e_Gmag FBP    e_FBP  BPmag   e_BPmag    FRP   e_FRP   RPmag     e_RPmag  BP-RP   RV   e_RV  Teff   AG   E(BP-RP) Rad  Lum  '.split()

    clu_df = pd.read_csv(clu_path,
                         sep='\s+',
                         skiprows=1,
                         names=clu_headers)
    
    return iso_df, clu_df

def plot_isochrone(iso_df, clu_df, x_tup, y_tup, d, diff_corr, cluster_name):

    def update_annot(ind):
        pos = sc.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        text = "it works"
        annot.set_text(text)
        annot.get_bbox_patch().set_facecolor('white')
        annot.get_bbox_patch().set_alpha(0.4)

    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = sc.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

    AG, g_corr = y_tup
    BPRP, b_corr = x_tup

    Gmag = iso_df['Gmag']
    G_BPmag = iso_df['G_BPmag']
    G_RPmag = iso_df['G_RPmag']
    
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
    
    final_path = os.getcwd() + '/plots/tracks/' + cluster_name + '.png'
    
    # Plot stars and isochrones
    fig, ax = plt.subplots(figsize=(12, 8))
    sc = plt.scatter(star_bprp, star_gmag, color='red', marker='.')
    p = plt.plot(bprp, gmag, color='black', linewidth=1, label='Isochrone')
    p = plt.plot(bprp, gmag_binary, color='blue', linewidth=1, label='Binary Track')

    annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    plt.xlim(x_wid)
    plt.ylim(y_wid)

    ax_ = sc.axes
    ax_.invert_yaxis()
    ax_.set_xlabel(r'$BP-RP$', fontsize=12)
    ax_.set_ylabel(r'$G_{mag}$', fontsize=12)
    ax_.set_title(f'Star Distribution in {cluster_name}')
    ax_.grid(True)
    plt.legend()
    fig.canvas.mpl_connect("motion_notify_event", hover)
    plt.show()
    #plt.savefig(final_path)

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
    d = int(subdata['distance'])
    isochrone = subdata['isochrone']
    iso_df, clu_df = load_data(isochrone, cluster_name)
    ag, bprp = find_ag_e_bprp(clu_df, cluster_name)
    x_tup = (bprp, float(subdata['b_corr']))
    y_tup = (ag, float(subdata['g_corr']))
    diff_corr = float(subdata['diff_corr'])
    plot_isochrone(iso_df, clu_df, x_tup, y_tup, d, diff_corr, cluster_name)
