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

import os
import random
import pygame

##\brief Keeps track of a sound list
##
##Keeps a group of sound files in a list and returns them one at a time

class SoundList:

  def __init__ ( self, filename ):
    self.lastSound = None
    self.sounds = []
    if filename.endswith('.cfg'):
      contents = open(filename).readlines()
      self.sounds = contents
    else:
      self.sounds.append(filename)
    # Choose the sounds
    i = 0
    for sound in self.sounds:
      self.sounds[i] = self.loadSound(os.path.join('data','sound',sound.strip()))
      i = i + 1

##\brief Chooses a sound
##
##Chooses a sound randomly from the list
##
##\param None
##\return Sound

  def getNext( self ):
    if len(self.sounds) == 1:
      return self.sounds[0]
    nextSound = self.sounds[random.randrange(len(self.sounds))]
    while nextSound == self.lastSound:
      nextSound = self.sounds[random.randrange(len(self.sounds))]
    self.lastSound = nextSound
    return nextSound

##\brief Loads a sound
##
##Loads a sound using the filename and its path
##
##\param fullname Filename and its path to the sound file
##\return None

  def loadSound ( self, fullname ):
    class NoneSound:
      def play(self,loop=0):
        pass
    if not pygame.mixer or not pygame.mixer.get_init():
      return NoneSound()
    try:
      sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
      print 'Cannot load sound:', fullname
      raise SystemExit, message
    return sound
