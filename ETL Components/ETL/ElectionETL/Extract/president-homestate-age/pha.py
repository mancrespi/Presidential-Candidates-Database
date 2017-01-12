from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup
import time
import json


Windows = False


"""
data paresed is in following fashon

final = {
        "president-dob-birthPlace-homeState-inOffice":
            [
            [name  , DOB , birthPlace , homeState , period in office ],
            [                      ......                            ],
            [                      ......                            ],
            [                      ......                            ],
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

browser.get('https://en.wikipedia.org/wiki/List_of_Presidents_of_the_United_States_by_home_state')


# getting table
table = browser.find_element_by_xpath(
        '//*[@id="mw-content-text"]/table[4]'
        ).get_attribute('innerHTML')
soup = BeautifulSoup(table, 'html.parser')
browser.quit()


# parsing table
data = []
counter = 1
tbody = soup.find('tbody')
rows = tbody.find_all('tr')
print len(rows)
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    currdata = [ele for ele in cols if ele]
    if currdata != []:
        data.append(currdata)

    print "read: " + str(counter) + " cols "
    counter += 1

print len(data)

jsonfile = open('pha{0}.json'.format(str(time.time())), 'w')
jsonfile.write(json.dumps({"president-dob-birthPlace-homeState-inOffice": data}))
jsonfile.close()
