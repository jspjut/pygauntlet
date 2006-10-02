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
import display
import events

class TextDisplay ( pygame.sprite.Sprite ):

  def __init__ ( self, myDisplay, eventManager, size, x ):
    self.display = myDisplay
    self.eventManager = eventManager
    self.eventManager.registerListener(self)
    pygame.sprite.Sprite.__init__( self )
    self.image = pygame.surface.Surface( size )
    self.background = pygame.surface.Surface( size )
    self.rect = self.image.get_rect()
    self.characters = []
    self.players = []
    self.level = 0
    #This is kind of ugly and should be cleaned up
    self.nameStr = [0, 0, 0, 0]
    self.healthStr = [0, 0, 0, 0]
    self.keysStr = [0, 0, 0, 0]
    self.potionStr = [0, 0, 0, 0]
    
    # If you want the icon to display on the side, set this to true
    icon = True
    if not icon:
      fontsize = 50
      grey = (100, 100, 100)
      text, textpos = display.renderText("Gauntlet", fontsize, grey)
      textpos.centerx = self.rect.centerx
    else:
      text = self.display.iconImage
      text = pygame.transform.scale(text,(160,160))
      textpos = text.get_rect()
      textpos.centerx = self.rect.centerx
      textpos.top = textpos.top - 30
    self.image.blit(text, textpos)
    self.headerEnd = textpos.bottom
    # Shift to the right side of the screen
    self.rect.topleft = (x, 0)
    self.x = x
    self.dirty = True

  def notify ( self, event ):
    if isinstance(event, events.StartGameEvent):
      self.level += 1
      self.levelText = 'Level ' + str(self.level)
      self.dirty = True
      self.characters = event.characters.sprites()
      self.players = []
      for i in xrange(len(self.characters)):
        self.players.append(i)
    elif isinstance(event, events.DisplayTickEvent):
      self.updateText()
      self.drawText()
    else:
      pass

  def updateText( self ):
    playerNum = 0

    for player in self.characters:
      self.players[playerNum] = playerNum
      origStr = self.nameStr[playerNum] + self.healthStr[playerNum] +\
                self.keysStr[playerNum] + self.potionStr[playerNum]
      self.nameStr[playerNum] = 'Player'+ str(playerNum+1) + \
                                ' Score: ' + str(int(player.score))
      self.healthStr[playerNum] = 'Health: ' + str(int(player.health))
      self.keysStr[playerNum] = 'Keys: ' + str(int(player.keys))
      self.potionStr[playerNum] = 'Potions: ' + str(int(player.potions))
      finalStr = self.nameStr[playerNum] + self.healthStr[playerNum] +\
                 self.keysStr[playerNum] + self.potionStr[playerNum]
      # Set dirty if there were any changes
      if origStr != finalStr:
        self.dirty = True
      playerNum += 1

  def drawText( self ):
    #only draw if there have been changes
    if self.dirty:
      # Move the overall rect back to (0,0)
      self.rect.topleft = (0, 0)

      fontsize = 20
      grey = (150, 150, 150)
      white = (255, 255, 255)

      reference = self.headerEnd

      text, textPos = display.renderText(self.levelText, fontsize + 10, \
                                         white)
      textPos.centery = reference
      self.image.blit(self.background, textPos)
      self.image.blit(text, textPos)
      reference = textPos.bottom + 20
      
      for playerNum in self.players:
        text, namepos = display.renderText(self.nameStr[playerNum],\
                                           fontsize, white)
        text2, healthpos = display.renderText(self.healthStr[playerNum],\
                                              fontsize, grey)
        text3, keyspos = display.renderText(self.keysStr[playerNum],\
                                            fontsize, grey)
        text4, potionpos = display.renderText(self.potionStr[playerNum],\
                                              fontsize, grey)
        
        namepos.centery = reference
        healthpos.top = namepos.bottom
        keyspos.top = healthpos.bottom
        potionpos.top = keyspos.bottom
        
        self.image.blit(self.background, namepos)
        self.image.blit(text, namepos)
        self.image.blit(self.background, healthpos)
        self.image.blit(text2, healthpos)
        self.image.blit(self.background, keyspos)
        self.image.blit(text3, keyspos)
        self.image.blit(self.background, potionpos)
        self.image.blit(text4, potionpos)

        reference = potionpos.bottom + 20

      self.dirty = False
      # Move the overall rect back to the right of the screen
      self.rect.topleft = (self.x, 0)
      self.display.dirty = True
