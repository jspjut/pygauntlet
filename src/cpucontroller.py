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

import time
import pygame
import events
from config import *


##\brief CPU controller
##
##posts tick events to the event manager. also is used as the server for
##networking

class CPUController:

  ##\brief CPUController constructor
  ##
  ##\param eventManager THE event manager
  ##\return None

  def __init__ ( self, eventManager ):
    self.eventManager = eventManager
    self.eventManager.registerListener(self)
    self.gameLoop = True

  ##\brief starts RUNning the game
  ##
  ##\return None

  def run ( self ):
    displayTick = 0
    while self.gameLoop:
      startTick = pygame.time.get_ticks()
      displayTick += 1
      if displayTick >= DISPLAY_DELAY:
        displayTickEvent = events.DisplayTickEvent()
        self.eventManager.post(displayTickEvent)
        displayTick = 0
      else:
        tickEvent = events.TickEvent(pygame.event.get())
        self.eventManager.post(tickEvent)
      pygame.event.pump()
      while pygame.time.get_ticks() - startTick < TURN_TICKS:
        #Using sleep doesn't busy wait, but the system is less responsive
        time.sleep(SLEEP_DELAY)
        #pygame.time.delay(DELAY)

  ##\brief listen for events posted to the event manager
  ##
  ##\param event the event that was posted
  ##\return None

  def notify ( self, event ):
    if isinstance(event,events.QuitEvent):
      self.gameLoop = False
