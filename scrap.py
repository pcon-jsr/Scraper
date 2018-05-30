from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import bs4
import csv
import pandas as pd
import numpy as np

driver = webdriver.Firefox()
driver.get('http://14.139.205.172/web_new/Default.aspx')

with open('mcaresult.csv', 'w') as f:
    f.write("RegId" + "," + "Name" + "," + "CGPA" + "\n")

#NA = [8,13,58,69,72,86]

for i in range(1,79):
	if i != 23 and i!=47 and i!=56 and i!=66:
		roll = str(i)
		if i<10:
			regno = '2017PGCACA0' + roll
		else: 
			regno = '2017PGCACA' + roll
		
		driver.find_element_by_name('txtRegno').clear()
		driver.find_element_by_name('txtRegno').send_keys(regno)
		driver.find_element_by_name('btnimgShow').click()
		sem = Select(driver.find_element_by_name('ddlSemester'))
		sem.select_by_value('2')
		showresult = driver.find_element_by_name('btnimgShowResult')
		showresult.click()
		res = driver.page_source
		soup = bs4.BeautifulSoup(res,'lxml')
		cg = soup.select('#lblCPI')
		cg = float(cg[0].text)
		cg=str(cg)
		name = soup.select('#lblSName')
		name = str(name[0].text)

		with open('mcaresult.csv', 'a') as f:
			f.write(regno+","+name+","+cg+"\n")


df=pd.read_csv('mcaresult.csv')
df=df.sort_values('CGPA',ascending=[False])
df.insert(0, 'Rank', range(1,1+len(df)))
df.head(15)
df.to_csv('mcaoutput.csv', encoding='utf-8', index=False)




	