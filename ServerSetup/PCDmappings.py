import json

def getCandidates():
	filename = open("./name-NIDFINAL.json", 'r')
	c = json.load(filename)
	return sorted(c.keys())

def get_election_years():
    elec_yrs = ["1789"]
    i = 1792
    while i <= 2016:
        elec_yrs.append(str(i))
        i += 4
    return elec_yrs

def getParties():
	filename = open("./party-PID.json", 'r')
	c = json.load(filename)
	return sorted(c.keys())