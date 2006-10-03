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
#PyGauntlet is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with PyGauntlet; if not, write to the Free Software
#Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import sys
try:
  import pygame
  import events
  import errors
  import character as charactermodule
  import barrier
  import keyboardcontroller
  import monstergenerator
  import projectile
  import maploader
  import menu
  from config import *
  import skin

  #take this out later:
  import mobile
except ImportError, err:
  print "couldn't load module. %s" % (err)
  sys.exit(2)


class Game:
  STATE_INITIALIZING = 0
  STATE_RUNNING = 1
  STATE_PAUSED = 2

  def __init__ ( self, eventManager, options ):
    self.options = options
    self.eventManager = eventManager
    self.eventManager.registerListener(self)
    self.mapLoader = maploader.MapLoader(options.mapFilename)
    self.state = Game.STATE_INITIALIZING
    self.currentLevel = 1
    self.numTicks = 0
    self.keyboardControllers = []
    
    self.characterList = []
    self.characters = pygame.sprite.RenderPlain()
    self.mobiles = pygame.sprite.RenderPlain()
    self.immobiles = pygame.sprite.RenderPlain()
    self.doors = pygame.sprite.RenderPlain()
    self.ghostcontroller = keyboardcontroller.StateMachineController(self.eventManager,"data/skins/"+skin.SKIN+"/ghost.stm")
    
  # called at the start of each level
  def init ( self ):
    self.map = self.mapLoader.nextMap(self.currentLevel)

    # Reset the characters state
    for character in self.characterList:
      character.alive = True
      character.attacking = False
      character.magicing = False
      character.movingWest = False
      character.movingEast = False
      character.movingNorth = False
      character.movingSouth = False
      self.characters.add(character)

    # Put the characters in their starting positions from the map
    startList = self.map.getStartList()
    counter = 1
    for character in self.characterList:
      character.rect.topleft = startList[counter]
      counter += 1

    self.mobiles.add(self.characters)
    self.mobiles.add(self.map.getMonsterList())
    self.immobiles.add(self.map.getImmobiles())
    self.doors.add(self.map.getDoors())

    self.state = Game.STATE_RUNNING

    for monster in self.map.getMonsterList().sprites():
      # Don't give monster generators state machines
      if not isinstance(monster, monstergenerator.MonsterGenerator):
        self.ghostcontroller.addMobile(monster);

    eventPost = events.StartGameEvent(self.characters,self.immobiles, self.mobiles)
    self.eventManager.post(eventPost)

  def notify ( self, event ):

    if isinstance(event,events.TickEvent):
      if self.state == Game.STATE_RUNNING:

        #increment the number of ticks (used for monster generation)
        self.numTicks += 1
        if self.numTicks > MONSTER_GENERATE_TIMER:
          self.numTicks = 0

        #mark all mobiles to show that they haven't been updated for this tick
        for mobile in self.mobiles.sprites():
          mobile.updated = False

        for character in self.characterList:
          #create a box representing the character's vision
          characterVision = pygame.sprite.Sprite()
          characterVision.rect = pygame.Rect ( \
              character.rect.left-(TILE_SIZE*VISION), \
              character.rect.top-(TILE_SIZE*VISION), \
              TILE_SIZE*VISION*2+1, \
              TILE_SIZE*VISION*2+1 )
          #find all mobiles that are within the character's vision
          for collideSprite in pygame.sprite.spritecollide(characterVision,self.mobiles,False):
            #if mobile has not been updated then update the mobile
            if not collideSprite.updated:
              collideSprite.update(self.eventManager,self.mobiles,self.immobiles)
              collideSprite.updated = True
              #generate a monster if numTicks is at the right number
              #if isinstance(collideSprite,monstergenerator.MonsterGenerator) \
              #       and self.numTicks == MONSTER_GENERATE_TIMER:

        #update projectiles that haven't been updated since the character's
        #vision shouldn't affect whether or not they updated
        for mobile in self.mobiles.sprites():
          if isinstance(mobile,projectile.Projectile):
            if not mobile.updated:
              mobile.update(self.eventManager,self.mobiles,self.immobiles)

      elif self.state == Game.STATE_PAUSED:
        pass
      elif self.state == Game.STATE_INITIALIZING:
        self.init()
    #attach a monster to its controller on creation
    elif isinstance(event,events.MobilePlaceEvent):
      self.ghostcontroller.addMobile(event.mobile)
    #check to see if game has started?
    elif isinstance(event,events.CharacterMovePress):
      for character in self.mobiles.sprites():
        if character.id == event.characterID:
          if event.direction == NORTH:
            character.movingNorth = True
          elif event.direction == SOUTH:
            character.movingSouth = True
          elif event.direction == EAST:
            character.movingEast = True
          elif event.direction == WEST:
            character.movingWest = True
    elif isinstance(event,events.CharacterMoveRelease):
      for character in self.mobiles.sprites():
        if character.id == event.characterID:
          if event.direction == NORTH:
            character.movingNorth = False
          elif event.direction == SOUTH:
            character.movingSouth = False
          elif event.direction == EAST:
            character.movingEast = False
          elif event.direction == WEST:
            character.movingWest = False
    elif isinstance(event,events.CharacterAttackPress):
      for character in self.mobiles.sprites():
        if character.id == event.characterID:
          character.attacking = True
    elif isinstance(event,events.AddProjectile):
      self.mobiles.add(event.proj)
    elif isinstance(event,events.CharacterAttackRelease):
      for character in self.mobiles.sprites():
        if character.id == event.characterID:
          character.attacking = False
    elif isinstance(event,events.CharacterMagicPress):
      pass
    elif isinstance(event,events.CharacterMagicRelease):
      for character in self.mobiles.sprites():
        if character.id == event.characterID:
          if character.potions > 0:
            eventPost = events.CharacterMagicAttack(character)
            self.eventManager.post(eventPost)
    elif isinstance(event,events.CharacterMagicAttack):
      event.character.potions -= 1
      magicSprite = pygame.sprite.Sprite()
      magicSprite.rect = pygame.Rect ( \
                event.character.rect.left-(TILE_SIZE*event.character.intelligence), \
                event.character.rect.top-(TILE_SIZE*event.character.intelligence), \
                TILE_SIZE*(event.character.intelligence*2+1), \
                TILE_SIZE*(event.character.intelligence*2+1))
      for collideSprite in pygame.sprite.spritecollide(magicSprite, \
                                                       self.mobiles, \
                                                       False):
        if (not collideSprite in self.characterList):
          collideSprite.takeMagicDamage(event.character,self.eventManager)
    elif isinstance(event, events.MobileDie):
      event.mobile.kill()
      for character in self.characterList:
        if character == event.mobile:
          self.characterList.remove(character)
      if len(self.characters) == 0:
        gameOver = True
        for char in self.characterList:
          if char.health > 0:
            gameOver = False
        if gameOver:
          newEvent = events.GameOverEvent()
          self.eventManager.post(newEvent)
          #take this out when we fix stuff
          print "Game Over."
#          sys.exit(0)
          #return to splash screen
          #self.state = Game.STATE_INITIALIZING
          #theGame = Game(self.eventManager,self.options)
          #menu.splashScreen()
          #menu.characterScreen(self.eventManager,theGame)
        else:
          self.currentLevel += 1
          self.state = Game.STATE_INITIALIZING
          for i in self.mobiles.sprites():
            i.kill()
          for i in self.immobiles.sprites():
            i.kill()
          self.init()
    elif isinstance(event, events.ItemPickUp):
      event.item.kill()
    elif isinstance(event, events.AddPlayerCharacter):
      player = charactermodule.Character(event.position,event.classType,event.ID)
      self.characterList.append(player)
    elif isinstance(event, events.AddPlayerController):
      self.keyboardControllers.append(keyboardcontroller.PlayerController(self.eventManager,event.ID))
    elif isinstance(event, events.DoorOpen):
      collideList = pygame.sprite.RenderPlain()
      event.door.rect = event.door.rect.move(1,1)
      collideList.add(pygame.sprite.spritecollide(event.door,self.doors,False))
      event.door.rect = event.door.rect.move(-2,-2)
      collideList.add(pygame.sprite.spritecollide(event.door,self.doors,False))
      event.door.rect = event.door.rect.move(1,1)
      event.door.kill()
      for immob in collideList.sprites():
        immob.open = True
        doorOpen = events.DoorOpen(immob)
        self.eventManager.post(doorOpen)
    elif isinstance(event, events.CharacterExit):
      event.char.kill()
      if len(self.characters) == 0:
        self.currentLevel += 1
        self.state = Game.STATE_INITIALIZING
        for i in self.mobiles.sprites():
          i.kill()
        for i in self.immobiles.sprites():
          i.kill()
        self.init()
