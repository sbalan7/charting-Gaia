import pandas as pd
import os


def gen_radec(cluster_name):
    clu_headers = 'SlNo,RA_ICRS,DE_ICRS,Source,GLON,GLAT,plx,pmRA,pmDE,o_,GMag,BP-RP,PMemb,Cluster,SimbadName,_RA.icrs,_DE.icrs'.split(',')
    temp = os.getcwd() + '/clusters/' + cluster_name + '.csv'
    clu_df = pd.read_csv(temp, 
                        skiprows=2,
                        names=clu_headers)
    radec = clu_df[['RA_ICRS', 'DE_ICRS']]
    out_path = os.getcwd() + '/radecs/' + 'radec_' + cluster_name + '.tsv'
    radec.to_csv(out_path, sep = '\t', index=False, header=False)


cluster_name = 'NGC_6405'
gen_radec(cluster_name)