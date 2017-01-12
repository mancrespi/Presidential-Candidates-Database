import time
import json
import re


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

nameNIDfile = open('/Users/Ibrahim/Google Drive/College/FALL16/CMSC424/Project/ETL/ElectionETL/Transform/Nominee/name-NIDFINAL.json', 'r')
partyPIDfile = open('/Users/Ibrahim/Google Drive/College/FALL16/CMSC424/Project/ETL/ElectionETL/Transform/Party/party-PID.json', 'r')
NIDyrCIDfile = open('/Users/Ibrahim/Google Drive/College/FALL16/CMSC424/Project/ETL/ElectionETL/Transform/Candidate-C_N-Affi/NIDyr-CID.json', 'r')


towinData = json.load(jsonfile)
pollsData = json.load(jsonPollsfile)
slogansData = turnIntoDict(json.load(jsonSloganfile)["slogans"])
spending = json.load(jsonSpendingfile)
contrib = json.load(jsonContribfile)

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




cid_slogan = {}
print len(candidates)
print "year,  name,  nid,  pid,  elec,  pop,  polls, CID"
for candidate in candidates:
    if int(candidate[0]) >= 1936:
        temp = matchLastname(candidate[1], pollsData[candidate[0]])
        if temp != -1:
            candidate.append(temp)
        else:
            candidate.append(-1)
    else:
        candidate.append(-1)


    candidate.append(int(NIDyrCID[str(candidate[2])+":"+str(candidate[0])]))


    if int(candidate[0]) >= 1840 and slogansData.has_key(int(candidate[0])):
        # print "checking "+candidate[1]+" on "+str(candidate[0])
        cid_slogan[candidate[7]] = matchLastnameSlogan(candidate[1], slogansData[int(candidate[0])])
    else:
        cid_slogan[candidate[7]] = 'NULL'




    lastname = re.search('([a-zA-Z\ .]*) ([a-zA-Z]*)', candidate[1]).group(2)
    found = False
    if spending.has_key(candidate[0]):
        for one in spending[candidate[0]]:
            if one[0] == lastname:
                candidate.append(int(one[1]))
                found = True
                break

        if not found:
            candidate.append('NULL')
    else:
        candidate.append('NULL')

    found = False
    if contrib.has_key(candidate[0]):
        for one in contrib[candidate[0]]:
            if one[0] == lastname:
                candidate.append(int(one[1]))
                found = True
                break

        if not found:
            candidate.append('NULL')
    else:
        candidate.append('NULL')


    # print candidate

# print spending
# print contrib
# print cid_slogan

# create table Campaign (
#   CID INT,
#   EXPENSES INT,
#   CONTRIB INT,
#   SLOGAN VARCHAR(100),
#   FOREIGN KEY( CID ) references Candidate(CID)
# );


# insert into Campaign values(CID, Spending, Contributions, slogan);


popfile = open('populateCampaign{0}.sql'.format(str(time.time())), 'w')
popfile.write('use PCD_Database;\n')

##"year,  name,  nid,  pid,  elec,  pop,  polls, CID,  spending, contrib"


for candidate in candidates:

    if cid_slogan.has_key(candidate[7]):
        if cid_slogan[candidate[7]] == 'NULL':
            popfile.write("insert into Campaign values({0}, {1}, {2}, {3});\n".format(candidate[7], candidate[8], candidate[9], cid_slogan[candidate[7]] ))
        else:
            popfile.write("insert into Campaign values({0}, {1}, {2}, \'{3}\');\n".format(candidate[7], candidate[8], candidate[9], removeQoutes(cid_slogan[candidate[7]])))
    else:
        popfile.write("insert into Campaign values({0}, {1}, {2}, NULL);\n".format(candidate[7], candidate[8], candidate[9]))



popfile.close

print cid_slogan
print len(cid_slogan)
linkfile = open('CID-slogan{0}.json'.format(str(time.time())), 'w')
linkfile.write(json.dumps(cid_slogan))
linkfile.close()