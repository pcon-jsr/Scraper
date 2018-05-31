from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoAlertPresentException
import bs4
import csv
import pandas as pd
import numpy as np

def is_alert_present():
    try: driver.switch_to_alert().accept()
    except NoAlertPresentException, e: return False
    return True

driver = webdriver.Firefox()
driver.get('http://14.139.205.172/web_new/Default.aspx')

with open('result.csv', 'w') as f:
    f.write("RegId" + "," + "Name" + "," + "CGPA" + "\n")

for i in range(1,93):
    roll = str(i)
    if i<10:
        regno = '2015UGCS00' + roll
    else: 
        regno = '2015UGCS0' + roll
    
    driver.find_element_by_name('txtRegno').clear()
    driver.find_element_by_name('txtRegno').send_keys(regno)
    driver.find_element_by_name('btnimgShow').click()

    if is_alert_present() == True:
    	driver.close()
    	driver = webdriver.Firefox()
    	driver.get('http://14.139.205.172/web_new/Default.aspx')
    else:
        sem = Select(driver.find_element_by_name('ddlSemester'))
        sem.select_by_value('6')
        showresult = driver.find_element_by_name('btnimgShowResult')
        showresult.click()
        res = driver.page_source
        soup = bs4.BeautifulSoup(res,'lxml')
        name = soup.select('#lblSName')
        name = str(name[0].text)
        cg = soup.select('#lblCPI')
        cg = float(cg[0].text)
        cg=str(cg)

        with open('result.csv', 'a') as f:
            f.write(regno+","+name+","+cg+"\n")

df=pd.read_csv('result.csv')
df=df.sort_values('CGPA',ascending=[False])
df.insert(0, 'Rank', range(1,1+len(df)))
df.to_csv('output.csv', encoding='utf-8', index=False)
