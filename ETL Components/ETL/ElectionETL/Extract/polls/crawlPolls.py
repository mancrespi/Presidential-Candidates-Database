from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup
import re
import time
import json


Windows = False


"""
data paresed is in following fashon

fainl = {
        "year":
            [ [candi,poll], [candi,poll] ],
        "year":
            [ [candi,poll], [candi,poll] ],
        ....
        }
"""


# downloading page

if Windows:
    binary = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')
    browser = webdriver.Firefox(firefox_binary=binary)
else:
    browser = webdriver.Firefox()

browser.get('https://en.wikipedia.org/wiki/Historical_polling_for_U.S._Presidential_elections')


# getting table
tables = browser.find_elements_by_xpath('//*[@id="mw-content-text"]/table[@class="wikitable"]')

soups = {}
counter = 2
for table in tables:
    key = BeautifulSoup(table.find_element_by_xpath('//*[@id="mw-content-text"]/table['+str(counter)+']/caption/b/a').get_attribute('innerHTML'), 'html.parser')
    value = BeautifulSoup(table.get_attribute('innerHTML'), 'html.parser')
    soups[key] = value
    counter += 1

browser.quit()

final = {}
counter = 1
for (elec_year, soup) in soups.iteritems():
    print "read: " + str(counter) + " cols "
    counter += 1
    # parsing table
    tbody = soup.find('tbody')
    candis = []
    heads = tbody.find_all('th')
    for head in heads:
        candis.append(head.text)

    candis = candis[1:]

    data = []

    rows = tbody.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        currdata = [ele for ele in cols if ele]
        if (currdata != []):
            if(currdata[0] == u'Difference between actual result and final poll' or currdata[0] == u'Actual result'):
                data.append(currdata[1:])

    index = 0
    final[str(elec_year)] = []
    for candi in candis:
        actual = int( re.search('(.*)(-?[0-9]*)%(.*)', data[0][index]).group(1) )
        differ = int( re.search('(.*)(-?[0-9]*)%(.*)', data[1][index]).group(1) )
        final[str(elec_year)].append([candi, str(actual - differ)])
        index += 1


jsonfile = open('resultPolls{0}.json'.format(str(time.time())), 'w')
jsonfile.write(json.dumps(final))
jsonfile.close()
