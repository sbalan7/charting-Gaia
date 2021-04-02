import pandas as pd
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