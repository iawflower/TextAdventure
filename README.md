TextAdventure
=============

This python code implements a framework for a Text Adventure.

Objects and Rooms:
	The base classes in this framework are Objects, which represent things in the game you can interact with, and Rooms, which represent housings for these objects.
	Individual objects are implemented as subclasses of the Object type, which allows them to inherit general properties, while still having object-unique behavior.
	Rooms are also implemented as subclasses, allowing for room-unique behavior, including commands that are associated with specific rooms.
	
Command parsing:
	Player commands are parsed by looking for keywords and ignoring everything else. This can create some powerful, and some counter-intuitive behavior.
	For example, imagine you want to allow the play go through a door into a closet. Then, depending on which keywords you use, the following could all trigger the event:
		"Enter closet"
		"Enter the closet"
		"Go through closet door"
		"Go into the closet"
		"Use closet door"
		"Use closet"
		"Do not go into the closet"
		"Run away from closet door enterance" [sic]
	This is based on the assumption that players are more likely to use positive commands than negative ones. If they do, they will find counter-intuitive behavior, which is
	unfortunate, but a byproduct of this method.
	
Right now, objects can interact with each other by adding the names of each object to the other's dictionary or interactions, but I would like to make this easier, and more
intuitive to code.

For that matter, I'm also working on creating a better method of adding interactions to objects, so that adding new interactions will be more intuitive.