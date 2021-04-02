# charting-Gaia

Using Gaia data to make some plots for open clusters. Star cluster plots are scraped from the VizieR database with Selenium, as implemented in `trawl_vizier.py`. These images undergo some basic transforms for better understanding in the `fix_images.py` file. The 1229 cluster plots are now analysed and here we select 10 plots for further analysis. These clusters selected are IC 4651, IC 4756, NGC 752, NGC 1664, NGC 2281, NGC 2287, NGC 2527, NGC 6281, NGC 6405, NGC 6475. The data related to these clusters are taken from the WEBDA database and added to the `select.json` file. The star data is downloaded into csv files by the `get_multiple_clusters.py` file. Here, plots of the raw data are also made. These plots will be used for analysing the data and making inferences. The `generate_radec.py` file lists out celestial coordinates for all star targets in the data and saves them in a file.

The data from WEBDA is then also used to download parsec isochrones from the CMD database. The website is trawled with Selenium again as in `download_isochrones.py`. Further processing of this isochrone data is done in `read_isochrones.py`. It generated a fitted isochrone with the cluster plot. Also in `read_isochrones.py` is the method to separate the single and binary track. Passing the argument `show` with the file highlights individual points in the plot. Otherwise the file defaults to saving a new copy of the isochrone tracks. Passing any additional argument allows for overwriting the file where the binary track is saved. This will be triggered only if `show` is passed before. 

`center_clusters.py` uses the mean shift algorithm as implemented by `scikit-learn` and determines the centers of the clusters. Then the `astropy` module is used to compute the radial distance between the targets and the cluster center. The radial distribution plot for the single and binary track is also generated by this file.

The `/report/` directory has the tex files and bib files used to generate the project report where a more detailed overview of the project is given. The BibTeX distribution is used for LaTeX.

### Dependencies for the code:
* python 3.8.5
* astropy 4.2
* matplotlib 3.3.3
* numpy 1.19.4
* pandas 1.2.1
* scikit-learn 0.24.0
* mplcursors 0.4

