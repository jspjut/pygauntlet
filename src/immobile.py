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
  import config
except ImportError, err:
  print "couldn't load module. %s" % (err)
  sys.exit(2)


##\brief An immobile object in the game (virtual class)
##
##Represents an immobile object in the game.
##Includes all objects that cannot move in the game.

class Immobile ( pygame.sprite.Sprite ):

  ##\brief Immobile constructor
  ##
  ##\return None

  def __init__ ( self, initPosition ):
    pygame.sprite.Sprite.__init__(self)
    self.rect = pygame.Rect(initPosition,[config.TILE_SIZE,config.TILE_SIZE])
