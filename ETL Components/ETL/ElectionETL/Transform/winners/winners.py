import json


file = open('winnerbyelec.json', 'r')
NIDyrCIDfile = open('/Users/Ibrahim/Google Drive/College/FALL16/CMSC424/Project/ETL/ElectionETL/Transform/Candidate-C_N-Affi/NIDyr-CID.json', 'r')
nameNIDfile = open('/Users/Ibrahim/Google Drive/College/FALL16/CMSC424/Project/ETL/ElectionETL/Transform/Nominee/name-NIDFINAL.json', 'r')


winners = json.load(file)
NIDyrCID = json.load(NIDyrCIDfile)
nameNID = json.load(nameNIDfile)


print winners
# zero is false

popfile = open('populateWinners.sql', 'w')
popfile.write('use pcd_database;\n')
winners = winners['winners']

done = []
for winner in winners:
    nid = nameNID[winner[0]]
    cid = NIDyrCID[nid+":"+winner[1]]
    done.append(cid)
    popfile.write("insert into winners values({0}, {1});\n".format(cid, str(1)))

for index in range(0, 155):
    if str(index) not in done:
        popfile.write("insert into winners values({0}, {1});\n".format(index, str(0)))

popfile.close()
