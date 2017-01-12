#!/Users/mannycrespi/anaconda2/bin/python2

import cgi
import PCDmappings
#import HTML 

#server debug
#import cgitb
#cgitb.enable(display=0, logdir="/path/to/logdir")


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

#meant to be called after dropDownTop
def dropMenu(title,list):
	#Sub categrory for a Query
	print("""<legend type='hidden'>""")
	#Sub Category title for 
	print("""</legend>
	           <p>
	              <label>""")
	print(title)
	print("""</label>""")
	print("""<select name = """)
	print("\""+title+"\" ")
	print("id = ")
	print(title.upper()+">")

	#enumerate the list into formatted options
	options = ""
	for i in range (0,len(list)):
		options += "<option value = \""+list[i]+"\">"+list[i]+"</option>\n"
	print(options)
	print("""</select>
	           </p>""")   
	              
def getData():
	formData = cgi.FieldStorage()
	firstname = formData.getvalue('firstname')
	return firstname



#sets up button to react to func call
def reactToInput(name):
	print("<form action=")
	print(name)
	print("""method="get">
	  <input type="button" value="Click me" onclick="printTable()">
		</form>""")

def scriptHead():
	print("""<script>""")

def scriptTail():
	print("""</script>""")

def func():
	#modify info to get different outputs
	info = "mode"

	#declare globals here
	print("""function printTable() {
			    window.alert(""")

	print(info)
	print(""");}""")


def setYearHTMLfunc():
	#declare globals here
	print("""function setYear() {
			    alert("year is ");}""")

def refresh():
	print("""<h1>PCD Database (1789-2016)</h1>
	    <form action="processname.cgi">
	    <br>
            
	       <fieldset>
	          <legend>Click this to refresh.</legend>
	          """)
	print("""<input type="submit" value="Refresh"/>""")
	print("""	</fieldset>
    </form>""")

def dropDownTop():
	print("""<h1>PCD Database (1789-2016)</h1>
	    <form action="displayTable.cgi">
	    <br>
            
	       <fieldset>
	          <legend>Please Query the Following Options</legend>
	          <p>
	             <label class="modelabel" for="modetype">Mode</label>
	             <select name="mode" id = "MODE">
	               <option value = "0">---</option>
	               <option value = "1">one</option>
	               <option value = "2">two</option>
	               <option value = "3">three</option>
	               <option value = "4">four</option>
	               <option value = "5">five</option>
	               <option value = "6">six</option>
	               <option value = "7">seven</option>
	               <option value = "8">eight</option>
	               <option value = "9">nine</option>
	             </select>
	          </p>""")
	list = PCDmappings.get_election_years()
	dropMenu("Year",["---"]+list)		#setYear()
		
	list = PCDmappings.getCandidates()
	dropMenu("Candidate",["---"]+list) #setCandidate()
		
	list = PCDmappings.getParties()
	dropMenu("Party", ["---"]+list)		#setParty()

def dropDownTail():
	print("""	</fieldset>
    </form>""")

#main program
if __name__ == "__main__":
	try:
		################ begin body #################
		htmlTop()			
		################ start drop down menus ######
		dropDownTop()
		print("""<input type="submit" value="Submit"/>""")
		print("""<p>
	          MODE 1: Select a year for info on that election.
	          </p>""")
		print("""<p>
	          MODE 2: Select a canidate for info relating to that candidate.
	          </p>""")
		print("""<p>
	          MODE 3: Click 'Submit' for details on re-lected non-contiguous candidates
	          </p>""")
		print("""<p>
	          MODE 4: Click 'Submit' for details on swing candidates.
	          </p>""")
		print("""<p>
	          MODE 5: Select a party for info on that party
	          </p>""")
		print("""<p>
	          MODE 6: Select a year for campaign details on that year
	          </p>""")
		print("""<p>
	          MODE 7: Select a candidate for info on his vice president(s) 
	          </p>""")
		print("""<p>
	          MODE 8: Click 'Submit' for table of states to number of presidents.
	          </p>""")
		print("""<p>
	          MODE 9: Click 'Submit' for details on all presidents. 
	          </p>""")
		dropDownTail()
		################ end drop down menus ########
		htmlTail()			
		################ end body ###################	
	except:
		print("<p>")
		print("SOMETHING WENT WRONG!")
		print("</p>")
		refresh()
		cgi.print_exception()
