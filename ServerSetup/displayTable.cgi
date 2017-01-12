#!/Users/mannycrespi/anaconda2/bin/python2
import MySQLdb
import cgi
#import HTML

#server debug
#import cgitb
#cgitb.enable(display=0, logdir="/path/to/logdir")

server = "PCD_424.local"
user = "root"
passwd = "basketball"
DB = "PCD_Database"

def goBack():
	print("""<h1>PCD Database (1789-2016)</h1>
	    <form action="processname.cgi">
	    <br>
            
	       <fieldset>
	          <legend>Click this to go back.</legend>
	          """)
	print("""<input type="submit" value="Go Back"/>""")
	print("""	</fieldset>
    </form>""")


def theQuery(db,query):
	cursor = db.cursor()
	cursor.execute(query)
	#h = HTML()
	results = cursor.fetchall()
	info = cursor.description
	length = len(results)
	width = len(results[0])

	print("<table border=\"1\">")
	print("<tr>")
	for i in range(0,width):
		print("<th>")
		print(info[i][0])
		print("</th>")
	print("</tr>")

	for row in results:
		print("<tr>")
		for i in row:
			print("<td>")
			print(i)
			print("</td>")		
		print("</tr>")
	print("</table>")

def htmlTop():
	print ("""Content-type:text/html\n\n
		<!DOCTYPE html>
		<html lang="en">
			<head>
				<meta charset="utf-8"/>
				<title>My server side template</title>
			</head>
			<body>""")

def htmlTail():
	print("""	</body>
		</html>""")

def getData(d):
	formData = cgi.FieldStorage()
	data = formData.getvalue(d)
	return data

#main program
if __name__ == "__main__":
	db = MySQLdb.connect(server,user,passwd,DB)
	mode = ""
	candidate = ""
	party = ""
	year = ""

	try:
		htmlTop()
		mode = getData('mode')
		cand = getData('Candidate')
		party = getData('Party')
		year = getData('Year')
		
		query1 = """SELECT C.year, C.CID, P.P_name, N.name, B.electoral, W.ISA
				FROM Nominee N, Cand_Nom CN, Candidate C, Ballot B, winners W, party P, Affiliated A
				WHERE C.year = """+year+"""
				AND N.NID = CN.NID
				AND CN.CID = C.CID
				AND C.CID = B.CID
				AND W.CID = C.CID
				AND A.CID = C.CID
				AND A.PID = P.PID			
				;"""

		query2 = """SELECT C.year, p.p_name, N.name, B.electoral, B.popular, B.polls, W.ISA
				FROM Nominee N, Cand_Nom CN, Candidate C, Ballot B, winners W, party p, Affiliated A
				WHERE N.name = \'"""+cand+"""\'
				AND N.NID = CN.NID
				AND CN.CID = C.CID
				AND C.CID = B.CID
				AND W.CID = C.CID
				AND A.CID = C.CID
				AND A.PID = P.PID
		;"""

		query3 = """SELECT name 
					FROM president 
					WHERE inoffice like '%/%';   
		;"""

		query4 = """SELECT C.year, N.name, B.electoral, B.popular, B.polls, W.ISA, P.P_name
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
		;"""

		query5 = """SELECT P.p_name, count(DISTINCT(C.CID)) as num_candidates,SUM(B.popular) as popular, SUM(B.electoral) as electoral, SUM(W.ISA) as wins
					FROM Nominee N, Cand_Nom CN, Candidate C, Ballot B, winners W, party P, Affiliated A
					WHERE N.NID = CN.NID
					AND CN.CID = C.CID
					AND C.CID = B.CID
					AND W.CID = C.CID
					AND A.CID = C.CID
					AND A.PID = P.PID
					AND P.p_name = \'"""+party+"""\'
					GROUP BY P.P_name
		;"""

		query6 = """SELECT N.name, C.year, CP.expenses, CP.CONTRIB, CP.SLOGAN
					FROM Nominee N, Cand_Nom CN, Candidate C, Campaign CP
					WHERE CN.NID = N.NID
					AND CN.CID = C.CID
					AND C.year = """+year+"""
					AND CP.CID = C.CID
		;"""

		query7 = """SELECT C.year, N.name, V.V_Name
					FROM Nominee N, Cand_Nom CN, Candidate C, Vice V
					WHERE N.name = \'"""+cand+"""\'
					AND N.NID = CN.NID
					AND CN.CID = C.CID
					AND V.CID = C.CID
		;"""

		query8 = """SELECT p.homestate, count(DISTINCT(p.name)) as num_presidents
					FROM president p
					GROUP BY p.homestate
		;"""

		query9 = """SELECT p.name, p.dob, p.birthplace, p.homestate FROM president p
		;"""

		################# DEBUG ######################
		#print("\nMODE: " + mode)
		#print("\nYEAR: " + year)
		#print("\nCANDIDATE: " + cand)
		#print("\nPARTY: " + party)
		##############################################
		if(mode == "0"):
			print("PLEASE SELECT A MODE")
		else:
			if mode == "1":
				if(year == "---"):
					print("PLEASE SELECT A YEAR")
				else:
					theQuery(db,query1)
			if mode == "2":
				if(cand == "---"):
					print("PLEASE SELECT A CANDIDATE")
				elif(cand == "Dwight D. Eisenhower"):
					theQuery(db,query2)
					print("<img src=\"https://mises.org/sites/default/files/styles/slideshow/public/static-page/img/ILikeIke.jpg?itok=I7nFblMX\"></img>")
				elif(cand == "Donald J. Trump"):
					theQuery(db,query2)
					print("<img src=\"http://abovethelaw.com/wp-content/uploads/2016/04/cartoon-trump-300x316.jpg\"></img>")
				elif(cand == "Barack H. Obama"):
					theQuery(db,query2)
					print("<img src=\"https://s-media-cache-ak0.pinimg.com/originals/81/1e/94/811e94942992fa90d821a6666736720e.jpg\"></img>")
				elif(cand == "Theodore Roosevelt"):
					theQuery(db,query2)
					print("<img src=\"http://images.mentalfloss.com/sites/default/files/styles/article_640x430/public/like-a-boss-e1350189178780_6.jpg\"></img>")
				elif(cand == "Abraham Lincoln"):
					theQuery(db,query2)
					print("<img src=\"https://s-media-cache-ak0.pinimg.com/originals/64/f1/98/64f198be4fa8447e01092fb894a23bbd.jpg\"></img>")
				else:
					theQuery(db,query2)
			if mode == "3":
				theQuery(db,query3)
			if mode == "4":
				theQuery(db,query4)
			if mode == "5":
				if(party == "---"):
					print("PLEASE SELECT A PARTY")
				else: 
					theQuery(db,query5)
			if mode == "6":
				if(year == "---"):
					print("PLEASE SELECT A YEAR")
				else:
					theQuery(db,query6)
			if mode == "7":
				if(cand == "---"):
					print("PLEASE SELECT A CANDIDATE")
				else:
					theQuery(db,query7)
			if mode == "8":
				theQuery(db,query8)
			if mode == "9":
				theQuery(db,query9)

		goBack()
		htmlTail()
		db.close()
	except:
		print("<p>")
		print("SOMETHING WENT WRONG!")
		print("</p>")
		goBack()
		cgi.print_exception()
