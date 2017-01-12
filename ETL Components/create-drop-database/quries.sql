
-- MODE 1 --> givenYear
-- Typically, we would like to have queries to return information on a given year, such as
-- candidates, their party affiliation, percentage of votes received, winner, polls prior to the
-- election etc. 
-- year, candidate, party, (all ballot fields), winner or not


SELECT C.year, C.CID, P.P_name, N.name, B.electoral, W.ISA
FROM Nominee N, Cand_Nom CN, Candidate C, Ballot B, winners W, party P, Affiliated A
WHERE C.year = 2008
AND N.NID = CN.NID
AND CN.CID = C.CID
AND C.CID = B.CID
AND W.CID = C.CID
AND A.CID = C.CID
AND A.PID = P.PID


-- MODE 2 --> candidate
-- This query will return information on a given president or candidate, including the years he
-- ran, the results, etc. 

SELECT C.year, C.CID, N.name, B.electoral, B.popular, B.polls, W.ISA
FROM Nominee N, Cand_Nom CN, Candidate C, Ballot B, winners W
WHERE N.name = 'Theodore Roosevelt'
AND N.NID = CN.NID
AND CN.CID = C.CID
AND C.CID = B.CID
AND W.CID = C.CID


-- MODE 3 --> no input
-- This query will find, presidents that were re-elected after losing one or more elections in
-- between. 

SELECT name 
FROM president 
WHERE inoffice like '%/%';


-- MODE 4 --> no input
-- Find any candidates who ran on one party one time and on another party another time. For
-- each such candidate, return the information asked in (2.2.2) above. 

SELECT C1.year, N1.name, P1.P_name, B1.electoral, B1.popular, B1.polls, W1.ISA
FROM Nominee N1, Cand_Nom CN1, Candidate C1, Ballot B1, winners W1, party P1, Affiliated A1
WHERE (SELECT count(DISTINCT(P.P_name))
		FROM Nominee N, Cand_Nom CN, Candidate C, Ballot B, winners W, party P, Affiliated A
		WHERE N.name = N1.name
		AND N.NID = CN.NID
		AND CN.CID = C.CID
		AND C.CID = B.CID
		AND W.CID = C.CID
		AND A.CID = C.CID
		AND A.PID = P.PID
		GROUP BY N.name) > 1
AND N1.NID = CN1.NID
AND CN1.CID = C1.CID
AND C1.CID = B1.CID
AND W1.CID = C1.CID
AND A1.CID = C1.CID
AND A1.PID = P1.PID



-- HERE!!
SELECT C.year, C.CID, N.name, B.electoral, B.popular, B.polls, W.ISA, P.P_name
FROM Nominee N, Cand_Nom CN, Candidate C, Ballot B, winners W, Affiliated A, Party P,

	(SELECT Nominee.name
	FROM Nominee
	WHERE (SELECT count(DISTINCT(P.P_name))
			FROM Nominee N, Cand_Nom CN, Candidate C, Ballot B, winners W, party P, Affiliated A
			WHERE N.name = Nominee.name
			AND N.NID = CN.NID
			AND CN.CID = C.CID
			AND C.CID = B.CID
			AND W.CID = C.CID
			AND A.CID = C.CID
			AND A.PID = P.PID
			GROUP BY N.name) > 1) swing

WHERE N.name = swing.name
AND N.NID = CN.NID
AND CN.CID = C.CID
AND C.CID = B.CID
AND W.CID = C.CID
AND A.CID = C.CID
AND A.PID = P.PID

-- MODE 5 --> party
-- This query should return the results of a party throughout the history of the elections. Along
-- with it, some statistics about the performance of the party wins/loses, electoral votes
-- each time. 

SELECT P.P_name, count(DISTINCT(C.CID)) as num_candidates,SUM(B.popular) as popular, SUM(B.electoral) as electoral, SUM(W.ISA) as wins
FROM Nominee N, Cand_Nom CN, Candidate C, Ballot B, winners W, party P, Affiliated A
WHERE P.P_name = 'Republican'
AND N.NID = CN.NID
AND CN.CID = C.CID
AND C.CID = B.CID
AND W.CID = C.CID
AND A.CID = C.CID
AND A.PID = P.PID
GROUP BY P.P_name


-- MODE 6 --> year
-- given a specific year this query will return the campaigns details of that year

SELECT N.name, C.year, CP.expenses, CP.CONTRIB, CP.SLOGAN
FROM Nominee N, Cand_Nom CN, Candidate C, Campaign CP
WHERE CN.NID = N.NID
AND CN.CID = C.CID
AND C.year = 2008
AND CP.CID = C.CID


-- MODE 7 --> candidate
-- returns vice president of that candidate
SELECT C.year, N.name, V.V_Name
FROM Nominee N, Cand_Nom CN, Candidate C, Vice V
WHERE N.name = 'Barack H. Obama'
AND N.NID = CN.NID
AND CN.CID = C.CID
AND V.CID = C.CID

-- MODE 8 --> no input
-- state to number of presidents

SELECT p.homestate, DISTINCT(p.name) as num_presidents
FROM president p
GROUP BY p.homestate

-- MODE 9 --> no input
-- shows data collected about presidents
SELECT p.name, p.dob, p.birthplace, p.homestate FROM president p












