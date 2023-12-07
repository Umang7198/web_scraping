from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

driver = webdriver.Chrome()
url = "https://ocimpact.com/delegate-roster"
driver.get(url)
time.sleep(5)
driver.find_element(By.XPATH, "//*[@id='om-kqxypdy18uglll6v2jry-optin']/div/button").click()
time.sleep(5)
driver.switch_to.frame(driver.find_elements(By.TAG_NAME, "iframe")[0])

names = []
titles = []
organizations = []
links = []
que1=[]
que2=[]
que3=[]
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    p = driver.page_source
    soup = BeautifulSoup(p,'lxml')
    profs = soup.find_all('div',{'class': "style__UIBox-ui__sc-134aw2g-0"})

    for prof in profs:
        name = prof.find('span',{'class':"grid__FullName-cmp__sc-1x1x5ym-3"})
        if(name!=None):
            name1 = name.get_text(strip=True)
        else:
            name1 = ""
        
        title = prof.find('span',{'class':"grid__Job-cmp__sc-1x1x5ym-5"})
        if(title!=None):
            title1 = title.get_text(strip=True)
        else:
            title1 = ""
        
        org = prof.find('span',{'class':"grid__Organization-cmp__sc-1x1x5ym-6"})
        if(org!=None):
            org1 = org.get_text(strip=True)
        else:
            org1 = ""

        link = prof.find('a', href=True)
        if(link!=None):
            link1 = link['href']
        else:
            link1 = ""
         # links to respective profile page
            
        names.append(name1)
        titles.append(title1)
        organizations.append(org1)
        links.append('https://ocimpact.app.swapcard.com'+link1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

#print(organizations)
dic = {'Name':names, 'Job title':titles, 'Organization':organizations, 'link':links}
df1 = pd.DataFrame(dic)
df1.drop_duplicates(inplace=True)

df1.to_csv("info.csv", header=True, index=False)

print(df1.shape)

print(len(links))