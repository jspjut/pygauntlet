#!/usr/bin/env python
#
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


def initGame(options):
  global cpuController
  global theGame
  global soundEngine
  global systemController


  #setup the event manager
  eventManager = eventmanager.EventManager(options)

  #setup the components
  theGame = game.Game(eventManager,options)
  cpuController = cpucontroller.CPUController(eventManager)
  systemController = keyboardcontroller.SystemController(eventManager)

  #call the splash screen function
  menu.splashScreen()

  #calls the character select screen, which posts the addCharacter events
  menu.mainMenuScreen(eventManager,theGame)

  #setup sound
  soundEngine = sound.SoundEngine(eventManager)

  #setup display
  if options.opengl:
    try:
      import pyopengldisplay
      pygamedisplay = pyopengldisplay
      #import pyopengldisplay
      #pygameDisplay = pyopengldisplay.PygameDisplay(eventManager,options)
      #pygameDisplay = pyopengldisplay.PygameDisplay(eventManager, options)
    except:
      import pygamedisplay
  else:
    import pygamedisplay
  pygameDisplay = pygamedisplay.PygameDisplay(eventManager,options)


try:
  import os
  import sys
  sys.path.append('src')
  import pygame
  import optparse
  import eventmanager
  import game
  import cpucontroller
  import keyboardcontroller
  import sound
  import errors
  import display
  import events
  import menu
  import skin
  from config import *
except ImportError, err:
  print "couldn't load module. %s" % (err)
  sys.exit(2)

if not pygame.font:
  print 'Warning, fonts disabled'
if not pygame.mixer:
  print 'Warning, sound disabled'

pygame.init()

def main ( ):
  #setup the command-line options/arguments parser
  usage = "usage: gauntlet.py [options] map"
  parser = optparse.OptionParser(usage)

  #add options
  parser.add_option("-f","--fullscreen",action="store_true",
                    dest="fullscreen",default=False,
                    help="begin the game in full-screen mode")
  parser.add_option("-v","--verbose",action="store_true",
                    dest="verbose",default=False,
                    help="print verbose text output (all events from the event manager")
#  parser.add_option("-o","--opengl",action="store_true",
#                    dest="opengl",default=False,
#                    help="enable OpenGL graphic rendering")
  parser.add_option("-n","--no-opengl",action="store_false",
                    dest="opengl",default=True,
                    help="disable OpenGL graphic rendering (Use Pygame).")
  parser.add_option("-s","--serveraddr",metavar="FILE",
                    dest="serveraddr",default="",
                    help="set server address for network play")
  parser.add_option("-m","--master",action="store_true",
                    dest="netmaster",default=False,
                    help="be the server in network play")

  #parse options/arguments
  options, args = parser.parse_args()
  try:
    options.mapFilename = args[0]
  except IndexError:
    options.mapFilename = os.path.join('data','skins',skin.SKIN,'mapList.cfg')

  initGame(options)
  #run the game
  while not cpuController.run():
    main()

if __name__ == "__main__":
  try:
    import psyco
    psyco.full()
    print 'Running with psyco!'
  except:
    print 'psyco not loaded.'
  try:
    main()
  except errors.Error, message:
    print "error:", message

