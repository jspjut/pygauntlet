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

import events
from pygame.locals import *
from config import *

CONTINUE1 = 50
CONTINUE5 = 51
CURRENTDIR = 52
NEARESTPLAYER = 53
FIRE = 54
CONDITIONS = {"NORTH":NORTH,
              "SOUTH":SOUTH,
              "EAST":EAST,
              "WEST":WEST,
              "NORTHEAST":NORTHEAST,
              "SOUTHEAST":SOUTHEAST,
              "NORTHWEST":NORTHWEST,
              "SOUTHWEST}":SOUTHWEST,
              "CONTINUE1":CONTINUE1,
              "CONTINUE5":CONTINUE5,
              "CURRENTDIR":CURRENTDIR,
              "NEARESTPLAYER":NEARESTPLAYER,
              "FIRE":FIRE}

class KeyboardController:

  def __init__ ( self, eventManager ):
    self.eventManager = eventManager
    self.eventManager.registerListener(self)


class SystemController ( KeyboardController ):

  def __init__ ( self, eventManager ):
    KeyboardController.__init__(self,eventManager)

  def notify ( self, event ):
    if isinstance(event,events.TickEvent):
      for event in event.pygameEvents:
        eventPost = None
        if event.type == QUIT:
          eventPost = events.QuitEvent()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
          eventPost = events.QuitEvent()
        elif event.type == KEYDOWN and event.key == K_f:
          eventPost = events.ToggleFullscreenEvent()
        if eventPost:
          self.eventManager.post(eventPost)

class StateMachineController ( KeyboardController ):

  def __init__ ( self, eventManager, fileName, mobile=None ):
    KeyboardController.__init__(self,eventManager)
    self.playerPositions = {}
    self.mobiles = []
    if mobile != None:
      self.mobiles.append(mobile)
    for mobile in self.mobiles:
      if mobile != None:
        mobile.controller = self
    self.loadMachine(fileName)
    self.stateTimer = 0
  def setMobile(self,mobile):
    self.mobiles = [mobile]
    mobile.controller = self
  def addMobile(self,mobile):
    self.mobiles.append(mobile)
    mobile.controller = self
  def releaseMobile(self,mobile):
    for cmobile in self.mobiles:
      if cmobile == mobile:
        self.mobiles.remove(cmobile)
      
  def step(self):
    for mobile in (self.mobiles):
      if(mobile == None):
        continue
      direction = mobile.direction
      mobile.stateTimer += 1
      if(self.states[mobile.currentState]['action'] == "attack"):
        if mobile.direction == NORTH or \
           mobile.direction == SOUTH or \
           mobile.direction == EAST or \
           mobile.direction == WEST:
          eventPost = events.CharacterAttackPress(mobile.id)
          self.eventManager.post(eventPost)
      elif(self.states[mobile.currentState]['action'] == "move"):
        if self.states[mobile.currentState]['actionparam'] == CURRENTDIR:
          direction = mobile.direction
        elif self.states[mobile.currentState]['actionparam'] == NEARESTPLAYER:
          bestSquaredOffset = -1;
          nearestPosition = (0,0)
          for playerPosKey in self.playerPositions.keys():
            playerPos = self.playerPositions[playerPosKey]
            horiz_offset = mobile.rect[0] - playerPos[0] 
            vert_offset = mobile.rect[1] - playerPos[1]
            squaredOffset = horiz_offset*horiz_offset + vert_offset*vert_offset
            if bestSquaredOffset < 0 or \
               squaredOffset < bestSquaredOffset:
              bestSquaredOffset = squaredOffset
              nearestPosition = playerPos
          horiz_offset = mobile.rect[0] - nearestPosition[0] 
          vert_offset = mobile.rect[1] - nearestPosition[1]
          if horiz_offset > 0:#nearest is West of mobile
            if not mobile.movingWest:
              eventPost = events.CharacterMovePress(mobile.id,WEST)
              self.eventManager.post(eventPost)
          elif horiz_offset < 0:#nearest is East of mobile
            if not mobile.movingEast:
              eventPost = events.CharacterMovePress(mobile.id,EAST)
              self.eventManager.post(eventPost)
          if vert_offset > 0:#nearest is North of mobile
            if not mobile.movingNorth:
              eventPost = events.CharacterMovePress(mobile.id,NORTH)
              self.eventManager.post(eventPost)
          elif vert_offset < 0:#nearest is South of mobile
            if not mobile.movingSouth:
              eventPost = events.CharacterMovePress(mobile.id,SOUTH)
              self.eventManager.post(eventPost)
      
        else:
          direction = self.states[mobile.currentState]['actionparam']
        eventPost = events.CharacterMovePress(mobile.id,direction)
        self.eventManager.post(eventPost)
        
      if self.evaluateCondition(self.states[mobile.currentState]['condition'],mobile):
        if(self.states[mobile.currentState]['conditionaction'] == "release"):
          if self.states[mobile.currentState]['action'] == "attack":
            eventPost = events.CharacterAttackRelease(mobile.id)
            self.eventManager.post(eventPost)
          elif self.states[mobile.currentState]['actionparam'] == NEARESTPLAYER:
            if mobile.movingWest:
              eventPost = events.CharacterMoveRelease(mobile.id,WEST)
              self.eventManager.post(eventPost)
            if mobile.movingEast:
              eventPost = events.CharacterMoveRelease(mobile.id,EAST)
              self.eventManager.post(eventPost)
            if mobile.movingNorth:
              eventPost = events.CharacterMoveRelease(mobile.id,NORTH)
              self.eventManager.post(eventPost)
            if mobile.movingSouth:
              eventPost = events.CharacterMoveRelease(mobile.id,SOUTH)
              self.eventManager.post(eventPost)
          
          self.eventManager.post(eventPost)
        mobile.currentState = self.states[mobile.currentState]['conditionstate']
        mobile.stateTimer = 0
      else:
        mobile.currentState = int(self.states[mobile.currentState]['defaultstate'])

  def loadMachine(self,filename):
    self.states = []
    # Attempt to load the statemachine file
    try:
      stateFile = open(filename)
    except:
      print "State Machine file %s could not be loaded."%filename
      sys.exit(1)
    # Read the lines of the state file
    stateLines = stateFile.readlines()
    lineNum = 1

    # Parse each line separately
    for line in stateLines:
      line = line.strip()
      parts = line.split(":")
      if parts[5] == '':
        parts[5] = len(self.states)
      self.states.append({"action": parts[0],
                          "actionparam": CONDITIONS[parts[1]],
                          "condition":CONDITIONS[parts[2]],
                          "conditionaction":parts[3],
                          "conditionstate":int(parts[4]),
                          "defaultstate": int(parts[5])})
    self.currentState = 0
    
  def evaluateCondition(self,condition,mobile):
    if condition == CONTINUE1:
      if(mobile.stateTimer < 10):
        return False
      else:
        return True
    elif condition == CONTINUE5:
      if(mobile.stateTimer < 50):
        return False
      else:
        return True
    elif condition == NORTH:
      if mobile.direction == NORTH:
        return True
    elif condition == SOUTH:
      if mobile.direction == SOUTH:
        return True
    elif condition == EAST:
      if mobile.direction == EAST:
        return True
    elif condition == WEST:
      if mobile.direction == WEST:
        return True
    elif condition == NORTHEAST:
      if mobile.direction == NORTHEAST:
        return True
    elif condition == SOUTHEAST:
      if mobile.direction == SOUTHEAST:
        return True
    elif condition == NORTHWEST:
      if mobile.direction == NORTHWEST:
        return True
    elif condition == SOUTHWEST:
      if mobile.direction == SOUTHWEST:
        return True
    else:
      return False
    return False

  def notify ( self, event ):
    if isinstance(event,events.CharacterMoveEvent):
      if event.character.classType in PLAYERS:#this is a player character
        self.playerPositions[event.character.id] = (event.character.rect[0],event.character.rect[1])
    if isinstance(event,events.MobileDie):
      if event.mobile.classType in PLAYERS and \
         event.mobile.id in self.playerPositions.keys():
        del self.playerPositions[event.mobile.id]
    if isinstance(event,events.TickEvent):
      self.step()
      
class PlayerController ( KeyboardController ):

  def __init__ ( self, eventManager, characterID ):
    KeyboardController.__init__(self,eventManager)
    self.characterID = characterID
    self.keys = PLAYER_KEYS[characterID]

  def notify ( self, event ):
    if isinstance(event,events.TickEvent):
      for event in event.pygameEvents:
        eventPost = None
        if event.type == KEYDOWN:
          if event.key == self.keys[NORTH]:
            direction = NORTH
            eventPost = events.CharacterMovePress(self.characterID,direction)
          elif event.key == self.keys[SOUTH]:
            direction = SOUTH
            eventPost = events.CharacterMovePress(self.characterID,direction)
          elif event.key == self.keys[WEST]:
            direction = WEST
            eventPost = events.CharacterMovePress(self.characterID,direction)
          elif event.key == self.keys[EAST]:
            direction = EAST
            eventPost = events.CharacterMovePress(self.characterID,direction)
          elif event.key == self.keys[ATTACK]:
            eventPost = events.CharacterAttackPress(self.characterID)
          elif event.key == self.keys[MAGIC]:
            eventPost = events.CharacterMagicPress(self.characterID)
        elif event.type == KEYUP:
          #setup a key for the player to quit the game
          if event.key == self.keys[NORTH]:
            direction = NORTH
            eventPost = events.CharacterMoveRelease(self.characterID,direction)
          elif event.key == self.keys[SOUTH]:
            direction = SOUTH
            eventPost = events.CharacterMoveRelease(self.characterID,direction)
          elif event.key == self.keys[WEST]:
            direction = WEST
            eventPost = events.CharacterMoveRelease(self.characterID,direction)
          elif event.key == self.keys[EAST]:
            direction = EAST
            eventPost = events.CharacterMoveRelease(self.characterID,direction)
          elif event.key == self.keys[ATTACK]:
            eventPost = events.CharacterAttackRelease(self.characterID)
          elif event.key == self.keys[MAGIC]:
            eventPost = events.CharacterMagicRelease(self.characterID)
        if eventPost:
          self.eventManager.post(eventPost)
