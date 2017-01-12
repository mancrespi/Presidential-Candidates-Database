import time
import json
import re

jsonfile = open('/Users/Ibrahim/Google Drive/College/FALL16/CMSC424/Project/ETL/ElectionETL/Extract/270towin/result270towinFINAL.json', 'r')
nameNIDfile = open('/Users/Ibrahim/Google Drive/College/FALL16/CMSC424/Project/ETL/ElectionETL/Transform/Nominee/name-NIDFINAL.json', 'r')

towinData = json.load(jsonfile)
nameNID = json.load(nameNIDfile)
jsonfile.close()
nameNIDfile.close()
# print towinData

data = []

for (year, table) in towinData.iteritems():
    for row in table:
        if row[1].encode('ascii', 'ignore') != "Party":
            party = row[1].encode('ascii', 'ignore')
            i = party.find('\'')
            if i == -1:
                data.append(party)
            else:
                data.append(party[:i-1]+party[i+1:])

data = set(data)
print len(data)


for index in sorted(data):
    print index



# create table Party(
#   PID INT NOT NULL,
#   P_NAME VARCHAR(100),
#   PRIMARY KEY( PID )
# );


# insert into Party values(0, 'Republican');

popfile = open('populateParty{0}.sql'.format(str(time.time())), 'w')
popfile.write('use PCD_Database;\n')

final = {}
index = 0
for party in data:
    popfile.write("insert into Party values({0}, \'{1}\');\n".format(index, party))
    final[party] = str(index)
    index += 1

popfile.close
print final
print len(final)
linkfile = open('party-PID{0}.json'.format(str(time.time())), 'w')
linkfile.write(json.dumps(final))
linkfile.close()