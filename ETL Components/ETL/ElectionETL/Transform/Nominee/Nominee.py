import time
import json
import re

jsonfile = open('/Users/Ibrahim/Google Drive/College/FALL16/CMSC424/Project/ETL/ElectionETL/Extract/270towin/result270towinFINAL.json', 'r')

towinData = json.load(jsonfile)
jsonfile.close()
# print towinData

candidates = []

for (year, table) in towinData.iteritems():
    for row in table:
        if row[0] != u'Candidate' and row[0] != u'Others':
            name = re.search('([a-zA-Z\ .]*)(\(I\))?', row[0].encode('ascii', 'ignore')).group(1)
            candidates.append(name)


candidates = set(candidates)
print len(candidates)


# create table Nominee(
#   NID INT NOT NULL,
#   NAME VARCHAR(100) NOT NULL,
#   PRIMARY KEY( NID )
# );


# insert into Nominee values(0, 'Hillary R. Clinton');

popfile = open('populateNominee{0}.sql'.format(str(time.time())), 'w')
popfile.write('use PCD_Database;\n')

final = {}
index = 0
for candidate in candidates:
    popfile.write("insert into Nominee values({0}, \'{1}\');\n".format(index, candidate))
    final[candidate] = str(index)
    index += 1

popfile.close

print final
linkfile = open('name-NID{0}.json'.format(str(time.time())), 'w')
linkfile.write(json.dumps(final))
linkfile.close()