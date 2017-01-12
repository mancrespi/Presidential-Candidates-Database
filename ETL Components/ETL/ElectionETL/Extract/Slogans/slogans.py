from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup
import time
import json


Windows = False


"""
data paresed is in following fashon

fainl = {
        "slogans":
            [
            [year  , candi. , slogan ],
            [2050  , name1  , "word" ],
            [2054  , name2  , "good" ],
            [2058  , name3  , "now"  ],
            .....

            ]
        }
"""


# downloading page

if Windows:
    binary = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')
    browser = webdriver.Firefox(firefox_binary=binary)
else:
    browser = webdriver.Firefox()

browser.get('http://www.presidentsusa.net/campaignslogans.html')


# getting table
table = browser.find_element_by_xpath(
        '//*[@id="slogans-page"]/div[1]/div[2]/div/div[2]/div[1]/ul'
        ).get_attribute('innerHTML')
soup = BeautifulSoup(table, 'html.parser')
browser.quit()


# parsing table
data = []
counter = 1
tbody = soup.find('tbody')
rows = tbody.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    currdata = [ele for ele in cols if ele]
    if (currdata != []):
        data.append(currdata)

    print "read: " + str(counter) + " cols "
    counter += 1


jsonfile = open('resultSlogans{0}.json'.format(str(time.time())), 'w')
jsonfile.write(json.dumps({"slogans": data}))
jsonfile.close()
