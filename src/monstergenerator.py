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

from random import *
import pygame
import events
import barrier
import mobile
import character
import map
from config import *


##\brief A monster generator in the game
##
##Represents a monster generator in the game. Creates monsters based on an
##external timer to weak havoc in Gauntlet land

class MonsterGenerator (mobile.Mobile ):

  ##\brief MonsterGenerator constructor
  ##
  ##\param initPosition A list (x,y) representing the monster generator's
  ##                    initial position
  ##\param genType Integer representing the type of genereated monsters
  ##\param level The level number of the monster generator
  ##\return None

  def __init__ ( self, initPosition, genType, level, id):
    mobile.Mobile.__init__(self,initPosition,id)
    self.type = genType
    self.level = level
    self.position = initPosition
    self.health = self.level * 10
    self.score = self.health
    self.classType = genType
    self.direction = 0
    self.defense = AVE_DEF
    self.monsterType = self.classType - GENERATOR_CLASS + MONSTER_CLASS
    self.speed = .12
    self.attackRest = random() / 2.0
    self.controller = None
    self.attacking = True

  # this attaches a controller to use for the generated monsters
  def attachController (self, controller):
    self.controller = controller

  def getPosition(self):
    return self.position

  def generate(self, mobiles, immobiles):
    x, y = self.position
    map.nextid += 1
    newMonster = character.Character((x +32, y), self.monsterType, map.nextid)
    if not pygame.sprite.spritecollide(newMonster, mobiles, False) and \
       not pygame.sprite.spritecollide(newMonster, immobiles, False):
      return newMonster
    
    newMonster = character.Character((x, y + 32), self.monsterType, map.nextid)
    if not pygame.sprite.spritecollide(newMonster, mobiles, False) and \
       not pygame.sprite.spritecollide(newMonster, immobiles, False):
      return newMonster
    
    newMonster = character.Character((x -32, y), self.monsterType, map.nextid)
    if not pygame.sprite.spritecollide(newMonster, mobiles, False) and \
       not pygame.sprite.spritecollide(newMonster, immobiles, False):
      return newMonster
      
    newMonster = character.Character((x, y- 32), self.monsterType, map.nextid)
    if not pygame.sprite.spritecollide(newMonster, mobiles, False) and \
       not pygame.sprite.spritecollide(newMonster, immobiles, False):
      return newMonster
    
    map.nextid -= 1
    return False

  # This is a placeholder for when we have the monster generators
  # generate on mobile attacking events.
  def attack(self, eventManager, mobiles, immobiles):
    monster = self.generate(mobiles, immobiles)
    if monster:
      mobiles.add(monster)
      # This could potentially cause conflict with the controller assigned in
      # game unless we remove it.
      if self.controller:
        self.controller.addMobile(monster)
      newEvent = events.MobilePlaceEvent(monster)
      eventManager.post(newEvent)
    # Add the random amount to vary the production rate
    self.attackRest += random() / 2.0
