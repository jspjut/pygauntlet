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
import immobile
from config import *


##\brief A barrier in the game
##
##Represents a barrier in the game

class Barrier ( immobile.Immobile ):

  ##\brief Barrier constructor
  ##
  ##\param initPosition A list (x,y) representing the barrier's inital position
  ##\return None

  def __init__ ( self, initPosition ):
    immobile.Immobile.__init__(self, initPosition)


##\brief A door in the game
##
##Represents a door in the game

class Door ( Barrier ):

  ##\brief Door constructor
  ##
  ##\param initPosition A list (x,y) representing the door's inital position
  ##\return None

  def __init__ ( self, initPosition ):
    self.type = 25
    self.open = False
    immobile.Immobile.__init__(self, initPosition)
