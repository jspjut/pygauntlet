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
  import events
  import errors
  import skin
  from config import *
  from pygame.locals import *
except ImportError, err:
  print "display.py: could not load module. %s"%(err)
  sys.exit(2)


##\brief A generic display class
##
##Provides the basic interface for a display that can easily
##be extended to allow a pygame or opengl display class to work.

class Display:

##\brief initializes the basic data common to all types of displays
##
##\param eventManager An event manager to listen to
##\param options The options set at the command line
##\param displayFlags The flags to be used when creating the screen
##\return None

  def __init__ ( self, eventManager, options, displayFlags ):
    self.options = options
    self.eventManager = eventManager
    self.eventManager.registerListener(self)
    self.fullscreen = options.fullscreen
    self.displayFlags = displayFlags
    if self.fullscreen:
      displayFlags = self.displayFlags | FULLSCREEN
    else:
      pass
    
    #initialize pygame screen
    self.screen = pygame.display.set_mode(RESOLUTION, displayFlags)
    try:
      fullpath = os.path.join('data','skins',skin.SKIN,'icon.png')
      self.iconImage = loadPng(fullpath)
      pygame.display.set_icon(self.iconImage)
    except:
      # This is not a fatal error, if the skin doesn't have an icon,
      # we just don't enable it.
      pass
    if options.netmaster:
      pygame.display.set_caption("Gauntlet - Server")
    elif options.serveraddr:
      pygame.display.set_caption("Gauntlet - Client")
    else:
      pygame.display.set_caption("Gauntlet")
    pygame.mouse.set_visible(False)

##\brief Handles events
##
##A basic framework that should be used for other display classes
##
##\param event An event sent from the EventManager
##\return None

  def notify ( self, event ):
    if isinstance( event, events.CharacterMoveEvent ):
      pass
    elif isinstance( event, events.StartGameEvent ):
      pass
    elif isinstance( event, events.ToggleFullscreenEvent ):
      if self.fullscreen:
        self.fullscreen = False
        displayFlags = self.displayFlags
      else:
        self.fullscreen = True
        displayFlags = self.displayFlags | FULLSCREEN
      self.screen = pygame.display.set_mode(RESOLUTION,displayFlags)
      pygame.display.update()


##\brief Loads an image
##
##Loads an image using the filename and its path
##
##\param fullname Filename and its path to the image
##\return None

def loadPng ( fullname ):
  try:
    image = pygame.image.load(fullname)
    if image.get_alpha() is None:
      image = image.convert()
    else:
      image = image.convert_alpha()
  except pygame.error, message:
    print 'Cannot load image:', '"'+fullname+'"'
    raise SystemExit, message
  return image


##\brief A class that holds a set of images
##
##Provides the functionality necessary to enable animation of
##sprites on the screen. Every time an image is requested, it
##gives back a different one than the previous time.

class ImageChooser:

##\brief initializes the ImageChooser to have a single image
##
##\param imageFile The full path to the image to load
##\param loadFunc The function to use to load the images
##\return None
  def __init__(self, imageFile, loadFunc = loadPng):
    self.loadFunc = loadFunc
    self.imageList = []
    self.imageList.append(self.loadFunc(imageFile))
    self.next = 0

##\brief Chooses an image from the list
##
##\param None
##\return image An image ready to display
  def getImage(self):
    length = len(self.imageList)
    if length == 1:
      return self.imageList[0]
    else:
      # Increment the last count
      if self.next >= length:
        self.next = 0
      retImg = self.imageList[self.next]
      self.next += 1
      return retImg

##\brief Add an image to the list
##
##\param imageFile The full path to the image to add
##\return None
  def addImage(self, imageFile):
    self.imageList.append(self.loadFunc(imageFile))


##\brief Loads a config file for a mobile object
##
##Opens the file specified and reads the data that describes the mobile object
##
##\param characterClass Identifies which class the character is
##\param configFilename The filename of the config file (does not appear
##to be in use).
##\return A list of Surfaces to be used for a mobile object

def loadConfig ( self, characterClass, loadFunc = loadPng ):
  fullpath = os.path.join('data','skins',skin.SKIN)
  if characterClass == WARRIOR:
    fullname = os.path.join(fullpath,"warrior.cfg")
  elif characterClass == WIZARD:
    fullname = os.path.join(fullpath,"wizard.cfg")
  elif characterClass == VALKYRIE:
    fullname = os.path.join(fullpath,"valkyrie.cfg")
  elif characterClass == ARCHER:
    fullname = os.path.join(fullpath,"archer.cfg")

  #monsters
  elif characterClass == GHOST:
    fullname = os.path.join(fullpath,"ghost.cfg")
  elif characterClass == GRUNT:
    fullname = os.path.join(fullpath,"grunt.cfg")
  elif characterClass == DEMON:
    fullname = os.path.join(fullpath,"demon.cfg")
  elif characterClass == LOBBER:
    fullname = os.path.join(fullpath,"lobber.cfg")
  elif characterClass == SORCERER:
    fullname = os.path.join(fullpath,"sorce.cfg")
  elif characterClass == DEATH:
    fullname = os.path.join(fullpath,"death.cfg")
  elif characterClass == THIEF:
    fullname = os.path.join(fullpath,"thief.cfg")

  #generators
  elif characterClass == GHOSTGENERATOR:
    fullname = os.path.join(fullpath,'ghostgenbig.cfg')
  elif characterClass == GRUNTGENERATOR:
    fullname = os.path.join(fullpath,'generator.cfg')
  elif characterClass < PROJECTILE:
    fullname = os.path.join(fullpath,'generator.cfg')
  
  #projectiles
  elif characterClass == PROJECTILE_WARRIOR:
    fullname = os.path.join(fullpath,"axe.cfg")
  elif characterClass == PROJECTILE_WIZARD:
    fullname = os.path.join(fullpath,"fireball.cfg")
  elif characterClass == PROJECTILE_VALKYRIE:
    fullname = os.path.join(fullpath,"sword.cfg")
  elif characterClass == PROJECTILE_ARCHER:
    fullname = os.path.join(fullpath,"arrow.cfg")
  elif characterClass == PROJECTILE_OTHER:
    fullname = os.path.join(fullpath,"fireball.cfg")
  else:
    fullname = os.path.join(fullpath,"archer.cfg")
  
  try:
    skinfile = open(fullname)
  except IOError, message:
    print 'Cannot load skin :', fullname

  # Make sure that the image list is the right size (9)
  try:
    if len(self.imageList) == 9:
      pass
  except:    
    self.imageList = [0,0,0,0,0,0,0,0,0]

  # Get the images
  # When adding animation to the images, we should look here.
  try:
    skinlines = skinfile.readlines()
    if skinlines[0].strip() == "float":
      self.float = True
      skinlines = skinlines[1:]
    if len(skinlines) == 8:
      for i in xrange(8):
        self.imageList[i+1] = ImageChooser(os.path.join(fullpath,skinlines[i].strip()), loadFunc)
    else:
      # loop until there is a ';' to end a line meaning next direction
      direc = NORTH
      for line in skinlines:
        try:
          self.imageList[direc].addImage(os.path.join(fullpath,line.strip().strip(';')))
        except:
          self.imageList[direc] = ImageChooser(os.path.join(fullpath,line.strip().strip(';')), loadFunc)
        if line.strip().endswith(';'):
          direc = direc + 1
        
  except IOError, message:
    print 'Cannot load images :', fullname
    raise SystemExit, message

  # Close the file
  skinfile.close()
    


##\brief Renders some text
##
##Renders the text passed in to be displayed
##
##\param text The text to render
##\param fontsize The size of the font to render
##\param color The color of the text to render
##\return renderedText The rendered text to display

def renderText ( text, fontsize, color ):
  font = pygame.font.Font(None, fontsize)
  text = font.render(text, 5, color )
  textpos = text.get_rect()
  return text, textpos
