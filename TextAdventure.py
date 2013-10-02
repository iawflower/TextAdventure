class Player:
	def __init__(self):
		self.actionsDone = []
	
	def hasItem(self,item):
		tempbool = False
		for x in inventory.objects:
			if x.name == item.name:
				tempbool = True
		return tempbool
	
	def addDone(self,done):
		if (done != "null") and (done not in self.actionsDone):
			self.actionsDone.append(done)
			
	def delDone(self,done):
		if (done != "null"):
			self.actionsDone.remove(done)
	
	def printInventory(self):
		for x in inventory.objects:
			print (x.name)
	
	def printDone(self):
		print (self.actionsDone)
	
	def move(self,place):
		if (place != "null"):
			place.enter(self)
	
	def setLoc(self,place):
		self._location = place
	
	def getLoc(self):
		return self._location
	
	location = property(getLoc,setLoc)
	
	def prompt(self):
		command = input(">>  ")
		self.interpret(command)
		
	def interpret(self,command):
		command = command.lower()
		here = self.location
		if command == "inventory":
			self.printInventory()
		elif command == "look around":
			here.visited = False
			here.enter(self)
		elif command == "actions":
			self.printDone()
		elif command in here.actions:
			here.performOverride(command)
		else: 
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
			if objectfound != 0:
				self.performAction(here,objectfound,command)
			else:
				print ("I don't understand.")
		self.prompt()
			
		
	def performAction(self,location,object,command):
		action = []
		commandstring = command.partition(" ")
		for x in object.interacts:
			if x in command:
				action = object.interacts.get(x)
		if action != []:
			if (action[0] != "null") and (not self.hasItem(action[0])):
				print(action[1])
			elif (action[2] != "null") and (action[2] not in player.actionsDone):
				print(action[3])
			else:
				if (action[4] != "null"):
					print(action[4])
				if (action[5] != "null"):
					action[5].move(inventory)
				if (action[6] != "null"):
					action[6].move(storage)
				player.addDone(action[7])
				player.move(action[8])
		else:
			print ("I don't understand.")
		
class object:
	def __init__(self,room,text):
		room.addObject(self)
		self.interacts = {}
		self.name = text
		self.here = room
		
	def move(self,room):
		self.here.removeObject(self)
		room.addObject(self)
		
	def addInteract(self,strings,action):
		for string in strings:
			self.interacts[string] = action
		
	def setDesc(self,info):
		self._desc = info.capitalize()
	
	def readDesc(self):
		return self._desc
	
	desc = property(readDesc, setDesc)
	
class Room:
	def __init__(self):
		self.objects = []
		self.actions = {}
		self.condItem = {}
		self.condDone = {}
		self.visited = False

	def addObject(self,object):
		self.objects.append(object)
		
	def removeObject(self,object):
		self.objects.remove(object)
	
	def enter(self,player):
		if (self.visited):
			print (self.desc)
		else:
			print (self.det)
			self.visited = True
		for x in self.condItem:
			if x in player.inventory:
				print (self.condItem.get(x))
		for x in self.condDone:
			if x in player.actionsDone:
				print (self.condDone.get(x))
		player.location = self
		
	def performOverride(self,command):
		action = self.actions.get(command)
		if (action[0] != "null") and (not player.hasItem(action[0])):
			print(action[1])
		elif (action[2] != "null") and (action[2] not in player.actionsDone):
			print(action[3])
		else:
			if (action[4] != "null"):
				print(action[4])
			if (action[5] != "null"):
				action[5].move(inventory)
			if (action[6] != "null"):
				action[6].move(storage)
			player.addDone(action[7])
			player.move(action[8])
			
	def addAction(self,triggers,action):
		for trigger in triggers:
			self.actions[trigger] = action
	
	def setDesc(self,info):
		self._desc = info.capitalize()
	
	def readDesc(self):
		return self._desc
	
	desc = property(readDesc, setDesc)
	
	def setDet(self,info):
		self._det = info.capitalize()
	
	def readDet(self):
		return self._det
	
	det = property(readDet, setDet)
	
	def addCondItem(self,item,text):
		self.condItem[item] = text
		
	def addCondDone(self,done,text):
		self.condDone[done] = text
		
player = Player()
inventory = Room()
storage = Room()

vocalcords = object(inventory,"vocalcords")

entrance = Room()
entrance.setDet("An uninteresting entrance hall. You wonder what's going on. There is a closet. There is a dark corner. What would you like to do?")
entrance.setDesc("You are in the enterance hall.")
entrance.addCondDone("sang","You can hear the echoes of your song.")

closet = Room()
closet.setDet("It's a dark and musty closet. There are jackets everywhere.")
closet.setDesc("You are in the closet.")

flashlight = object(entrance,"flashlight")
flashlight.setDesc ("It's a normal flashlight.")
flashlight.addInteract(["take","pick up"],["null","null","null","null","You picked up a flashlight. Missing it's batteries, though.",flashlight,"null","null","null"])

batteries = object(closet,"batteries")
batteries.setDesc("D-type batteries. Perfect for a flashlight.")

flashlight.addInteract(["batteries"],[batteries,"You don't have any batteries.","null","null","You put the batteries in the flashlight.","null",batteries,"flashlight charged","null"])
###########################
#
#	Objects in Entrance
#
###########################
entrance.addAction(["sing"],[vocalcords,"Hah, with what vocal cords?","null","You're not experienced enough yet.","Sounded beautiful.","null","null","sang","null"])
lamp = object(entrance,"lamp")
lamp.addInteract(["look","examine","inspect"],["null","null","null","null","It's a non-descript lamp. Not very interesting.","null","null","inspected lamp","null"])
corner = object(entrance,"corner")
corner.addInteract(["illuminate","light"],[flashlight,"You don't have a flashlight.","flashlight charged","You're flashlight is dead","You illuminate the corner with your flashlight. Cowering there is a scared cat.","null","null","illuminated corner","null"])
closetdoor = object(entrance,"closet")
closetdoor.addInteract(["enter","use"],["null","null","null","null","null","null","null","null",closet])


###########################
#
#	Objects in Closet
#
###########################
closet.addAction(["exit","leave","return"],["null","null","null","null","null","null","null","null",entrance])
batteries = object(closet,"batteries")
batteries.addInteract("take",["null","null","null","null","You've acquired batteries.",batteries,"null","null","null"])

entrance.enter(player)
player.prompt()
