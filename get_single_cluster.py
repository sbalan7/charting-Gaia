from selenium import webdriver
import time
import sys


VizieR_ROOT = 'https://vizier.u-strasbg.fr/viz-bin/'
CG_PATH = 'VizieR-3?-source=J/A%2bA/618/A93/table1'
OPTIONS = '&-out.max=50&-out.form=HTML%20Table&-out.add=_r&-out.add=_RAJ,_DEJ&-sort=_r&-oc.form=sexa'

# Open VizieR website
driver = webdriver.Firefox()
driver.get(VizieR_ROOT+CG_PATH+OPTIONS)

# Submit request for catalogue
driver.find_element_by_xpath("//select[@name='-out.max']/option[text()='unlimited']").click()
element = driver.find_element_by_xpath(".//*[@id='vcst']")
element.submit()

time.sleep(30)

# Make a list of all the clusters from the table
targetcluster = sys.argv[1]

table = driver.find_element_by_css_selector("#c36180093t1_1")

for row in table.find_elements_by_css_selector('tr'):
    x = 0
    for d in row.find_elements_by_css_selector('td'):
        x += 1
        if (x == 4):
            if d.text == targetcluster:
                print(d.get_attribute("href"))
            break

