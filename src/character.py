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

try:
  import pygame
  import events
  import errors
  import mobile
  import barrier
  import projectile
  import item
  import exit
  from config import *
  import stats
except ImportError, err:
  print "couldn't load module. %s" % (err)
  sys.exit(2)


##\brief A character in the game
##
##Inherited from the Mobile class to represent a character in the game.
##Maintains information about the character: position, id, health, gold, etc.

class Character ( mobile.Mobile ):

  ##\brief Character constructor
  ##
  ##\param initPosition A list (x,y) representing the character's inital
  ##                    position
  ##\param characterClass Integer representing the character type
  ##\param id Integer Identifies a Character
  ##\return None

  def __init__ \
    ( self, initPosition, characterClass, id ):
    mobile.Mobile.__init__(self, initPosition, id)
    self.classType = characterClass
    self.direction = SOUTH
    self.gold = 0
    self.potions = 5
    self.keys = 0
    self.score = 0
    self.health = 50
    self.exiting = False
    self.attacking = False
    
    try:
      self.strength = stats.STRENGTH[self.classType]
      self.defense = stats.DEFENSE[self.classType]
      self.intelligence = stats.INTELLIGENCE[self.classType]
      self.dexterity = stats.DEXTERITY[self.classType]
      self.health = stats.HEALTH[self.classType]
    except:
      self.strength = stats.STRENGTH[stats.DEFAULT]
      self.defense = stats.DEFENSE[stats.DEFAULT]
      self.intelligence = stats.INTELLIGENCE[stats.DEFAULT]
      self.dexterity = stats.DEXTERITY[stats.DEFAULT]
      self.health = stats.HEALTH[stats.DEFAULT]

    # calculate the mobile values
    self.speed = self.dexterity / AVE_DEX
    self.damage = self.strength / AVE_STR
    if not self.classType in PLAYERS:
      self.score += self.health

  ##\brief Collision detection for immobiles
  ##
  ##\param collideSprite the sprite the character (self) is colliding with
  ##\param oldpos the old position of the character (self)
  ##\param eventManager THE event manager
  ##\param initPosition A list (x,y) representing the barrier's inital position
  ##\return None

  def collideImmobile( self, collideSprite, oldpos, eventManager):

    #character (self) colliding with a barrier
    if isinstance(collideSprite,barrier.Barrier):
      self.rect.topleft = oldpos.topleft

    if self.classType in PLAYERS:
      #player (self) colliding with an exit
      if isinstance(collideSprite,exit.Exit):
        exitEvent = events.CharacterExit(self)
        eventManager.post(exitEvent)
      #player (self) colliding with a door
      elif isinstance(collideSprite,barrier.Door):
        if self.keys > 0:
          self.keys -= 1
          doorOpen = events.DoorOpen(collideSprite)
          eventManager.post(doorOpen)
        else:
          self.rect.topleft = oldpos.topleft
      #player (self) colliding with an item
      elif isinstance(collideSprite,item.Item):
        if collideSprite.type == KEY:
          keyUp = events.ItemPickUp(collideSprite)
          eventManager.post(keyUp)
          self.keys += 1
        elif collideSprite.type == FOOD:
          foodUp = events.ItemPickUp(collideSprite)
          eventManager.post(foodUp)
          self.health += collideSprite.value
        elif collideSprite.type == POTION:
          magicUp = events.ItemPickUp(collideSprite)
          eventManager.post(magicUp)
          self.potions += 1
        elif collideSprite.type == GOLD:
          goldUp = events.ItemPickUp(collideSprite)
          eventManager.post(goldUp)
          self.gold += collideSprite.value
          self.score += collideSprite.value
    else:
      self.rect.topleft = oldpos.topleft

  ##\brief Collision detection for mobiles
  ##
  ##\param collideSprite the sprite the character (self) is colliding with
  ##\param oldpos the old position of the character (self)
  ##\param eventManager THE event manager
  ##\param initPosition A list (x,y) representing the barrier's inital position
  ##\return None

  def collideMobile( self, collideSprite, oldpos, eventManager):
    if isinstance(collideSprite, Character):
      if (self.classType in PLAYERS and \
          collideSprite.classType in PLAYERS) or \
          (self.classType not in PLAYERS and \
           collideSprite.classType not in PLAYERS) and \
           (self.classType < PROJECTILE):
        self.rect.topleft = oldpos.topleft
      else:
        self.rect.topleft = oldpos.topleft
        collideSprite.takeDamage(self, eventManager)
    else:
      if not isinstance(collideSprite, projectile.Projectile):
        self.rect.topleft = oldpos.topleft
        if self.classType in PLAYERS:
          collideSprite.takeDamage(self, eventManager)

  ##\brief updates the character (self) every tick of the game
  ##
  ##\param eventManager THE event manager
  ##\param mobiles the list of mobiles
  ##\param immobiles the list of immobiles
  ##\return None

  def update ( self, eventManager, mobiles, immobiles ):
      mobile.Mobile.update( self, eventManager, mobiles, immobiles )
      if self.alive and self.attacking and self.attackRest >= ATTACK_TIME:
        self.attack(eventManager, mobiles, immobiles)
        self.attackRest = 0.0
        
  ##\brief character shoots a projectile
  ##
  ##\param eventManager THE event manager
  ##\param mobiles the list of mobiles
  ##\param immobiles the list of immobiles
  ##\return None

  def attack( self, eventManager, mobiles, immobiles ):
    newProjectile = projectile.Projectile( self.rect.topleft, \
                            self.classType + PROJECTILE )
    newProjectile.owner = self
    if self.direction == NORTH or self.direction == NORTHWEST or \
       self.direction == NORTHEAST:
      newProjectile.movingNorth = True
      newProjectile.rect.top -= TILE_SIZE
    elif self.direction == SOUTH or self.direction == SOUTHWEST or \
         self.direction == SOUTHEAST:
      newProjectile.movingSouth = True
      newProjectile.rect.top += TILE_SIZE
    if self.direction == EAST or self.direction == SOUTHEAST or \
       self.direction == NORTHEAST:
      newProjectile.movingEast = True
      newProjectile.rect.left += TILE_SIZE
    elif self.direction == WEST or self.direction == SOUTHWEST or \
         self.direction == NORTHWEST:
      newProjectile.movingWest = True
      newProjectile.rect.left -= TILE_SIZE
    newProjectile.direction = self.direction
    newProjectile.speed = 3 * self.speed
    #check if the projectile is colliding with anything before adding
    if pygame.sprite.spritecollide(newProjectile,mobiles,False): 
      for mob in pygame.sprite.spritecollide(newProjectile,mobiles,False):
        if not isinstance(mob, projectile.Projectile):
          mob.takeDamage(newProjectile, eventManager)
    elif pygame.sprite.spritecollide(newProjectile,immobiles,False):
      pass
    else:
      projEvent = events.AddProjectile(newProjectile)
      eventManager.post(projEvent)
      #self.resting -= ATTACK_TIME
