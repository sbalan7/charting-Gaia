from selenium import webdriver
import json
import time
import sys
import os

with open('select.json') as f:
    data = json.load(f)

info = {}
for key, values in data.items():
    info[key] = (values['isochrone'].replace('gy', 'e9'), values['metallicity'])

driver = webdriver.Firefox()

for cluster, (age, met) in info.items():
    print(cluster)
    path = os.getcwd() + '/isochrones/' + cluster.replace(' ', '_') + '.dat'
    driver.get("http://stev.oapd.inaf.it/cgi-bin/cmd")
    system_select = driver.find_element_by_xpath("/html/body/form/div/fieldset[2]/p/select/option[32]").click()
    in1 = driver.find_element_by_xpath("/html/body/form/div/fieldset[7]/table/tbody/tr[3]/td[2]/input")
    in1.clear()
    in1.send_keys(age)
    in2 = driver.find_element_by_xpath("/html/body/form/div/fieldset[7]/table/tbody/tr[3]/td[3]/input")
    in2.clear()
    in2.send_keys(age)
    driver.find_element_by_xpath("/html/body/form/div/fieldset[7]/table/tbody/tr[7]/td[1]/input").click()
    in3 = driver.find_element_by_xpath("/html/body/form/div/fieldset[7]/table/tbody/tr[7]/td[2]/input")
    in3.clear()
    in3.send_keys(met)
    in4 = driver.find_element_by_xpath("/html/body/form/div/fieldset[7]/table/tbody/tr[7]/td[3]/input")
    in4.clear()
    in4.send_keys(met)
    driver.find_element_by_xpath("/html/body/form/div/input[4]").click()
    print("loaded_data")
    time.sleep(10)
    driver.find_element_by_xpath("/html/body/form/fieldset[1]/p[1]/a").click()
    time.sleep(10)
    with open(path, 'w') as f:
        f.write(driver.page_source)
    print("done")

driver.quit()