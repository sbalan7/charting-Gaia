from selenium import webdriver
import matplotlib.pyplot as plt
import time
import csv
import os


VizieR_ROOT = 'https://vizier.u-strasbg.fr/viz-bin/'
OPTIONS = 'VizieR-6?-out.form=%2bH&-source=J/A%2bA/618/A93&Cluster='

def get_cluster_list():
    with open('select.txt', 'r') as f:
        clusters = f.read().splitlines()
        
    return clusters

def collect_data(targetcluster, driver, threshold=0.3):
    # Open VizieR website
    driver.get(VizieR_ROOT+OPTIONS+targetcluster)

    headers = ['SlNo', 'RA_ICRS', 'DE_ICRS', 'Source', 'GLON', 'GLAT', 'plx', 'pmRA', 'pmDE', 'o_', 'GMag', 'BP-RP', 'PMemb', 
                'Cluster', 'SimbadName', '_RA.icrs', '_DE.icrs']

    driver.find_element_by_xpath("//select[@name='-out.max']/option[text()='unlimited']").click()
    element = driver.find_element_by_xpath("/html/body/div[4]/div/form/div[1]/div/div/div[2]/div[2]/div/table/tbody/tr/td/input").click()

    time.sleep(7)

    table = driver.find_element_by_css_selector("#c36180093members_2")
    
    with open(os.getcwd()+'/clusters/'+targetcluster+'.csv', 'a') as f:
        cl_writer = csv.writer(f, delimiter=',')
        cl_writer.writerow(headers)
        for row in table.find_elements_by_css_selector('tr'):
            row_el = []
            for d in row.find_elements_by_css_selector('td'):
                row_el.append(d.text)
            cl_writer.writerow(row_el)
    

def plot(bprp, gmag, prob, prog, cluster):
    fig = plt.figure(figsize=(14, 8))
    s = plt.scatter(bprp, gmag, color='red', marker='.', label='All stars')
    s = plt.scatter(prob, prog, color='blue', marker='o', label='Probable member')
    ax = s.axes
    ax.invert_yaxis()
    ax.set_xlabel(r'$BP-RP$', fontsize=12)
    ax.set_ylabel(r'$G_{mag}$', fontsize=12)
    ax.set_title(f'Star Distribution in {cluster}')
    ax.grid(True)
    fig.tight_layout()
    plt.legend()
    plt.savefig(os.getcwd()+'/plots/'+cluster+'.png')
    plt.close(fig)

def open_VizieR():
    driver = webdriver.Firefox()
    clusters = get_cluster_list()

    for cluster in clusters:
        print(f'Collecting data for {cluster}')
        tic = time.time()
        target = cluster.replace(' ', '_')
        collect_data(target, driver)
        toc = time.time()
        print(f'Completed in {toc-tic} sec(s)')

    driver.quit()

def main():
    open_VizieR()    

if __name__ == '__main__':
    main()