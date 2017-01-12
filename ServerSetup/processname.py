#!/Users/mannycrespi/anaconda2/bin/python

import cgi
import PCDmappings
from html import HTML 

#server debug
import cgitb
cgitb.enable(display=0, logdir="/path/to/logdir")


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

def dropDownTop():
	print("""<h1>PCD Database</h1>
	    <form action="displayTable.cgi">
	    <br>
            
	       <fieldset>
	          <legend>Please Query the Following Options</legend>
	          <p>
	             <label class="modelabel" for="modetype">Mode</label>
	             <select name="mode" id = "MODE">
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
	dropMenu("Year",list)		#setYear()
		
	list = PCDmappings.getCandidates()
	dropMenu("Candidate", list) #setCandidate()
		
	list = PCDmappings.getParties()
	dropMenu("Party", list)		#setParty()

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
		dropDownTail()
		################ end drop down menus ########
		htmlTail()			
		################ end body ###################	
	except:
		cgi.print_exception()
