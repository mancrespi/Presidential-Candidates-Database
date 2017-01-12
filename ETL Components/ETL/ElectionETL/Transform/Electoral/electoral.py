import json


file = open("electoral.json")

elecData = json.load(file)

inserts = open("populateElect.sql", 'w')
inserts.write("use PCD_database;\n")
for (year, elec) in elecData.iteritems():
    inserts.write("insert into Electoral values({0}, {1});\n".format(year, elec))

inserts.close()