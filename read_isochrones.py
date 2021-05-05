from utils import load_data, plot_cmd
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

def plot_isochrone(iso_df, clu_df, tup, d, cluster_name, say_what='save', w=False):
    def text(sel, w):
        row = cleaned_clu[(cleaned_clu['Gmag'] == sel.target[1]) & (cleaned_clu['BP-RP'] == sel.target[0])]
        if w:
            f.write(row['Source'].astype(int))
            f.write('\n')
        try:
            t = f"Source: {int(row['Source'])}\nRA: {float(row['sentRA'])}\nDE: {float(row['sentDE'])}"
        except TypeError:
            t = f"Source: nan\nRA: nan\nDE: nan"
        print(t)
        print(row.to_string(header=False, index=False))
        return t
    (fig, ax), sc, (p1, p2), cleaned_clu = plot_cmd(cluster_name, tup, d, clu_df, iso_df)
    ax.set_title(f'Star Distribution in {cluster_name} \nAge {data[cluster_name]["isochrone"]}, Metallicity {data[cluster_name]["metallicity"]}')

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
    ag, bprp = subdata['AG'], subdata['E_BP-RP']
    tup = (ag, float(subdata['g_corr']), bprp, float(subdata['b_corr']), float(subdata['diff_corr']))
    
    if len(sys.argv) > 2:
        plot_isochrone(iso_df, clu_df, tup, d, cluster_name, sys.argv[1], w)
    elif len(sys.argv) > 1:
        plot_isochrone(iso_df, clu_df, tup, d, cluster_name, sys.argv[1])
    else:
        plot_isochrone(iso_df, clu_df, tup, d, cluster_name)
    
    if len(sys.argv) > 2:        
        f.close()

with open('select.json', 'w') as f:
    json.dump(data, f, indent=4)
