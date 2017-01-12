import time
import json
import re

jsonfile = open('/Users/Ibrahim/Google Drive/College/FALL16/CMSC424/Project/ETL/ElectionETL/Extract/270towin/result270towinFINAL.json', 'r')
nameNIDfile = open('/Users/Ibrahim/Google Drive/College/FALL16/CMSC424/Project/ETL/ElectionETL/Transform/Nominee/name-NIDFINAL.json', 'r')
partyPIDfile = open('/Users/Ibrahim/Google Drive/College/FALL16/CMSC424/Project/ETL/ElectionETL/Transform/Party/party-PID.json', 'r')

towinData = json.load(jsonfile)
nameNID = json.load(nameNIDfile)
partyPID = json.load(partyPIDfile)

jsonfile.close()
nameNIDfile.close()
partyPIDfile.close()


candidates = []

for (year, table) in towinData.iteritems():
    for row in table:
        if row[0] != u'Candidate' and row[0] != u'Others':
            name = re.search('([a-zA-Z\ .]*)(\(I\))?', row[0].encode('ascii', 'ignore')).group(1)
            party = row[1].encode('ascii', 'ignore')
            i = party.find('\'')
            if i != -1:
                party = (party[:i - 1] + party[i + 1:])
            candidates.append((year.encode('ascii', 'ignore'), nameNID[name].encode('ascii', 'ignore'), partyPID[party].encode('ascii', 'ignore')))


candidates = set(candidates)
print len(candidates)

data = []
index = 0
for candidate in sorted(candidates):
              #   year         NID           PID           CID
    data.append((candidate[0], candidate[1], candidate[2], index))
    index += 1

# create table Affiliated(
#   PID INT,
#   CID INT,
#   FOREIGN KEY( PID ) references Party(PID),
#   FOREIGN KEY( CID ) references Candidate(CID)
# );
#
# create table Cand_Nom(
#   NID INT,
#   CID INT,
#   FOREIGN KEY(NID) references Nominee(NID),
#   FOREIGN KEY(CID) references Candidate(CID)
# );
#
# create table Candidate(
#   CID INT NOT NULL,
#   YEAR INT,
#   PRIMARY KEY ( CID )
# );


# insert into Candidate values(CID, year);
# insert into Cand_Nom values(NID, CID);
# insert into Affiliated values(PID, CID);


popfile = open('populateCand_CN_Aff{0}.sql'.format(str(time.time())), 'w')
popfile.write('use PCD_Database;')

final = {}
for candidate in data:
    popfile.write("insert into Candidate values({0}, {1});\n".format(candidate[3], candidate[0]))
    popfile.write("insert into Cand_Nom values({0}, {1});\n".format(candidate[1], candidate[3]))
    popfile.write("insert into Affiliated values({0}, {1});\n".format(candidate[2], candidate[3]))
    final[str(candidate[1])+':'+str(candidate[0])] = str(candidate[3])


popfile.close

print final
print len(final)
linkfile = open('NIDyr-CID{0}.json'.format(str(time.time())), 'w')
linkfile.write(json.dumps(final))
linkfile.close()