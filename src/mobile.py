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

import pygame
import events
import barrier
import exit
import immobile
import character
import item
import errors
from config import *

##\brief A mobile object in the game (virtual class)
##
##Represents a mobile object in the game. Includes all objects that move in the game

class Mobile ( pygame.sprite.Sprite ):
  
  ##\brief Mobile constructor
  ##
  ##\return None

  def __init__ ( self, initPosition, id=0 ):
    pygame.sprite.Sprite.__init__(self)
    self.id = id
    self.rect = pygame.Rect(initPosition,[TILE_SIZE,TILE_SIZE])
    self.movingWest = False
    self.movingEast = False
    self.movingNorth = False
    self.movingSouth = False
    self.resting = 0.0
    self.speed = 0.0
    self.damage = 1
    self.alive = True
    #controller related variables
    self.controller = None
    self.currentState = 0
    self.stateTimer = 0
    self.attackRest = 0.0
    self.attacking = False
    self.updated = False

  ##\brief Updates a mobile object's position
  ##
  ##Updates the mobile object's position while detecting for collisions.
  ##If a collision is detected, then the movement does not occur.
  ##
  ##\param mobiles A sprite group containing all the Mobile sprites
  ##\param immobiles A sprite group containing all the Immobile sprites
  ##\return None

  def update ( self, eventManager, mobiles, immobiles ):
    if self.attackRest < ATTACK_TIME:
      self.attackRest += self.speed
    if self.resting < REST_TIME:
      self.resting += self.speed
    elif self.movingWest or self.movingEast or self.movingNorth or \
             self.movingSouth or self.attacking:
      oldRect = self.rect

      if self.movingWest or self.movingEast and self.alive:
        # move the object
        move = 0
        if self.movingWest:
          move -= MOVE_SPEED
        if self.movingEast:
          move += MOVE_SPEED
        self.rect = self.rect.move(move,0)

        # check for and handle collisions in horizontal move
        for collideSprite in pygame.sprite.spritecollide(self,immobiles,False):
          if isinstance(collideSprite, barrier.Door) and \
             collideSprite.open:
            pass
          else:
            self.collideImmobile(collideSprite, oldRect, eventManager)
            collisionEvent = events.CharacterCollisionEvent(self)
            eventManager.post(collisionEvent)
        for collideSprite in pygame.sprite.spritecollide(self,mobiles,False):
          if collideSprite != self:
            self.collideMobile(collideSprite, oldRect, eventManager)
            collisionEvent = events.CharacterCollisionEvent(self)
            eventManager.post(collisionEvent)

      if self.movingNorth or self.movingSouth and self.alive:
        secondRect = self.rect
        # move the object
        move = 0
        if self.movingNorth:
          move -= MOVE_SPEED
        if self.movingSouth:
          move += MOVE_SPEED
        self.rect = self.rect.move(0,move)
  
        # check for and handle collisions in vertical move
        for collideSprite in pygame.sprite.spritecollide(self,immobiles,False):
          if isinstance(collideSprite, barrier.Door) and \
             collideSprite.open:
            pass
          else:
            self.collideImmobile(collideSprite, secondRect, eventManager)
            collisionEvent = events.CharacterCollisionEvent(self,collideSprite)
            eventManager.post(collisionEvent)
        for collideSprite in pygame.sprite.spritecollide(self,mobiles,False):
          if collideSprite != self:
            self.collideMobile(collideSprite, secondRect, eventManager)
            collisionEvent = events.CharacterCollisionEvent(self)
            eventManager.post(collisionEvent)

      # check for changes and post move events
      if self.rect != oldRect:
        self.postMove(eventManager, oldRect)
        self.resting -= REST_TIME
      else:
        # this was an attempt to reduce the excess number of collisions
        #self.resting -= 50
        self.resting = REST_TIME

      if self.alive and self.attacking and self.attackRest >= ATTACK_TIME:
        self.attack(eventManager, mobiles, immobiles)
        self.attackRest -= ATTACK_TIME
        
##\brief a private method to change the direction and post the move
##event at the same time
##
##\param eventManager a reference to the event manager
##\param oldRect the old position to post
##\return None
  def postMove( self, eventManager, oldRect ):
    #calculate direction
    if self.movingEast:
      if self.movingSouth:
        self.direction = SOUTHEAST
      elif self.movingNorth:
        self.direction = NORTHEAST
      else:
        self.direction = EAST
    elif self.movingWest:
      if self.movingSouth:
        self.direction = SOUTHWEST
      elif self.movingNorth:
        self.direction = NORTHWEST
      else:
        self.direction = WEST
    else:
      if self.movingSouth:
        self.direction = SOUTH
      elif self.movingNorth:
        self.direction = NORTH
    moveEvent = events.CharacterMoveEvent(self,oldRect)
    eventManager.post(moveEvent)

  def getVectorToPoint(self,position=(0,0)):
    return (position[0] - self.rect[0], position[1] - self.rect[1])

  # Take damage and give the damage doer score if it kills
  def takeDamage(self, damageDoer, eventManager):
    self.health -= damageDoer.damage * AVE_DEF / self.defense
    if self.health <= 0:
      # Add score
      if damageDoer.classType >= PROJECTILE:
        damageDoer.owner.score += self.score
      else:
        damageDoer.score += self.score
      # Post event
      newEvent = events.MobileDie(self)
      eventManager.post(newEvent) 
    if self.health == 7  and isinstance(self,character.Character):
        newEvent = events.AbouttoDie(self)
        eventManager.post(newEvent)

  # Take magic damage and give the damage doer score if it kills
  def takeMagicDamage(self, damageDoer, eventManager):
    self.health -= damageDoer.intelligence * 4
    if self.health <= 0:
      # Add score
      damageDoer.score += self.score
      # Post event
      newEvent = events.MobileDie(self)
      eventManager.post(newEvent) 
    if self.health ==  7  and isinstance(self,character.Character):
      newEvent = events.AbouttoDie(self)
      eventManager.post(newEvent)
    
  def kill(self):
    if self.controller:
      self.controller.releaseMobile(self)
    pygame.sprite.Sprite.kill(self)
