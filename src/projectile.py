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

import sys

try:
  import errors
  import mobile
  import events
  import character
except ImportError, err:
  print 'gauntlet: Could not load module. %s' % (err)
  sys.exit(2)


##\brief A projectile in the game
##
##Inherited from the Mobile class to represent a projectile in the game.

class Projectile ( mobile.Mobile ):

  ##\brief Projectile constructor
  ##
  ##\param
  ##\return None

  def __init__ ( self, initPosition, projType ):
    id = 0
    mobile.Mobile.__init__(self, initPosition, id)
    self.classType = projType
    # this needs to be removed when characters set the damage
    self.damage = 10
    self.score = 0
    self.health = 10

  #projectile (self) colliding with an immobile
  def collideImmobile( self, collideSprite, oldpos, eventManager):
    self.rect.topleft = oldpos.topleft
    newEvent = events.MobileDie(self)
    eventManager.post(newEvent)

  #mobile (self) colliding with a mobile
  def collideMobile( self, collideSprite, oldpos, eventManager):
    if isinstance(collideSprite, character.Character) or \
           not isinstance(collideSprite, Projectile):
      self.rect.topleft = oldpos.topleft
      collideSprite.takeDamage(self, eventManager)
      newEvent = events.MobileDie(self)
      eventManager.post(newEvent) 
    else:
      pass
