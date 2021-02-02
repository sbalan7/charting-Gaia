from selenium import webdriver
import json
import time
import sys
import os

with open('select.json') as f:
    data = json.load(f)

ages = []
for key, values in data.items():
    ages.append(values['isochrone'].replace('gy', 'e9'))
ages = list(set(ages))

driver = webdriver.Firefox()

for age in ages:
    path = os.getcwd() + '/isochrones/' + age.replace('e9', 'gy') + '.dat'
    if os.path.isfile(path) and not sys.argv[1]:
        continue
    driver.get("http://stev.oapd.inaf.it/cgi-bin/cmd_3.4")
    system_select = driver.find_element_by_xpath("/html/body/form/div/fieldset[2]/p/select/option[32]").click()
    in1 = driver.find_element_by_xpath("/html/body/form/div/fieldset[7]/table/tbody/tr[3]/td[2]/input")
    in1.clear()
    in1.send_keys(age)
    in2 = driver.find_element_by_xpath("/html/body/form/div/fieldset[7]/table/tbody/tr[3]/td[3]/input")
    in2.clear()
    in2.send_keys(age)
    driver.find_element_by_xpath("/html/body/form/div/input[4]").click()
    time.sleep(5)
    driver.find_element_by_xpath("/html/body/form/fieldset[1]/p[1]/a").click()
    time.sleep(5)
    with open(path, 'w') as f:
        f.write(driver.page_source)

driver.quit()