import time
import json
import re

def removeCommas(x):
    flag = x.find(',')
    while(flag!=-1):
        x = x[:flag-1]+x[flag+1:]
        flag = x.find(',')

    return x


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


jsonfile = open('/Users/Ibrahim/Google Drive/College/FALL16/CMSC424/Project/ETL/ElectionETL/Extract/270towin/result270towinFINAL.json', 'r')
jsonPollsfile = open('/Users/Ibrahim/Google Drive/College/FALL16/CMSC424/Project/ETL/ElectionETL/Extract/polls/resultPollsFINAL.json', 'r')
nameNIDfile = open('/Users/Ibrahim/Google Drive/College/FALL16/CMSC424/Project/ETL/ElectionETL/Transform/Nominee/name-NIDFINAL.json', 'r')
partyPIDfile = open('/Users/Ibrahim/Google Drive/College/FALL16/CMSC424/Project/ETL/ElectionETL/Transform/Party/party-PID.json', 'r')
NIDyrCIDfile = open('/Users/Ibrahim/Google Drive/College/FALL16/CMSC424/Project/ETL/ElectionETL/Transform/Candidate-C_N-Affi/NIDyr-CID.json', 'r')


towinData = json.load(jsonfile)
pollsData = json.load(jsonPollsfile)
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

    # print candidate

# create table Ballot(
#   CID INT,
#   POPULAR INT,
#   ELECTORAL INT,
#   POLLS INT,
#   FOREIGN KEY( CID ) references Candidate(CID)
# );


# insert into Ballot values(CID, popular, electoral, polls);


popfile = open('populateBallot{0}.sql'.format(str(time.time())), 'w')
popfile.write('use PCD_Database;\n')

##"year,  name,  nid,  pid,  elec,  pop,  polls, CID"

final = {}
for candidate in candidates:
    popular = candidate[5]
    if candidate[5] == -1:
        popular = 'NULL'
    polls = candidate[6]
    if candidate[6] == -1:
        polls = 'NULL'

    popfile.write("insert into Ballot values({0}, {1}, {2}, {3});\n".format(candidate[7], popular, candidate[4], polls))
    final[str(candidate[7])] = str(polls)


popfile.close

print final
print len(final)
linkfile = open('CID-poll{0}.json'.format(str(time.time())), 'w')
linkfile.write(json.dumps(final))
linkfile.close()