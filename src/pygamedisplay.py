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

try:
  import sys
  import os
  import pygame
  import events
  import errors
  import display
  import textdisplay
  import monstergenerator
  import exit
  import item
  import barrier
  from pygame.locals import *
  import skin
  from config import *
except ImportError, err:
  print "pygamedisplay.py: could not load module. %s " % (err)
  sys.exit(2)


##\brief A display using pygame only with scrolling
##
#Inherits from display for the generic display features.
##Displays the current state of the game using only pygame for
##graphics. This is very similar to the pygamedisplay, but adds
##side scrolling.
  
class PygameDisplay( display.Display ):

##\brief initializes the display and sets the background
##
##\param eventManager An event manager to listen to for game events
##\param options The options set at the command line
##\return None
  def __init__ ( self, eventManager, options ):
    # displayFlags should be nothing for pygame display
    displayFlags = 0
    display.Display.__init__(self, eventManager, options, displayFlags)


    self.buffer = pygame.surface.Surface((RESOLUTION[0]*5,RESOLUTION[1]*5))
    self.bufferRect = self.buffer.get_rect()

    # render text stuff - should be put in its own function eventually
    textSize = (RESOLUTION[0]/4,RESOLUTION[1])
    textLocationY = RESOLUTION[0]/4*3
    self.text = textdisplay.TextDisplay( self, self.eventManager, \
                                         textSize, textLocationY )

    self.characters = pygame.sprite.RenderUpdates()

    self.immobiles = pygame.sprite.RenderUpdates()
    self.mobiles = pygame.sprite.RenderUpdates()      
    self.initScreen()
    


  def initScreen (self):

    self.buffer = pygame.surface.Surface((RESOLUTION[0]*4,RESOLUTION[1]*4))
    self.bufferRect = self.buffer.get_rect()

    #initialize background
    #fullname = os.path.join('data','images','grey_tile.png')
    fullname = os.path.join('data','skins',skin.SKIN,'background.png')
    background = display.loadPng(fullname)
    background = background.convert()
    # This would be a good place to use the map size.
    self.background = pygame.surface.Surface((RESOLUTION[0]*5,RESOLUTION[1]*5))

    # Fill the whole background
    brect = background.get_rect()
    for j in xrange(self.background.get_rect().height / brect.height):
      for i in xrange(self.background.get_rect().width / brect.width):
        self.background.blit(background,(i*brect.width, j*brect.height))

    #draw background
    self.buffer.blit(self.background,(0,0))
    self.screen.blit(self.buffer,self.bufferRect)
    self.screen.blit(self.text.image, self.text.rect)
    pygame.display.update()
    self.dirty = False

    self.immobiles.draw(self.buffer)
    self.mobiles.draw(self.buffer)

  def buildSprites ( self, characters, immobiles, mobiles ):
    self.characters.empty()
    self.immobiles.empty()
    self.mobiles.empty()
    self.characters.add(characters)
    for mob in mobiles.sprites():
      mobileDisplay = MobilePygameDisplay(mob)
      self.mobiles.add(mobileDisplay)
    for immobile in immobiles.sprites():
      immobileDisplay = ImmobilePygameDisplay(immobile)
      self.immobiles.add(immobileDisplay)
    self.mobiles.draw(self.buffer)
    self.immobiles.draw(self.buffer)
    self.focusOnCharacters( self.characters )
    self.screen.blit(self.buffer,self.bufferRect)
    pygame.display.update()
    self.dirty = False

  def addMobile (self, mobile):
    mobileDisplay = MobilePygameDisplay(mobile)
    self.mobiles.add(mobileDisplay)
    self.buffer.blit(mobileDisplay.image,mobileDisplay.rect)
    self.dirty = True

  def addImmobile (self, immobile):
    immobileDisplay = ImmobilePygameDisplay(immobile)
    self.immobiles.add(immobileDisplay)

  def find ( self, mobileInstance ):
    mobID = mobileInstance.id
    for mob in self.mobiles.sprites():
      if mobID == 0:
        if mob.classType == mobileInstance.classType:
          return mob
      elif mob.id == mobID:
        return mob
  
  def notify ( self, event ):
    if isinstance( event, events.CharacterCollisionEvent):
      for obj in self.mobiles.sprites():
        if obj.id == event.collideObj:
          obj.draw()
    if isinstance( event, events.MobilePlaceEvent ):
      self.addMobile(event.mobile)
    if isinstance( event, events.CharacterMoveEvent ) and \
           event.character.alive:
      #get display character
      mob = self.find(event.character)
      
      #change the character's image to correspond to the character's direction
      if mob != None:
        mob.image = mob.imageList[event.character.direction].getImage()

        #update the character's new position
        mob.rect = mob.image.get_rect()
        mob.rect.topleft = event.character.rect.topleft
        #mob.rect = event.character.rect
  
        #clear old character area
        self.buffer.blit(self.background,event.oldRect,event.oldRect)
  
        #note:every mobile object (not PygameDisplay) should contain unique id
        #draw new character area
        self.buffer.blit(mob.image,mob.rect)
        self.dirty = True
  
    elif isinstance( event, events.StartGameEvent ):
      self.buffer.blit(self.background,(0,0))
      self.buildSprites(event.characters,event.immobiles,event.mobiles)
    elif isinstance( event, events.ToggleFullscreenEvent ):
      if self.fullscreen:
        displayFlags = self.displayFlags
        self.fullscreen = False
      else:
        displayFlags = self.displayFlags | FULLSCREEN
        self.fullscreen = True
      self.screen = pygame.display.set_mode(RESOLUTION, displayFlags)
      self.focusOnCharacters( self.characters )
      self.screen.blit(self.buffer,self.bufferRect)
      self.screen.blit(self.text.image,self.text.rect)
      pygame.display.update()
      self.dirty = False
    elif isinstance( event, events.DisplayTickEvent ):
      if self.dirty:
        #temporary fix to the display thats out of bounds of the map
        self.screen.blit(self.background,(0,0))
        self.focusOnCharacters( self.characters )
        self.screen.blit(self.buffer,self.bufferRect)
        self.screen.blit(self.text.image,self.text.rect)
        pygame.display.update()
        self.dirty = False

    elif isinstance( event, events.MobileDie):
      #clear old character area
      self.buffer.blit \
        (self.background,event.mobile.rect,event.mobile.rect)
      self.dirty = True
    elif isinstance( event, events.CharacterExit):
      #clear old character area
      self.buffer.blit \
        (self.background,event.char.rect,event.char.rect)
      self.dirty = True
    elif isinstance(event, events.ItemPickUp):
      #clear old item area
      self.buffer.blit \
        (self.background, event.item.rect, event.item.rect)
      self.dirty = True
    elif isinstance(event, events.DoorOpen):
      #clear old item area
      self.buffer.blit \
        (self.background, event.door.rect, event.door.rect)
      self.dirty = True
    elif isinstance(event, events.AddProjectile):
      #get display projectile
      mob = MobilePygameDisplay(event.proj)      
      self.mobiles.add(mob)
      self.dirty = True
    elif isinstance(event, events.GameOverEvent):
      #prints Game Over Splash Screen
      fontSize = pygame.font.Font(None,50)
      color = (255,0,0)
      text = fontSize.render("Game Over",1,color)
      textPOS = text.get_rect()
      # This should probably be generalized for differenct resolutions
      textPOS.topleft = (220,220)
      
      showSplash = True
      n = 0
      while showSplash:
      	self.screen.blit(text, textPOS)
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            sys.exit()
          elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()
          elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            pygame.display.toggle_fullscreen()
          elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            showSplash=False
        n += 1
        if n > 1000:
          showSplash=False
        pygame.display.update()

##\brief focuses the display on the characters
##
##\param characters The sprite group of characters to focus on
##\return None
  def focusOnCharacters( self, characters ):
    #calculate the center of the characters
    if len(characters.sprites()) > 0:
      # This used to focus on the first character
      #charx = characters.sprites()[0].rect.centerx
      #chary = characters.sprites()[0].rect.centery
      # This used to focus on multiple characters
      numChar = len(characters)
      charx = 0
      chary = 0
      if numChar <= 0:
        print "Warning, bad number of characters to focus on."
        return
      for charac in characters.sprites():
        charx += charac.rect.centerx
        chary += charac.rect.centery
      self.bufferRect.left = HALF_RESOLUTION[0] * 3 / 4 - charx / numChar
      self.bufferRect.top = HALF_RESOLUTION[1] - chary / numChar
    else:
      pass

class ImmobilePygameDisplay ( pygame.sprite.Sprite ):

  ##\brief ImmobilePygameDisplay constructor
  ##
  ##\param immobile The immobile object this display sprite is representing
  ##\return None

  def __init__ ( self, immobile ):
    pygame.sprite.Sprite.__init__(self)

    self.immobile = immobile
    if isinstance(self.immobile,exit.Exit):
      fullname = os.path.join('data','skins',skin.SKIN,'exit.png')
    elif isinstance(self.immobile,item.Item):
      if self.immobile.type == KEY:
        fullname = os.path.join('data','skins',skin.SKIN,'keyhoriz.png')
      elif self.immobile.type == FOOD:
        fullname = os.path.join('data','skins',skin.SKIN,'foodplate.png')
      elif self.immobile.type == POTION:
        fullname = os.path.join('data','skins',skin.SKIN,'bluepotion.png')
      elif self.immobile.type == GOLD:
        fullname = os.path.join('data','skins',skin.SKIN,'treasure.png')
    elif isinstance(self.immobile, barrier.Door):
      fullname = os.path.join('data','skins',skin.SKIN,'door.png')
    else:
      #implement singleton method here so images don't get loaded multiple times
      fullname = os.path.join('data','skins',skin.SKIN,'wall.png')

    self.image = display.loadPng(fullname)
    self.rect = immobile.rect


class MobilePygameDisplay ( pygame.sprite.Sprite ):

  ##\brief MobilePygameDisplay constructor
  ##
  ##\param mobile The mobile this display sprite is representing
  ##\return None

  def __init__ ( self, mobile ):
    pygame.sprite.Sprite.__init__(self)
    #implement singleton method here so images don't get loaded multiple times
    display.loadConfig(self,mobile.classType)
    self.id = mobile.id
    self.image = self.imageList[SOUTH].getImage()
    self.rect = mobile.rect
    self.classType = mobile.classType
