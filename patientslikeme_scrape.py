#A semi-automated web scraper for PatientsLikeMe user data

#Import necessary packages

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import pandas as pd
import random
import time

#import login information from another file

from logins_patientslikeme import username, password

#Initiate webdriver 

options = Options()
options.headless  = False

driver = webdriver.Chrome(options = options, executable_path='/Downloads/chromedriver 2')

#get login page using driver

driver.get('https://www.patientslikeme.com/users/sign_in')

driver.maximize_window()


#Send login credentials to login page

time.sleep(1)

driver.find_element_by_id("user_email_or_login").send_keys(username)

time.sleep(1)

driver.find_element_by_id("user_password").send_keys(password)
time.sleep(1)

#Sleep script so we can solve recaptcha challenge and sign in

time.sleep(20)

#create dataframe to add data into

df = pd.DataFrame()

#loop through 806 pages of users with epilepsy and gather data

for i in range(1, 807):
    url = f'https://www.patientslikeme.com/patients/searches/detail_search?page={i}&saved_search_id=22523'
    driver.get(url)
    source = driver.page_source
    soup = BeautifulSoup(source, 'html.parser')
    text = soup.find_all('div', {'data-react-class':"ProfileSummaryPropsContainer"})
    for x in text:
        #load data as a json and convert to a pandas dataframe format
        js = json.loads(x['data-react-props'])
        dfx = pd.DataFrame([js]).set_index('id')
        #if script is interrupted, print the page number it stopped on
        if len(dfx) == 0:
            print('Stopped at' + str(i))
            driver.close()
            break
        #append new data to existing dataframe
        df = df.append(dfx)
    #sleep script to prevent causing performance issues on website
    time.sleep(random.uniform(5,10))

#transfer data to csv file
df.to_csv('webscrape_PLM.csv')

driver.close()

