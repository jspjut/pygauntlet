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
  import os
  import pygame
  from pygame.locals import *
  import events
  import errors
  import skin
  from config import *
  import soundList
except ImportError, err:
  print 'sound.py: could not load module. %s'%(err)
  sys.exit(2)


class SoundEngine:

  def __init__ ( self, eventManager ):
    try:
      pygame.mixer.init()
      self.eventManager = eventManager
      self.eventManager.registerListener(self)
      self.keySound = True
      musicFile = os.path.join('data','skins',skin.SKIN,'music.cfg')
      self.music = soundList.SoundList(musicFile)
      almostDeadFile = os.path.join('data','skins',skin.SKIN,'atd.cfg')
      self.almostDead = soundList.SoundList(almostDeadFile)
    except pygame.error:
      print 'Sound disabled.'
      pass

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

##\brief Choose the sound for the character
##
##Chooses the sound based on the character's class
##
##\param charac The character whose class to look at
##\return fullname Filename and its path to the sound file
  def getClassSound ( self, charac ):
    if charac.classType == ARCHER:
      return os.path.join('data','skins',skin.SKIN,'elf.wav')
    elif charac.classType == WARRIOR:
      return os.path.join('data','skins',skin.SKIN,'warrior.wav')
    elif charac.classType == WIZARD:
      return os.path.join('data','skins',skin.SKIN,'wizard.wav')
    elif charac.classType == VALKYRIE:
      return os.path.join('data','skins',skin.SKIN,'valkyrie.wav')
    else:
      return ''

##\brief Handles events
##
##A basic framework that should be used for other display classes
##
##\param event An event sent from the EventManager
##\return None

  def notify ( self, event ):
    soundfile = ''
    if isinstance( event, events.MobileDie ):
      if event.mobile.classType in PLAYERS:
        soundfile = os.path.join('data','skins',skin.SKIN,'playerdie.wav')
      elif event.mobile.classType in MONSTERS:
        soundfile = os.path.join('data','skins',skin.SKIN,'monsterdie.wav')

    elif isinstance( event, events.StartGameEvent ):
      #maybe load some background music
      pygame.mixer.stop()
      #soundfile = os.path.join('data','skins',skin.SKIN,'Gauntlet1(short).ogg')
      sound = self.music.getNext()
      sound.play(-1)
      #load the player welcome sounds
      try:
        welcomefile = os.path.join('data','skins',skin.SKIN,'welcome.wav')
        welcomesound = self.loadSound(welcomefile)
        welcomechannel = welcomesound.play()
        #should check for character class here
        charac = event.characters.sprites()[0]
        soundfile = self.getClassSound(charac)
        if soundfile != '' and welcomechannel:
          welcomesound = self.loadSound(soundfile)
          welcomechannel.queue(welcomesound)
      except:
        pass
      soundfile = ''

    # This section of code looks extra buggy. I'm commenting it out
    # until I have a chance to fix it
    elif isinstance( event, events.AbouttoDie ):
#      classfile = self.getClassSound(event.mobile)
#      # This uses a channel to play both sounds
#      if classfile != '':
#        #soundfile = os.path.join('data','skins',skin.SKIN,'IATD.wav')
#        classsound = self.loadSound(classfile)
#        diesound = self.almostDead.getNext()
#        channel = classsound.play()
#        if channel:
#          diesound = self.loadSound(soundfile)
#          channel.queue(diesound)
      soundfile = ''

    elif isinstance( event, events.ItemPickUp ):
      if self.keySound and event.item.type == KEY:
        soundfile = os.path.join('data','skins',skin.SKIN,'UKTOD.wav')
        self.keySound = False
      else:
        soundfile = os.path.join('data','skins',skin.SKIN,'itempickup.wav')
      
    elif isinstance( event, events.DoorOpen ):
      soundfile = os.path.join('data','skins',skin.SKIN,'dooropen.wav')
      
    elif isinstance( event, events.CharacterMagicAttack ):
      soundfile = os.path.join('data','skins',skin.SKIN,'magic.wav')
      
    elif isinstance( event, events.AddProjectile ):
      if event.proj.classType in PLAYER_PROJECTILES:
        soundfile = os.path.join('data','skins',skin.SKIN,'playershoot.wav')
      else:
        soundfile = os.path.join('data','skins',skin.SKIN,'monstershoot.wav')
    elif isinstance( event, events.GameOverEvent ):
      # I changed this because this file was in the wrong place.
      #soundfile = os.path.join('data','sound','gameover.wav')
      soundfile = ''
    if soundfile != '':
      sound = self.loadSound(soundfile)
      if pygame.mixer:
        sound.play()
