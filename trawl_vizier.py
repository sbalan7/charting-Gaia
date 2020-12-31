from selenium import webdriver
import time


VizieR_ROOT = 'https://vizier.u-strasbg.fr/viz-bin/'
CG_PATH = 'VizieR-3?-source=J/A%2bA/618/A93/table1'
OPTIONS = '&-out.max=50&-out.form=HTML%20Table&-out.add=_r&-out.add=_RAJ,_DEJ&-sort=_r&-oc.form=sexa'
CLUSTER_ROOT = 'https://vizier.u-strasbg.fr/viz-bin/VizieR-6?-out.form=+H&-source=J/A+A/618/A93&Cluster='
CLUSTER_PLOT1 = 'http://cdsportal.u-strasbg.fr/widgets/dataplot/dataplot.html?dataset_url_1=&dataset_url_1=https%3A%2F%2Fvizier.u-strasbg.fr%2Fviz-bin%2Fvotable%3F-ref%3DVIZ5fed9b736a7e%26%2F%2Foutaddvalue%3Ddefault%26-order%3DI%26-oc.form%3Dsexa%26-c.r%3D%2520%25202%26-c.geom%3Dr%26-source%3DJ%252FA%252BA%252F618%252FA93%26Cluster%3D'
CLUSTER_PLOT2 = '%26-meta.ucd%3D2%26-meta%3D1%26-meta.foot%3D1%26-out.max%3Dunlimited%26%3DCDS%252C%2520France%26-c.eq%3DJ2000%26-c.u%3Darcmin&option_graph_title=%20J/A+A/618/A93'

# Open VizieR website
driver = webdriver.Firefox()
driver.get(VizieR_ROOT+CG_PATH+OPTIONS)

# Submit request for catalogue
driver.find_element_by_xpath("//select[@name='-out.max']/option[text()='unlimited']").click()
element = driver.find_element_by_xpath(".//*[@id='vcst']")
element.submit()

time.sleep(10)

# Make a list of all the clusters from the table
clusterlist = []
x = 0

table = driver.find_element_by_css_selector("#c36180093t1_1")

for row in table.find_elements_by_css_selector('tr'):
    x = 0
    for d in row.find_elements_by_css_selector('td'):
        x += 1
        if (x == 4):
            clusterlist.append(d.text)
            break

for clustername in clusterlist:
    clusterlink = CLUSTER_PLOT1 + clustername + CLUSTER_PLOT2
    driver.get(clusterlink)
    time.sleep(10)
    driver.save_screenshot('/home/sbalan7/Desktop/Code/charting-Gaia/plots/' + clustername + '.png')

driver.quit()