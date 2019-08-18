import os, traceback
from tkinter import *
from tkinter import ttk

window = Tk()
currentFileName = "Start"

LIST_UID = 0
ITEM_UID = 1
HEIGHT = 500
WIDTH = 800

class Checkitem:

	def __init__(self, line, complete):
		self.complete = complete
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

	def __init__(self, name):
		self.checklist = []
		self.name = name

	def addItem(self, text, complete):
		self.checklist.append(Checkitem(text, complete))

	def addList(self, text):
		self.checklist.append(Checklist(text))

	def remove(self, num):
		try:
			self.checklist.pop(num - 1)
		except:
			print("Invalid index", num, "into", self.name)

	def getName(self):
		return self.name

	def getList(self):
		return self.checklist


masterlist = Checklist("INIT")

# ------------ SERVER ------------ #


def serverOpenFile(fileName):

	f = 0

	try:
		globals()['currentFileName'] = fileName.lstrip("../checklists/")
		f = [line.rstrip('\n') for line in open(fileName)]
		serverReadFile(f, globals()['masterlist'], 0)
	except:
		print("Unable to read file", fileName)
		traceback.print_exc()



def serverReadFile(text, curList, index):

	while index < len(text):
		line = text[index]
		index += 1
		if line.strip() == "":
			continue
		elif("<LS>" in line):
			curList.addList(line[5:])
			index = serverReadFile(text, curList.getList()[-1], index)
		elif("<LE>" in line):
			return index
		elif("<IT>" in line):
			curList.addItem(line[5:].strip(), True)
		elif("<IF>" in line):
			curList.addItem(line[5:].strip(), False)
		else:
			return index

	clientMenu()


def serverExport(fileName):

	f = open("../checklists/" + fileName, "w")

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

	masterlist[int(usr)-1].add(newitem, False)



def addList():
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
	print("\n-------------- Export --------------\n")

	usr = input("What would you like to name the new file? ")

	serverExport(usr)

def load():

	print("\n-------------- Load --------------\n")

	checkdir = os.listdir("../checklists")

	i = 1
	for file in checkdir:
		print('[' + str(i) + ']', file)
		i += 1
	print(" ")

	usr = int(input("What is the number of the file would you like to open? "))

	serverOpenFile("../checklists/" + checkdir[usr - 1])


def show():

	print("\n-------------- Show --------------\n")

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

	usrList = masterlist[int(usr) - 1].getList()

	print(" ")
	if(usr.isdigit() == True):
		for listItem in usrList:
			print(listItem.getFormat())


def add():

	func = {
		"c" : addList,
		"i" : addItem,
	}

	usr = input("Add a Checklist (c) or an Item (i) or Quit (q)? ").lower()

	if(not usr == "q"):
		func[usr]()


def takeInput():


	print("\n---------- Menu ----------\n")


	usr = input("Add (a), Remove (r), Show (s), Export (e), Load (l), or Quit (q)? ").lower()




def clientAddMenu():

	menu = Tk()

	lbl = Label(menu, text="What would you like to add?")

	btn1 = Button(menu, text="List", command=addList)
	btn2 = Button(menu, text="Item", command=addItem)

def clientWindow():

	window.title("Check Recursion")
	window.geometry(str(WIDTH) + 'x' + str(HEIGHT))


def clientClearScreen():
	a = window.winfo_children()
	for widget in a:
		b = widget.winfo_class()
		if "Treeview" == b:
			for i in widget.get_children():
				widget.delete(i)
		widget.destroy()


	globals()['LIST_UID'] = 0
	globals()['ITEM_UID'] = 1

def clientLoadFile():

	clientClearScreen()
	globals()['masterlist'] = Checklist("INIT")
	globals()['LIST_UID'] = 0
	globals()['ITEM_UID'] = 1

	fileLoc = "../checklists/"
	checkdir = os.listdir(fileLoc)

	v = IntVar()
	i = 0

	lbl = Label(window, text="What file would you like to open?")
	lbl.grid(column=0, row=0)

	for file in checkdir:
		Radiobutton(window, text=file, variable=v, value=i).grid(row=i+1, sticky=W)
		i += 1



	submit = Button(window, text="Submit", command=lambda: serverOpenFile(fileLoc + checkdir[v.get()])).grid(sticky=SW)

def serverLoadTree(tree, curList, curListUID, curItemUID):

	for lst in curList.getList():
		if type(lst) is Checklist:
			tree.insert(curListUID, 'end', curItemUID, text=lst.getName())
			curItemUID = serverLoadTree(tree, lst, curItemUID, curItemUID + 1)
		elif type(lst) is Checkitem:
			tree.insert(curListUID, 'end', curItemUID, text=lst.getFormat())
			curItemUID += 1

	globals()['LIST_UID'] = curItemUID
	globals()['ITEM_UID'] = curItemUID

	return curItemUID

def clientShowLists(frame):

	tree = ttk.Treeview(frame)

	i = -1

	curListUID = globals()['LIST_UID']
	curItemUID = globals()['ITEM_UID']

	tree.insert("", 'end', 0, text="Start")

	serverLoadTree(tree, masterlist, curListUID, curItemUID)


	tree.pack(fill=BOTH, expand=TRUE)


def clientMenu():

	clientClearScreen()


	# Setting up frames
	top = Frame(window, bg='#F00', height=40)
	top.pack(fill=X, side=TOP)
	bot = Frame(window, bg='#00F', height=40)
	bot.pack(fill=X, side=BOTTOM)
	#mid = Frame(window, bg='#0F0', height=500, width=500)
	#mid.pack(fill=X, side=LEFT)


	# Top
	lbl = Label(top, text=globals()['currentFileName'], font='Helvetica 16 bold', bg='#FF0')
	lbl.grid(column=0, row=0)

	# Middle

	clientShowLists(window)

	# Bottom

	# buttons = ["Add Item", "Delete Item", "Save File", "Load New File"]
	# functions = []
	lines = ["Load", "Menu", "Add"]
	functions = [clientLoadFile, clientMenu, clientAddMenu]
	for i in range(len(lines)):
		Button(bot, text=lines[i], command=functions[i]).grid(column=i, row=0)

def main():

	clientLoadFile()
	clientWindow()
	window.mainloop()


if __name__ == "__main__":
	main()
