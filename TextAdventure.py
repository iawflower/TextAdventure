#
#	The Player class is a collections of methods designed to represent the player's interactions. It includes more of the i/o information, as well
#	as methods for interacting with the inventory, list of actions done, and location.
#

class Player:
	def __init__(self):
		self.actionsDone = []	# List of actions performed so far. Unaccessable by the player, this list just helps the game figure out what you've done so far.
								# Note that this is a list of strings, so spelling matters!
	
	def hasItem(self,item): # Checks the requested item name against the items in the inventory. Note that it uses the string type names associated with each object.
		tempbool = False
		for x in inventory.objects:
			if x.name == item.name:
				tempbool = True
		return tempbool
	
	def hasDone(self,action): # Checks if the player has done that particular action yet.
		return (action in self.actionsDone)
	
	def addDone(self,done): # Adds a string to the list of actions done.
		if (done not in self.actionsDone):
			self.actionsDone.append(done)
			
	def delDone(self,done): # Removes a given string from the list of actions done.
		if (done in self.actionsDone):
			self.actionsDone.remove(done)
	
	def printInventory(self): # Prints out the inventory, using the item name strings. The player can access this list whenever they need to during the game.
		for x in inventory.objects:
			print (x.name)
	
	def printDone(self): # Prints the list of actions done. Used for debugging, not intended to be accessible by player.
		print (self.actionsDone)
	
	# Location is a property of the Player class object. It provides access to the room that the player currently resides in.
	def setLoc(self,place):
		self._location = place
	
	def getLoc(self):
		return self._location
	
	location = property(getLoc,setLoc)
	
	#
	#	Prompt is the most important function in this framework. It asks the player for an input string, and then uses that to determine
	#	what action they are trying to perform. It works by looking for possibilities in this order:
	#		1. Checks it the command in its entirety is one of a few "general commands." If so, it simply executes that command.
	#		2. Checks if the command in its entirety is in the list of "override commands" for the room the player is in. If so, it simply executes that command.
	#		3. Otherwise, it scans the command looking for the names of objects either in the player's inventory of in the room they are in.
	#			a. If it finds an object, it checks if any keywords associated with that object are in the command. If so, it executes the command associated with that keyword.
	#		4. If it hasn't yet done something, it responds "I don't understand."
	#	Finally, it calls itself again, to ask the player for another input.
	#
	def prompt(self):
		# Gets input.
		command = input(">>  ")
		command = command.lower() # makes it lower case to match names
		here = self.location
		# Checks if the command is one of the "general commands."
		if command == "inventory":
			self.printInventory()
		elif command == "look around":
			here.visited = False
			here.enter()
		elif command == "actions":
			self.printDone()
		# Checks if the command is one of the "override commands" for the room.
		elif command in here.overrides:
			here.overrides[command]()
		else: 
			# Looks for object names.
			objectfound = 0
			commandstring = command.partition(" ")
			while (commandstring[0] != "") and objectfound == 0:
				for object in here.objects:
					if commandstring[0] == object.name:
						objectfound = object
				for object in inventory.objects:
					if commandstring[0] == object.name:
						objectfound = object
				commandstring = commandstring[2].partition(" ")
			# If it finds one, calls performAction, which will evaluate for commands.
			if objectfound != 0:
				self.performAction(here,objectfound,command)
			# If no object found, and no commands matched above, returns "I don't understand."
			else:
				print ("I don't understand.")
		# Reexecutes the prompt.
		self.prompt()
			
	#
	#	
	#
	def performAction(self,location,object,command):
		for x in object.interacts:
			if x in command:
				object.interacts[x]()
				break


#
#	Objects are things you can directly interact with, and are designed to be called by name in a command.
#	Each object keeps track of which room it is in, which includes the player's inventory.
#	An object's most important feature is its list of interactions, which is stored as a dictionary.
#	Each object in the game is initiated as a subclass of the object class, which gives it the initialization it needs.
#				
class object:						# When created, it requires two arguments: the room it should be created in, and the name it should be called by.
	def __init__(self,room,text):	# Subclasses shouldn't override this unless absolutely necessary.
		room.addObject(self)		# Uses the room init argument, adds itself to that room.
		self.name = text			# Saves the name given.
		self.here = room			# Saves currently location.
		self.interacts = {}			# Dictionary of interactions.
		
		#
		#	The dictionary of interactions works as a dispatch table. It stores function calls as the entries, and uses keywords as the entry titles.
		#	Each object will have, inherently, the interactions listed below, but they need to have the functions defined on a per object basis, or
		#	they will default to the boring versions given here.
		#
		self.addInteracts()
	
	#
	#	In order to define new interactions, each object should redefine the addInteracts(self) function, adding new entries to the interacts dictionary.
	#	For example: self.interacts["new action"] = self.doSomething
	#	and then, later in the subclass definition, doSomething(self) must be defined.
	#
	
	def addInteracts(self):
		{}
	
	# Allows the object to be moved around. Moving to inventory gives the item to the player. There is also a room called storage where objects can be placed temporarily.
	def move(self,room):
		self.here.removeObject(self)
		room.addObject(self)

#
#	Rooms are places you, and objects, can reside in. They keep track of which objects are in them, and also a dictionary of override commands that can
#	be called in just that room. These override commands are defined the exact same way as object interactions, using function calls and dictionary entries.
#	They also feature an "enter" method, which does a few things.
#		It places the player into that room.
#		First, it can perform any special behaviors defined in the enterSpecial(self) method for that object.
#		Second, it prints a message associated with that room. If player is entering the room for the first time, it prints a detailed description of the room.
#			otherwise, it prints a simple description.
#
class Room:
	def __init__(self):
		self.objects = []
		self.overrides = {}
		self.addOverrides()
		self.visited = False
	
	def addObject(self,object):
		self.objects.append(object)
		
	def removeObject(self,object):
		self.objects.remove(object)
	
	def printDesc(self):
		print("\nGeneric room with no description")
		
	def printDet(self):
		print("\nDetailed description of generic room")
		
	def enterSpecial(self):
		{}
	
	def enter(self):
		self.enterSpecial()
		if (self.visited):
			self.printDesc()
		else:
			self.printDet()
			self.visited = True
		player.location = self
	
	def addOverrides(self):
		{}


player = Player()		#	Player class.
inventory = Room()		#	Player's inventory.
storage = Room()		#	Void storage for objects that are out of use.

###########################
#
#	Rooms in the game
#
###########################
class entrance(Room):
	def printDesc(self):
		print("You are in the enterance hall.")
		
	def printDet(self):
		print("An uninteresting entrance hall. You wonder what's going on. There is a closet. There is a dark corner. What would you like to do?")
		if ("sang" in player.actionsDone):
			print ("You can hear the echoes of your song.")
			
	def addOverrides(self):
		self.overrides["sing"] = self.sing
		
	def sing(self):
		print("Sounded beautiful.")
		player.addDone("sang")	
entrance = entrance()

class closet(Room):
	def printDet(self):
		print("It's a dark and musty closet. There are jackets everywhere.")
		if	(batteries in self.objects):
			print ("In one of the jacket pockets, there are batteries.")
	
	def printDesc(self):
		print("\nYou are in the closet.")
		
	def addOverrides(self):
		self.overrides["leave"] = self.leave
		self.overrides["exit"] = self.leave
		self.overrides["go"] = self.leave
		self.overrides["back"] = self.leave
		self.overrides["go back"] = self.leave
		
	def leave(self):
		entrance.enter()
closet = closet()

###########################
#
#	Objects in Entrance
#
###########################
class flashlight(object):
	def addInteracts(self):
		self.interacts["inspect"] = self.inspect
		self.interacts["take"] = self.take
		self.interacts["pick up"] = self.take
		self.interacts["batteries"] = self.batteries
		
	def take(self):
		print("You picked up a flashlight. Missing its batteries, though.")
		self.move(inventory)
		
	def inspect(self):
		if("flashlight charged" in player.actionsDone):
			print("It's a normal flashlight.")
		else:
			print("It's a normal flashlight. Missing its batteries, though.")
			
	def batteries(self):
		if player.hasItem(batteries):
			batteries.move(storage)
			player.addDone("flashlight charged")
		else:
			print ("I don't understand.")
flashlight = flashlight(entrance,"flashlight")


class lamp(object):
	def inspect(self):
		print("It's a non-descript lamp. It dimly illuminates the room, but plenty of shadows remain.")
		player.addDone("inspected lamp")
lamp = lamp(entrance,"lamp")


class corner(object):
	def addInteracts(self):
		self.interacts["illuminate"] = self.light
		self.interacts["light"] = self.light
		
	def light(self):
		if (not player.hasItem(flashlight)):
			print("You don't have a flashlight")
		elif (not player.hasDone("flashlight charged")):
			print("Your flashlight is dead.")
		else:
			print("You illuminate the corner with your flashlight. Cowering there is a scared cat. It hisses.")
			player.addDone("illuminated corner")
corner = corner(entrance,"corner")


class closetdoor(object):
	def addInteracts(self):
		self.interacts["enter"] = self.gothrough
		self.interacts["use"] = self.gothrough
		
	def gothrough(self):
		closet.enter()
closetdoor = closetdoor(entrance,"closet")


###########################
#
#	Objects in Closet
#
###########################
class batteries(object):
	def addInteracts(self):
		self.interacts["inspect"] = self.inspect
		self.interacts["take"] = self.take
		self.interacts["pick up"] = self.take
		self.interacts["flashlight"] = self.flashlight
		
	def take(self):
		print("You've acquired batteries.")
		self.move(inventory)
		
	def inspect(self):
		print("D-type batteries. Perfect for a flashlight.")
		
	def flashlight(self):
		if player.hasItem(flashlight):
			self.move(storage)
			player.addDone("flashlight charged")
		else:
			print ("I don't understand.")
			
batteries = batteries(closet,"batteries")



entrance.enter()	#	Places the player in the entrance.
player.prompt()		#	Initiates the first prompt command. The game is afoot!
