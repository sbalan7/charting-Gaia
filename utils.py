import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def load_data(cluster_name, iso=True):
    clu_path = os.getcwd() + '/cluster_tsvs/' + cluster_name.replace(' ', '_') + '.tsv'
    clu_headers = 'sentRA  sentDE   _r   _RAJ2000h _RAJ2000m _RAJ2000s   _DEJ2000h _DEJ2000m _DEJ2000s    RA_ICRS   e_RA   DE_ICRS  e_DE  Source   Plx    e_Plx   pmRA   e_pmRA   pmDE   e_pmDE   Dup   FG  e_FG    Gmag     e_Gmag FBP    e_FBP  BPmag   e_BPmag    FRP   e_FRP   RPmag     e_RPmag  BP-RP   RV   e_RV  Teff   AG   E(BP-RP) Rad  Lum  '.split()

    clu_df = pd.read_csv(clu_path,
                         sep='\s+',
                         skiprows=1,
                         names=clu_headers)
    if iso:
        iso_path = os.getcwd() + '/isochrones/' + cluster_name.replace(' ', '_') + '.dat'
        iso_headers = 'Zini     MH   logAge Mini        int_IMF         Mass   logL    logTe  logg  label   McoreTP C_O  period0  period1  period2  period3  period4  pmode  Mloss  tau1m   X   Y   Xc  Xn  Xo  Cexcess  Z 	 mbolmag  Gmag    G_BPmag  G_RPmag'.split()
        
        iso_df = pd.read_csv(iso_path,
                            sep='\s+',
                            skiprows=13,
                            header=0,
                            names=iso_headers)
        iso_df.drop(iso_df.tail(1).index, inplace=True)    
        return iso_df, clu_df
        
    else:
        return clu_df

def find_mass_fn(iso_df):
    iso_df = iso_df[(iso_df['Gmag']<20)&(iso_df['Gmag']>10)]
    mass, gmag = iso_df['Mass'], iso_df['Gmag']
    p = np.polyfit(gmag, mass, 3)
    return np.poly1d(p), iso_df

def plot_cmd(cluster_name, tup, d, clu_df, iso_df=None):
    AG, g_corr, BPRP, b_corr, diff_corr = tup
    print(cluster_name)
    if iso_df is not None:
        # Remove outliers in isochrone data
        cleaned_iso = iso_df.loc[(iso_df['Gmag'] > -5) & (iso_df['Gmag'] < 20)]
        Gmag = cleaned_iso['Gmag']
        G_BPmag = cleaned_iso['G_BPmag']
        G_RPmag = cleaned_iso['G_RPmag']
        
        # Magnitude calculation
        gmag = Gmag + (5 * np.log10(d)) - 5 + AG + g_corr
        bprp = G_BPmag - G_RPmag + BPRP + b_corr

        gmag_binary = gmag - diff_corr
    
    # Some missing sources in the data cause outliers, and are removed
    cleaned_clu = clu_df[(clu_df['Gmag'] < 90) & (clu_df['BP-RP'] < 90)]
    star_gmag = cleaned_clu['Gmag']
    star_bprp = cleaned_clu['BP-RP']
    
    x_wid = [np.mean(star_bprp.nsmallest(5))-0.5, np.mean(star_bprp.nlargest(5))+0.5]
    y_wid = [np.mean(star_gmag.nsmallest(5))-0.5, np.mean(star_gmag.nlargest(5))+0.5]

    # Plot stars and isochrones
    fig, ax = plt.subplots(figsize=(12, 8))
    sc = plt.scatter(star_bprp, star_gmag, color='red', marker='.', alpha=0.6)
    if iso_df is not None:
        p1 = plt.plot(bprp, gmag, color='black', linewidth=1, label='Isochrone')
        p2 = plt.plot(bprp, gmag_binary, color='blue', linewidth=1, label='Binary Track')
    
    plt.xlim(x_wid)
    plt.ylim(y_wid)

    ax_ = sc.axes
    ax_.invert_yaxis()
    ax_.set_xlabel(r'$BP-RP$', fontsize=12)
    ax_.set_ylabel(r'$G_{mag}$', fontsize=12)
    ax_.grid(True)
    plt.legend()

    if iso_df is not None:
        return (fig, ax), sc, (p1, p2), cleaned_clu
    else:
        return (fig, ax), sc, cleaned_clu
    


