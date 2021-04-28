from numpy.polynomial.polynomial import polyfit
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import mplcursors
import os


path = os.getcwd() + '/result.csv'
results = pd.read_csv(path, sep='\s+')

x, y = results['Area'].astype(float), results['N_relax'].astype(float)
text = results['Cluster_Name']
b, m = polyfit(x, y, 1)

fig, ax = plt.subplots(figsize=(14, 8))

rline = ax.plot(x, b+m*x, 'b-')
splot = ax.scatter(x, y, c='r')

crs = mplcursors.cursor(splot, multiple=True)
@crs.connect("add")
def _(sel):
    sel.annotation.get_bbox_patch().set(fc="white")
    sel.annotation.arrow_patch.set(arrowstyle=None, fc="white", alpha=.5)
crs.connect(
    "add", lambda sel: sel.annotation.set_text(
          text[sel.target.index].replace('_', ' ')
))


plt.xlabel('Area between tracks')
plt.ylabel('N_relax')
plt.show()
