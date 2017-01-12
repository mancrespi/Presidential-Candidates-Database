from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup
import time
import json

Windows = False


"""
data paresed is in following fashon

fainl = {
        1789:   [
                [candi. , party , elec. , popular ],
                [name1  , party1, 333   , 444     ],
                [name2  , party2, 363   , 484     ]
                ],
        1792:   [
                [candi. , party , elec. , popular ],
                [name1  , party1, 333   , 444     ],
                [name2  , party2, 363   , 484     ]
                ],
        1796:   ....,
        1800:   ....
        }

"""


def get_election_years():
    elec_yrs = [1789]
    i = 1792
    while i <= 2016:
        elec_yrs.append(i)
        i += 4

    return elec_yrs


elecyears = get_election_years()


def get_270towin_links():
    links = {}
    for elecyear in get_election_years():
        links[elecyear] = 'http://www.270towin.com/' + str(elecyear) + '_Election/'

    return links


if Windows:
    binary = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')
    browser = webdriver.Firefox(firefox_binary=binary)
else:
    browser = webdriver.Firefox()

counter = 1
final = {}
for (year, link) in get_270towin_links().iteritems():
    print "loaded:"+str(counter)+" out of "+str(len(elecyears))
    counter += 1

    browser.get(link)
    table = browser.find_element_by_xpath(
        '//*[@id="wrapper"]/table[2]/tbody/tr/td[1]/table/tbody/tr[3]/td/div'
        ).get_attribute('innerHTML')
    soup = BeautifulSoup(table, 'html.parser')

    data = []
    tbody = soup.find('tbody')
    rows = tbody.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])

    final[year] = data

browser.close()
jsonfile = open('result270towin{0}.json'.format(str(time.time())), 'w')
jsonfile.write(json.dumps(final))
jsonfile.close()
