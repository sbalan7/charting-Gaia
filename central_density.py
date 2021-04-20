from utils import find_mass_fn, plot_cmd, load_data
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
import os


with open('select.json') as f:
    data = json.load(f)

for cluster_name, subdata in data.items():
    if subdata['cluster_r'] == 0:
        continue
    
    path = os.getcwd() + '/clusters/' + cluster_name.replace(' ', '_') + '.csv'
    clu_df = pd.read_csv(path)
    
    clu_df = clu_df[clu_df['Rad_Dist']<subdata['cluster_r']]
    poly = np.poly1d(subdata["mass_fn"])
    clu_df["Mass"] = poly(clu_df['Gmag'])
    avg_mass = clu_df["Mass"].mean()
    
    d = int(subdata['distance'])
    iso_df, _ = load_data(cluster_name)
    ag, bprp = subdata['AG'], subdata['E_BP-RP']
    tup = (ag, float(subdata['g_corr']), bprp, float(subdata['b_corr']), float(subdata['diff_corr']))

    (fig, ax), sc, (p1, p2), cleaned_clu = plot_cmd(cluster_name, tup, d, clu_df, iso_df)
    ax.set_title(f'Star Distribution in {cluster_name} \nAge {data[cluster_name]["isochrone"]}, '
                   f'Metallicity {data[cluster_name]["metallicity"]}, Avg Mass {avg_mass}')
    plt.show()

    red_clu_df = clu_df[clu_df['Rad_Dist']<subdata['central_r']]
    (fig, ax), sc, (p1, p2), cleaned_clu = plot_cmd(cluster_name, tup, d, red_clu_df, iso_df)
    central_mass = red_clu_df['Mass'].sum()
    
    parsec_rad = (subdata['central_r']/60)*(np.pi/180)*d
    central_vol = (4/3) * np.pi * (parsec_rad ** 3)
    central_density = central_mass / central_vol
    ax.set_title(f'Central Distribution of {cluster_name} \nTotal Mass {central_mass}, '
                 f'Central Density {central_density}')
    print(f'{cluster_name} - {len(red_clu_df)}/{len(clu_df)} stars in core, Mass {central_mass} Density {central_density}')
    plt.show()




