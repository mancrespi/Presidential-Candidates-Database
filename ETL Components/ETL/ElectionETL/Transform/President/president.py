import time
import json
import re


def getDate(x):
    dobre = re.search('(\d\d-\d\d)[a-zA-Z ]*\d\d?, (\d\d\d\d)', x.encode('ascii', 'ignore'))
    return dobre.group(1) + "-" + dobre.group(2)  # MM-DD-YYYY

def removeQoutes(x):
    temp = x.find('\'')
    while(temp != -1):
        x = x[:temp-1]+x[temp+1:]
        temp = x.find('\'')

    return x

def removeCommas(x):
    flag = x.find(',')
    while(flag!=-1):
        x = x[:flag-1]+x[flag+1:]
        flag = x.find(',')

    return x


def turnIntoDict(llist):
    dict = {}
    for l in llist:
        temp = int(l[0])
        name = l[1].encode('ascii','ignore')
        slogan = l[2].encode('ascii', 'ignore')

        if not (dict.has_key(temp)):
            dict[temp] = []
            dict[temp].append([name, slogan])
        else:
            found = False
            for ent in dict[temp]:
                if ent[0] == name:
                    ent[1] = ent[1]+" - "+slogan
                    found = True
            if not found:
                dict[temp].append([name, slogan])

    return dict

def matchLastname(x, ylist):
    given = re.search('([a-zA-Z\ .]*) ([a-zA-Z]*)', x).group(2)
    names = {}
    for y in ylist:
        y[0] = y[0].encode('ascii', 'ignore')
        # print y[0]
        lastname = re.search('([a-zA-Z\ .]*) ([a-zA-Z]*) (\(([a-zA-Z]*)\))?', y[0]).group(2)
        names[lastname] = int(y[1])

    if given in names.keys():
        return names[given]
    return -1


def matchLastnameSlogan(x, ylist):
    given = re.search('([a-zA-Z\ .]*) ([a-zA-Z]*)', x).group(2)
    names = {}
    for y in ylist:
        # print y[0]

        lastname = re.search('([a-zA-Z\ .]*) ([a-zA-Z]*)', y[0]).group(2)
        # print lastname
        # print y[1]
        names[lastname] = y[1]

    if given in names.keys():
        return names[given]
    return 'NULL'

jsonfile = open('/Users/Ibrahim/Google Drive/College/FALL16/CMSC424/Project/ETL/ElectionETL/Extract/270towin/result270towinFINAL.json', 'r')
jsonPollsfile = open('/Users/Ibrahim/Google Drive/College/FALL16/CMSC424/Project/ETL/ElectionETL/Extract/polls/resultPollsFINAL.json', 'r')
jsonSloganfile = open('/Users/Ibrahim/Google Drive/College/FALL16/CMSC424/Project/ETL/ElectionETL/Extract/Slogans/resultSlogansFINAL.json', 'r')
jsonSpendingfile = open('/Users/Ibrahim/Google Drive/College/FALL16/CMSC424/Project/ETL/ElectionETL/Extract/campiagn/spending.json', 'r')
jsonContribfile = open('/Users/Ibrahim/Google Drive/College/FALL16/CMSC424/Project/ETL/ElectionETL/Extract/campiagn/contributions.json', 'r')
jsonPhafile = open('/Users/Ibrahim/Google Drive/College/FALL16/CMSC424/Project/ETL/ElectionETL/Extract/president-homestate-age/phaFAINL.json', 'r')


nameNIDfile = open('/Users/Ibrahim/Google Drive/College/FALL16/CMSC424/Project/ETL/ElectionETL/Transform/Nominee/name-NIDFINAL.json', 'r')
partyPIDfile = open('/Users/Ibrahim/Google Drive/College/FALL16/CMSC424/Project/ETL/ElectionETL/Transform/Party/party-PID.json', 'r')
NIDyrCIDfile = open('/Users/Ibrahim/Google Drive/College/FALL16/CMSC424/Project/ETL/ElectionETL/Transform/Candidate-C_N-Affi/NIDyr-CID.json', 'r')

towinData = json.load(jsonfile)
pollsData = json.load(jsonPollsfile)
slogansData = turnIntoDict(json.load(jsonSloganfile)["slogans"])
spending = json.load(jsonSpendingfile)
contrib = json.load(jsonContribfile)
pha = json.load(jsonPhafile)

NIDyrCID = json.load(NIDyrCIDfile)
nameNID = json.load(nameNIDfile)
partyPID = json.load(partyPIDfile)

jsonfile.close()
nameNIDfile.close()
partyPIDfile.close()


candidates = []
names = []

for (year, table) in towinData.iteritems():
    for row in table:
        if row[0] != u'Candidate' and row[0] != u'Others':
            name = re.search('([a-zA-Z\ .]*)(\(I\))?', row[0].encode('ascii', 'ignore')).group(1)
            party = row[1].encode('ascii', 'ignore')
            i = party.find('\'')
            if i != -1:
                party = (party[:i - 1] + party[i + 1:])


            temp = []
            temp = [year.encode('ascii', 'ignore'),
                    name,
                    nameNID[name].encode('ascii', 'ignore'),
                    partyPID[party].encode('ascii', 'ignore'),
                    int(row[2].encode('ascii', 'ignore'))]

            if len(row) == 4 and row[3] != '***' and row[3] != 'Unknown':
                # both elec and popular votes
                popular = int(removeCommas(row[3].encode('ascii', 'ignore')))
                temp.append(popular)
            else:
                temp.append(-1)

            candidates.append(temp)

presidents = {}
counter = 1
prev = pha['president-dob-birthPlace-homeState-inOffice'][0]
for ent in pha['president-dob-birthPlace-homeState-inOffice'][1:]:
    counter += 1
    # print prev
    lastname = prev[0].encode('ascii','ignore')
    dob = getDate(prev[1])
    city = re.search('([a-zA-Z\ .]*)', prev[2].encode('ascii', 'ignore')).group(1)
    state = re.search('^[a-zA-Z]*? ?!?[a-zA-Z ]*?\/?([a-zA-Z ]*)$', prev[3].encode('ascii', 'ignore')).group(1)
    periodre = re.search('^\d?\d? ?!?([a-zA-Z 0-9,]*)  \d?\d? ?!?([a-zA-Z 0-9,]*)$', prev[4].encode('ascii', 'ignore'))
    # print prev[4]
    period = periodre.group(1) + " - " + periodre.group(2)
    # print period
    presidents[lastname] = [dob, city, state, period]



    if len(ent) == 1:
        temp = prev[:4]
        temp.append(ent[0])
        prev = temp
    else:
        prev = ent

# print prev
lastname = prev[0]
# print lastname
dob = getDate(prev[1])
city = re.search('([a-zA-Z\ .]*)', prev[2].encode('ascii', 'ignore')).group(1)
state = re.search('^[a-zA-Z]*? ?!?[a-zA-Z ]*?\/?([a-zA-Z ]*)$', prev[3].encode('ascii', 'ignore')).group(1)
periodre = re.search('^\d?\d? ?!?([a-zA-Z 0-9,]*)  \d?\d? ?!?([a-zA-Z 0-9,]*)$', prev[4].encode('ascii', 'ignore'))
# print prev[4]
period = periodre.group(1)+" - "+periodre.group(2)
# print period
presidents[lastname.encode('ascii','ignore')] = [dob, city, state, period]


print presidents




print len(candidates)
print "year,  name,  nid,  pid,  elec,  pop, CID"
for candidate in candidates:
    candidate.append(int(NIDyrCID[str(candidate[2])+":"+str(candidate[0])]))
    lastname = re.search('([a-zA-Z\ .]*) ([a-zA-Z]*)', candidate[1]).group(2)



    # print candidate
print len(presidents.keys())

inserts = []
for candidate in candidates:
    lastname = re.search('([a-zA-Z\ .]*) ([a-zA-Z]*)', candidate[1]).group(2)
    if presidents.has_key(lastname):
        ins = presidents[lastname]
        inserts.append([candidate[6], ins[0], ins[1], ins[2]])

print "presidents"
print len(inserts)


# create table President(
#   NAME VARCHAR(100) NOT NULL,
#   DOB DATE NOT NULL,
#   BIRTHPLACE VARCHAR(100),
#   HOMESTATE VARCHAR(100)
# );


# insert into President values(name, DOB, BirthPlace, homestate);


popfile = open('populatePresident{0}.sql'.format(str(time.time())), 'w')
popfile.write('use PCD_Database;\n')

# ##"year,  name,  nid,  pid,  elec,  pop,  polls, CID,  spending, contrib"


for (president, attrib) in presidents.iteritems():
    popfile.write("insert into President values(\'{0}\', STR_TO_DATE(\'{1}\', \'%m-%d-%Y\'), \'{2}\', \'{3}\', \'{4}\');\n".format(president, attrib[0], attrib[1], attrib[2], attrib[3]))


popfile.close

# print cid_slogan
# print len(cid_slogan)
# linkfile = open('CID-slogan{0}.json'.format(str(time.time())), 'w')
# linkfile.write(json.dumps(cid_slogan))
# linkfile.close()