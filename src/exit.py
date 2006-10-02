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

import barrier
from config import *


##\brief exit out of a maze, and goto the next level(new maze)
##


class Exit ( barrier.Barrier ):

  ##\brief Exit constructor
  ##
  ##\param initPosition A list (x,y) representing the 
  ##\param genType Integer representing the type of genereated monsters
  ##\param level The level number of the monster generator
  ##\return None

  def __init__ ( self, initPosition, level ):
    barrier.Barrier.__init__(self,initPosition)
    self.level = level
