#Copyright 2005-2006 the PyGauntlet Team (See CREDITS for more info)
#http://code.google.com/p/pygauntlet/
#
#This file is part of PyGauntlet.
#
#PyGauntlet is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.
#
#Foobar is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with Foobar; if not, write to the Free Software
#Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


CHARACTERMOVEPRESS = 1
CHARACTERMOVERELEASE = 2
CHARACTERATTACKPRESS = 3
CHARACTERATTACKRELEASE = 4
CHARACTERMAGICPRESS = 5
CHARACTERMAGICRELEASE = 6
CHARACTEREXIT = 7
ITEMPICKUP = 8
DOOROPEN = 9
ADDPROJECTILE = 10
TICKEVENT = 11
DISPLAYTICKEVENT = 12
QUITEVENT = 13
TOGGLEFULLSCREENEVENT = 14
GAMEOVEREVENT = 15

ADDPLAYERCHARACTER = 17
CHARACTERMAGICATTACK = 18
ADDPLAYERCONTROLLER = 19
STARTGAMEEVENT = 20

class Event:

  def __init__ ( self ):
    pass

  def __str__ ( self ):
    return "Generic Event"


class TickEvent ( Event ):

  def __init__ ( self, pygameEvents=[] ):
    self.pygameEvents = pygameEvents

  def __str__ ( self ):
    return "CPU tick Event"


class DisplayTickEvent ( Event ):

  def __init__ ( self ):
    pass

  def __str__ ( self ):
    return "Display tick Event"


class QuitEvent ( Event ):

  def __init__ ( self ):
    pass

  def __str__ ( self ):
    return "Program quit Event"


class ToggleFullscreenEvent ( Event ):

  def __init__ ( self ):
    pass

  def __str__ ( self ):
    return "Toggle Fullscreen Event"


##\brief An event to start the game
##
##Inherits from Event to show that it is an event.
##Contains the necessary information to start the game.
class StartGameEvent ( Event ):

##\brief Constructor creates the event
##
##\param characters The list of persistant characters between levels
##\param immobile The list of immobiles in the current level
##\param mobiles The list of mobiles in the current level
##\return None
  def __init__ ( self, characters, immobiles, mobiles ):
    self.characters = characters
    self.immobiles = immobiles
    self.mobiles = mobiles

  def __str__ ( self ):
    return "Game start Event"


##\brief An event for game over
##
##Inherits from Event to show that it is an event.
##Contains the necessary information to end the game.
class GameOverEvent ( Event ):

##\brief Constructor creates the event
##
##\param None
##\return None
  def __init__ ( self ):
    pass

  def __str__ ( self ):
    return "Game over Event"


##\brief A character placement event
##
##This event occurs when a character is placed in a position (not moved)
##not currently used yet (use this when players are created mid-game)
class MobilePlaceEvent ( Event ):

##\brief Constructor creates the event
##
##\param character The character to be placed in the game
##\return None
  def __init__ ( self, mobile ):
    self.mobile = mobile

  def __str__ ( self ):
    return "Mobile place Event"


#This event occurs when a character is successfully moved
class CharacterMoveEvent ( Event ):

  def __init__ ( self, character, oldRect ):
    #We now move left/right before we move up/down when we move diagonally.
    #So, the oldRect is not an indicator of the true old position
    self.character = character
    self.oldRect = oldRect

  def __str__ ( self ):
    return "Character move Event (from %s to %s)" % \
                (self.oldRect.topleft,self.character.rect.topleft)


class CharacterCollisionEvent ( Event ):

  def __init__ ( self, character, collideObj=None ):
    self.character = character
    self.collideObj = collideObj

  def __str__ ( self ):
    return "Character collision Event (playerID = %d, position = [%d, %d])" % \
                (self.character.id, self.character.rect.topleft[0],\
                 self.character.rect.topleft[1])


#all of the following events are sent from the KeyboardController
class CharacterMovePress ( Event ):

  def __init__ ( self, characterID, direction ):
    self.characterID = characterID
    self.direction = direction

  def __str__ ( self ):
    return "Character move key-press   (playerID = %d, direction = %d)"% \
                (self.characterID, self.direction)


class CharacterMoveRelease ( Event ):

  def __init__ ( self, characterID, direction ):
    self.characterID = characterID
    self.direction = direction

  def __str__ ( self ):
    return "Character move key-release   (playerID = %d, direction = %d)"% \
                (self.characterID, self.direction)


class CharacterAttackPress ( Event ):

  def __init__ ( self, characterID ):
    self.characterID = characterID

  def __str__ ( self ):
    return "Character attack key-press   (playerID = %d)" % (self.characterID)


class CharacterAttackRelease ( Event ):

  def __init__ ( self, characterID ):
    self.characterID = characterID

  def __str__ ( self ):
    return "Character attack key-release   (playerID = %d)" % (self.characterID)


class CharacterMagicPress ( Event ):

  def __init__ ( self, characterID ):
    self.characterID = characterID

  def __str__ ( self ):
    return "Character magic key-press   (playerID = %d)" % (self.characterID)


class CharacterMagicRelease ( Event ):

  def __init__ ( self, characterID ):
    self.characterID = characterID

  def __str__ ( self ):
    return "Character magic key-release   (playerID = %d)" % (self.characterID)


class CharacterMagicAttack ( Event ):

  def __init__ ( self, character ):
    self.character = character

  def __str__ ( self ):
    return "Character magic attack        (playerID = %d)" % (self.character.id)


class MobileDie (Event):

  def __init__ (self, mobile):
    self.mobile = mobile
    self.mobile.movingWest = False
    self.mobile.movingEast = False
    self.mobile.movingNorth = False
    self.mobile.movingSouth = False
    self.mobile.alive = False

  def __str__ (self):
    return "Mobile Die Event (mobileID = %d)" % (self.mobile.id)


class CharacterExit (Event):

  def __init__ ( self, charExited ):
    self.char = charExited
    self.char.alive = False

  def __str__(self):
    return "Character Exit Event (characterID = %d)" % (self.char.id)


class ItemPickUp (Event):

  def __init__(self, item):
    self.item = item

  def __str__(self):
    return "Item Pick up event (Item = %d)" % (self.item.type)


class DoorOpen (Event):

  def __init__(self, door):
    self.door = door

  def __str__(self):
    return "Door Open event"


class AddProjectile (Event):

  def __init__(self, proj):
    self.proj = proj

  def __str__(self):
    return "Add Projectile Event (proj = %d)" % (self.proj.classType)

class AddPlayerCharacter (Event):

  def __init__(self, pos, classType, ID):
    self.position = pos
    self.classType = classType
    self.ID = ID

class AddPlayerController (Event):

  def __init__(self, ID):
    self.ID = ID

class AbouttoDie (Event):

  def __init__(self, mobile):
    self.mobile = mobile
  
  def __str__(self):
    return "Character about to die"

