masterlist = []


class Checkitem:
	
	complete = False
	line = ""

	def __init__(self, line):
		self.line = line

	def check(self):
		self.complete = True

	def uncheck(self):
		self.complete = False

	def modify(self, line):
		self.line = line

	def getLine(self):
		return self.line

	def getFormat(self):
		if(self.complete == True):
			start = "[x] "
		else:
			start = "[ ] "

		return start + self.line

class Checklist:
	
	name = ""
	checklist = []

	def	__init__(self, name):
		self.name = name

	def add(self, text):
		self.checklist.append(Checkitem(text))

	def remove(self, num):
		try:
			checklist.pop(num - 1)
		except:
			print("Invalid index", num, "into", name)
	
	def getName(self):
		return self.name

	def getList(self):
		return self.checklist

# FILE IO #


def loadText(fileName):
	
	f = 0

	try:
		f = open(fileName, "r")
	except:
		print("Unknown File: ", fileName)
		return

	i = -1

	for line in f:
		if(not line[0] == '[' and line):
			masterlist.append(Checklist(line.strip()))
			i += 1
		else:
			masterlist[i].add(line[4:].strip())



def exportText(fileName):

	f = open(fileName, "w")
	
	for checklist in masterlist:
		f.write(checklist.getName() + '\n')
		for line in checklist.getList():
			f.write(line.getFormat()+ '\n')


def addItem():

	i = 1
	for checklist in masterlist:
		print("[" + str(i) + "]", checklist.getName())
		i += 1

	usr = input("\nTo which checklist do you want to add? ")

	
	bad = True

	while(bad == True):

		bad = False

		if(usr.isdigit() == True):
			if(int(usr) > len(masterlist) or int(usr) < 1):
				usr = input("Please choose a valid number: ")
				bad = True
		
		elif(not usr == "q" and not usr == "Q"):	
			usr = input("Invalid Input. Try Again: ")
			bad = True		

	
	bad = True

	while(bad == True):
		newitem = input("What would you like to add? ")

		verify = input("Are you sure? (y/n): ").lower()

		if(verify == "y"):
			bad = False

	masterlist[int(usr)-1].add(newitem)



def addChecklist():
	usr = input("What is the name of the new checklist? ").lower()

	bad = True
	while(bad == True):

		bad = False
	
		if(usr == "q" or usr == "quit"):
			return
		else:
			for checklist in masterlist:
				if usr == checklist.getName().lower():
					bad = True
					usr = input("Name Exists- Please enter a new name: ")		

	masterlist.append(Checklist(usr))


def export():

	usr = input("What would you like to name the new file?")

	exportText(usr)

def load():

	usr = input("What file would you like to open?")

	loadText(usr)

def show():

	i = 1			
	for list in masterlist:
		print('[' + str(i) + ']', list.getName())
		i += 1

	print("\n[q] Quit \n")

	usr = input("Input List Number: ")
	
	bad = True
	while(bad == True):
		if(usr.isdigit() == True):
			if(int(usr) > len(masterlist) or int(usr) < 1):
				usr = input("Please choose a valid number: ")
		
		elif(not usr == "q" and not usr == "Q"):	
			usr = input("Invalid Input. Try Again: ")
		
		bad = False

	if(usr.isdigit() == True):
		for listItem in masterlist[int(usr)-1].getList():
			print(listItem.getFormat())



def add():
	
	func = {
		"c" : addChecklist,
		"i" : addItem,
	}

	usr = input("Add a Checklist (c) or an Item (i) or Quit (q)? ").lower()

	if(not usr == "q"):
		func[usr]()
	


def rem():
	return 2




def takeInput():
	
	func = {
		"a" : add,  "r" : rem,
		"s" : show, "e" : export,
		"l" : load, "q" : exit
	}

	usr = input("Add (a), Remove (r), Show (s), Export (e), Load (l), or Quit (q)? ").lower()
	
	func[usr]()





def main():

	while(0 == 0):
		ret = takeInput()		
	print("Finished")


if __name__ == "__main__":
	main()	
	

	
