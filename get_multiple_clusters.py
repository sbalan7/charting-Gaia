from selenium import webdriver
import matplotlib.pyplot as plt
import time
import os


VizieR_ROOT = 'https://vizier.u-strasbg.fr/viz-bin/'
OPTIONS = 'VizieR-6?-out.form=%2bH&-source=J/A%2bA/618/A93&Cluster='

def get_cluster_list():
    with open('select.txt', 'r') as f:
        clusters = f.read().splitlines()
        
    return clusters

def collect_data(targetcluster, threshold=0.3):
    # Open VizieR website
    driver = webdriver.Firefox()
    driver.get(VizieR_ROOT+OPTIONS+targetcluster)

    driver.find_element_by_xpath("//select[@name='-out.max']/option[text()='unlimited']").click()
    element = driver.find_element_by_xpath("/html/body/div[4]/div/form/div[1]/div/div/div[2]/div[2]/div/table/tbody/tr/td/input").click()

    time.sleep(7)

    table = driver.find_element_by_css_selector("#c36180093members_2")

    gmag = []
    bprp = []
    ug = []
    ub = []

    for row in table.find_elements_by_css_selector('tr'):
        x = 0
        for d in row.find_elements_by_css_selector('td'):
            x += 1
            if (x == 11):
                if len(d.text) <= 1:
                    continue
                gmag.append(float(d.text))
            if (x == 12):
                if len(d.text) <= 1:
                    gmag.pop()
                    continue
                bprp.append(float(d.text))
            if (x == 13):
                if float(d.text) > threshold:
                    ub.append(bprp[-1])
                    ug.append(gmag[-1])
    
    driver.quit()
    
    if len(bprp) <= 10:
        print('Cluster not found')

    return bprp, gmag, ub, ug

def plot(bprp, gmag, ub, ug, cluster):
    fig = plt.figure(figsize=(10, 6))
    s = plt.scatter(ub, ug, color='blue', marker='o')
    s = plt.scatter(bprp, gmag, color='red', marker='.')
    ax = s.axes
    ax.invert_yaxis()
    ax.set_xlabel(r'$BP-RP$', fontsize=12)
    ax.set_ylabel(r'$G_{mag}$', fontsize=12)
    ax.set_title(f'Star Distribution in {cluster}')
    ax.grid(True)
    fig.tight_layout()
    plt.savefig(os.getcwd()+'/plots/'+cluster+'.png')
    plt.close(fig)


clusters = get_cluster_list()

for cluster in clusters:
    print(f'Collecting data for {cluster}')
    tic = time.time()
    target = cluster.replace(' ', '_')
    b, g, ub, ug = collect_data(target)
    plot(b, g, ub, ug, cluster)
    toc = time.time()
    print(f'Completed in {toc-tic} sec(s)')
