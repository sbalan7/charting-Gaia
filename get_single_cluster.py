from selenium import webdriver
import time
import sys


VizieR_ROOT = 'https://vizier.u-strasbg.fr/viz-bin/'
OPTIONS = 'VizieR-6?-out.form=%2bH&-source=J/A%2bA/618/A93&Cluster='

targetcluster = sys.argv[1]

# Open VizieR website
driver = webdriver.Firefox()
driver.get(VizieR_ROOT+OPTIONS+targetcluster)

driver.find_element_by_xpath("//select[@name='-out.max']/option[text()='unlimited']").click()
element = driver.find_element_by_xpath("/html/body/div[4]/div/form/div[1]/div/div/div[2]/div[2]/div/table/tbody/tr/td/input").click()

time.sleep(15)
driver.quit()