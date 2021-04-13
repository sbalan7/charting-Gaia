from utils import load_data, find_mass_fn
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
import sys
import os


with open('select.json') as f:
    data = json.load(f)

lgmag, hgmag = 10, 18

for cluster_name, subdata in data.items():
    iso_df, clu_df = load_data(cluster_name)
    poly, main_seq = find_mass_fn(iso_df)
    data[cluster_name]["mass_fn"] = list(poly)
    
    int_poly = np.polyint(poly)
    avg_mass = ((int_poly(hgmag) - int_poly(lgmag)) / (hgmag - lgmag))
    
    xs = np.linspace(lgmag, hgmag, 100)
    ys = poly(xs)

    plt.scatter(main_seq['Gmag'], main_seq['Mass'], label="Actual Data")
    plt.plot(xs, ys, label=f'${poly[0]:.3f}+{poly[1]:.3f}x+{poly[2]:.3f}x^2+{poly[3]:.3f}x^3$')

    plt.title(f'{cluster_name}\'s Mass v Gmag Function \nAverage Mass = {avg_mass}')
    plt.xlabel('Gmag')
    plt.ylabel('Mass')
    plt.legend()
    plt.show()

with open('select.json', 'w') as f:
    json.dump(data, f, indent=4)

