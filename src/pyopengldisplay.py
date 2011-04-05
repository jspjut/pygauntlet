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
#PyGauntlet is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with PyGauntlet; if not, write to the Free Software
#Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


# A try at a new pyopengl display
#
# There is still a lot of work that needs to be done, but this is a start.
# Right now it renders maps using the map module.
# Done:
#   load images using display functions
#   Connect to the game receiving events
#   provide for moving images
#   remove images when they die
# TODO:
#   fix starting location
#   make the floor size match the map being loaded
#   generally optimize for speed
#   etc.

import os
import math
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame, pygame.image
from pygame.locals import *

import map
from display import loadConfig, ImageChooser
import display
import skin
import exit
import item
import barrier
import events
import textdisplay
from config import *

# These rotation variables are only used when this script is run
# by itself for testing
xrot = yrot = 0.0
xspeed = yspeed = 0.0
#z = 10.0
#x = 0.0
#y = 0.0
filter = 0
light = 0
blend = 0
cull = 0
# This is the light
# There is something wrong with the normals of the walls right now.
LightAmbient  = ( (0.5, 0.5, 0.5, 1.0) );
LightDiffuse  = ( (0.7, 0.7, 0.7, 1.0) );
LightPosition = ( (0.0, 0.0, 5.0, 1.0) );


# This is the global list of textures to only load the textures once.
textures = []
# This if is to clip things that are too far away in the draw function.
# The distance is the number of squares away
CLIP_DISTANCE = 17


class PygameDisplay( display.Display ):
  def __init__(self, eventManager = None, options = None):
    if eventManager != None:
      displayFlags = OPENGL|DOUBLEBUF
      display.Display.__init__(self, eventManager, options, displayFlags)

    # This is global so that functions in this file can see it
    global verbose
    if options != None:
      verbose = self.options.verbose

    # Set up the initial view point
    # The x and y values are set by the character locations
    # The z value is how high above the floor the camera is
    self.z = 25.0
    #self.x = 0.0
    #self.y = 0.0

    # This section needs to be replaced with data from the actual level loaded.
    # This should also probably happen at the start game event.
    m = map.Map(os.path.join('data','map','level10.map'))
    # Get the width and height for tiles
    self.mapWidth = m.getWidth()
    self.mapHeight = m.getHeight()

    # items is separate from blocks to draw them in the right order
    self.mobiles = []
    self.blocks = []
    self.items = []
    self.buildSprites([], m.getImmobiles().sprites(),[])
    # I'm not sure why we need this, but to run alone, these can't
    # be passed as parameters to the buildSprites function.
    for i in m.getMonsterList().sprites():
      self.mobiles.append(Mobile(i))
    for s in m.getStartList():
      self.mobiles.append(Mobile(i))

    # Center on Starting Position (needs work)
    s = m.getStartList()
    self.x = s[1][0]/16.0
    self.y = -s[1][1]/16.0
    if self.options.verbose:
      print s
      print s[1]
      print self.x, self.y

    # Setup the text display
    textSize = (RESOLUTION[0]/4,RESOLUTION[1])
    textLocationY = RESOLUTION[0]/4*3
    self.text = textdisplay.TextDisplay( self, self.eventManager, \
                                         textSize, textLocationY )
    self.textTexture = glGenTextures(1)
    pass
  

  def buildSprites( self, chars, immobiles, mobiles ):
    del(self.blocks)
    del(self.mobiles)
    del(self.items)
    self.blocks = []
    self.mobiles = []
    self.items = []
    if self.options.verbose:
      print "Map is %dx%d"%(self.mapWidth,self.mapHeight)
    self.floor = Floor(2*self.mapWidth, 2*self.mapHeight)
    for i in immobiles:
      if isinstance(i, item.Item):
        self.items.append(Immobile(i))
      else:
        self.blocks.append(Immobile(i))
    for i in chars:
      self.mobiles.append(Mobile(i))
    for i in mobiles:
      self.mobiles.append(Mobile(i))
  
  def resize(self, (width, height)):
    if height==0:
      height=1.0
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    self.width = width
    self.height = height
    yratio = 1.0*height/width
    glFrustum(-1.0, 1.0, -1.0*yratio, 1.0*yratio, 2, 80.0)
#    gluPerspective(45, 1.0*width/height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

  def init(self):
    glEnable(GL_TEXTURE_2D)
    #self.load_textures()
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glLightfv( GL_LIGHT1, GL_AMBIENT, LightAmbient )
    glLightfv( GL_LIGHT1, GL_DIFFUSE, LightDiffuse )
    glLightfv( GL_LIGHT1, GL_POSITION, LightPosition )
    glEnable( GL_LIGHT1 )
    glEnable(GL_LIGHTING)
    # Might want to change this
    glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )

    # set desired features
    glEnable(GL_BLEND)
    glCullFace(GL_FRONT)


  def drawText(self):
    # Get to normalized viewport
    glDisable(GL_LIGHTING)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, RESOLUTION[0], 0, RESOLUTION[1], 4, -4)
    glClear(GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glBindTexture(GL_TEXTURE_2D, self.textTexture)
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
    image = self.text.image.convert()
    textureData = pygame.image.tostring(image, "RGB", 1)
    glTexImage2D( GL_TEXTURE_2D, 0, GL_RGB, image.get_width(), image.get_height(), 0,
                  GL_RGB, GL_UNSIGNED_BYTE, textureData )

    # Now that we have a texture from the surface let's map it to a square
    glEnable(GL_CULL_FACE)
    glColor4f(1,1,1,0)

    glBegin(GL_QUADS)

    glNormal3f(0.0, 0.0, 1.0)
    rect = self.text.rect
    # These labels are wrong, but who cares?
    glTexCoord2f(1.0, 1.0); glVertex3f(rect.right, rect.bottom,  -.50)	# Bottom Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0); glVertex3f(rect.right, rect.top   ,  -.50)	# Top Left Of The Texture and Quad
    glTexCoord2f(0.0, 0.0); glVertex3f(rect.left , rect.top   ,  -.50)	# Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f(rect.left , rect.bottom,  -.50)	# Bottom Right Of The Texture and Quad

    glEnd();

    glEnable(GL_DEPTH_TEST)
    glDisable(GL_BLEND)
    glDisable(GL_CULL_FACE)
    glColor4f(1,1,1,1)

    # Reset the projection mode for regular objects
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    yratio = 1.0*self.height/self.width
    glFrustum(-1.0, 1.0, -1.0*yratio, 1.0*yratio, 2, 80.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_LIGHTING)

  def draw(self):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    # Set the viewing angle
    eyey = self.y - self.z / math.sqrt(3)
    gluLookAt(self.x, eyey, self.z, \
             self.x, self.y, 0, \
             0, 1, 0)

    # Update Torch
    LightPosition = ( (self.x, self.y, 5.0, 1.0) );
    glLightfv( GL_LIGHT1, GL_POSITION, LightPosition )

    # Some of the following is for running this in test mode only
    global xrot, yrot, xspeed, yspeed
    glRotatef(xrot, 1.0, 0.0, 0.0)
    glRotatef(yrot, 0.0, 1.0, 0.0)

    # Draw the shapes
    self.floor.draw()
    for b in self.blocks:
      if self.distance(b) < CLIP_DISTANCE:
        b.draw()
    for b in self.items:
      if self.distance(b) < CLIP_DISTANCE:
        b.draw()
    for b in self.mobiles:
      b.move()
      if self.distance(b) < CLIP_DISTANCE:
        b.draw()

    # This only does anything when this script is run for testing
    xrot += xspeed
    yrot += yspeed


  # This function provides for better clipping
  def distance(self, b):
    #print "(%d-%d)^2 + (%d-%d)^2"%(self.x, b.loc[0], self.y, b.loc[1])
    #return (self.x - b.loc[0])**2+(self.y + b.loc[1])**2
    return math.hypot(self.x - b.loc[0], self.y + b.loc[1])
    

  def notify ( self, event ):
    if isinstance( event, events.CharacterMoveEvent ):
      # This should actually move the character and not just the viewpoint
      # This just centers the camera on the spot where the player is standing
      if event.character.classType in PLAYERS:
        self.x = event.character.rect.centerx / 16.0
        self.y = -event.character.rect.centery / 16.0
      pass
    elif isinstance( event, events.ToggleFullscreenEvent ):
      if self.fullscreen:
        self.fullscreen = False
        self.displayFlags = self.displayFlags & ~FULLSCREEN
      else:
        self.fullscreen = True
        self.displayFlags = self.displayFlags | FULLSCREEN
      # The textures should be reloaded here
      self.screen = pygame.display.set_mode(RESOLUTION,self.displayFlags)
      self.resize(RESOLUTION)
      self.init()
      pygame.display.flip()
    elif isinstance( event, events.StartGameEvent ):
      if self.options.verbose:
        print 'Starting display...'
      # Clear the texture cache
      global __TEXTURES__
      __TEXTURES__ = {}
      Block.textures = {}
      # Load the images and locations of everything
      self.buildSprites(event.characters, event.immobiles, event.mobiles)
      self.resize(RESOLUTION)
      self.init()
      pygame.display.flip()
    elif isinstance( event, events.MobileDie ):
      self.mobiles = [i for i in self.mobiles if i.mobile != event.mobile]
    elif isinstance( event, events.ItemPickUp ):
      self.items = [i for i in self.items if i.immobile != event.item]
    elif isinstance( event, events.DoorOpen ):
      self.blocks = [i for i in self.blocks if i.immobile != event.door]
    elif isinstance( event, events.MobilePlaceEvent ):
      self.mobiles.append(Mobile(event.mobile))
    elif isinstance( event, events.AddProjectile ):
      self.mobiles.append(Mobile(event.proj))
    elif isinstance( event, events.DisplayTickEvent ):
      #update items
      for i in self.items:
        i.update_loc()
      self.draw()
      self.drawText()
      pygame.display.flip()

class Block:
  textures = {}
  def __init__(self, texture = None):
    self.locz = 0
    self.float = False
    self.animz = 0.03
    self.maxz = 0.5
    #self.loc should already be set
    self.update_loc()
    if texture == None:
      self.loadTexture()
    else:
      self.texture = texture

  def update_loc(self):
    self.loc0m = self.loc[0]-1.0
    self.loc0p = self.loc[0]+1.0
    self.loc1m = -self.loc[1]-1.0
    self.loc1p = -self.loc[1]+1.0
    #floating animation
    if self.float:
      self.locz = self.locz + self.animz
      if self.locz >= self.maxz or self.locz <= 0:
        self.animz = -self.animz
        self.locz = self.locz + self.animz

  def loadTexture(self):
    self.texture = None

  def draw_sprite(self):
    glBindTexture(GL_TEXTURE_2D, self.texture)

    if isinstance(self, Mobile):
      glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP )
      glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP )
    else:
      glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT )
      glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT )
    
    if not isinstance(self, Floor):
      glEnable(GL_BLEND)
      glDisable(GL_DEPTH_TEST)
    else:
      glEnable(GL_CULL_FACE)
      glColor4f(.25,.25,.25,0)

    glBegin(GL_QUADS)
	
    glNormal3f(0.0, 0.0, 1.0)
    glTexCoord2f(0.0, 0.0); glVertex3f(self.loc0m, self.loc1m, self.locz)	# Bottom Left Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f(self.loc0m, self.loc1p, self.locz)	# Top Left Of The Texture and Quad
    glTexCoord2f(1.0, 1.0); glVertex3f(self.loc0p, self.loc1p, self.locz)	# Top Right Of The Texture and Quad
    glTexCoord2f(1.0, 0.0); glVertex3f(self.loc0p, self.loc1m, self.locz)	# Bottom Right Of The Texture and Quad

    glEnd();

    glEnable(GL_DEPTH_TEST)
    glDisable(GL_BLEND)
    glDisable(GL_CULL_FACE)
    glColor4f(1,1,1,1)

  def draw(self):
    glBindTexture(GL_TEXTURE_2D, self.texture)
    
    try:
      if isinstance(self.immobile, barrier.Barrier):
        pass
      else:
        self.draw_sprite()
        return
    except:
      self.draw_sprite()
      return # return here to draw only one surface (top)

    # Culling enabled here to prevent drawing unnecessary faces.
    glEnable( GL_CULL_FACE )
    glColor4f(.5,.5,.5,1)

    #This is a repeat of the bottom with oposite facing for culling
    glBegin(GL_QUADS)
	
    glNormal3f(0.0, 0.0, -1.0)
    glTexCoord2f(0.0, 1.0); glVertex3f(self.loc0m, self.loc1p,  -1.0)	# Top Left Of The Texture and Quad
    glTexCoord2f(0.0, 0.0); glVertex3f(self.loc0m, self.loc1m,  -1.0)	# Bottom Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0); glVertex3f(self.loc0p, self.loc1m,  -1.0)	# Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0); glVertex3f(self.loc0p, self.loc1p,  -1.0)	# Top Right Of The Texture and Quad

    glEnd();
    glBegin(GL_QUADS)
    # Back Face
    glNormal3f(0.0, 0.0, 1.0)
    glTexCoord2f(0.0, 0.0); glVertex3f(self.loc0m, self.loc1m, 1.0)	# Bottom Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f(self.loc0m, self.loc1p, 1.0)	# Top Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0); glVertex3f(self.loc0p, self.loc1p, 1.0)	# Top Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0); glVertex3f(self.loc0p, self.loc1m, 1.0)	# Bottom Left Of The Texture and Quad
	
    glEnd();
    glBegin(GL_QUADS)
    # Top Face
    glNormal3f(0.0, -1.0, 0.0)
    glTexCoord2f(1.0, 1.0); glVertex3f(self.loc0m, self.loc1p,  1.0)	# Bottom Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0); glVertex3f(self.loc0m, self.loc1p, -1.0)	# Top Left Of The Texture and Quad
    glTexCoord2f(0.0, 0.0); glVertex3f(self.loc0p, self.loc1p, -1.0)	# Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f(self.loc0p, self.loc1p,  1.0)	# Bottom Right Of The Texture and Quad
	
    glEnd();
    glBegin(GL_QUADS)
    # Bottom Face
    glNormal3f(0.0, 1.0, 0.0)
    glTexCoord2f(1.0, 0.0); glVertex3f(self.loc0p, self.loc1m, -1.0)	# Top Left Of The Texture and Quad
    glTexCoord2f(0.0, 0.0); glVertex3f(self.loc0m, self.loc1m, -1.0)	# Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f(self.loc0m, self.loc1m,  1.0)	# Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0); glVertex3f(self.loc0p, self.loc1m,  1.0)	# Bottom Left Of The Texture and Quad
	
    glEnd();
    glBegin(GL_QUADS)
    # Right face
    glNormal3f(-1.0, 0.0, 0.0)
    glTexCoord2f(1.0, 0.0); glVertex3f(self.loc0p, self.loc1p, -1.0)	# Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 0.0); glVertex3f(self.loc0p, self.loc1m, -1.0)	# Bottom Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f(self.loc0p, self.loc1m,  1.0)	# Bottom Left Of The Texture and Quad
    glTexCoord2f(1.0, 1.0); glVertex3f(self.loc0p, self.loc1p,  1.0)	# Top Left Of The Texture and Quad
	
    glEnd();
    glBegin(GL_QUADS)
    # Left Face
    glNormal3f(1.0, 0.0, 0.0)
    glTexCoord2f(1.0, 1.0); glVertex3f(self.loc0m, self.loc1m,  1.0)	# Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 0.0); glVertex3f(self.loc0m, self.loc1m, -1.0)	# Bottom Left Of The Texture and Quad
    glTexCoord2f(0.0, 0.0); glVertex3f(self.loc0m, self.loc1p, -1.0)	# Top Left Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f(self.loc0m, self.loc1p,  1.0)	# Top Right Of The Texture and Quad
	
    glEnd();				

    glColor4f(1,1,1,1)
    glDisable(GL_CULL_FACE)


# A tiled floor of the size x, y
class Floor (Block):
  def __init__(self, x, y):
    self.loc = (x/2.0, y/2.0)
    Block.__init__(self)

  # This function is rewriten to make the floor the right size
  def update_loc(self):
    # Should reall be changed to be the size of the map
    self.loc0m = -1
    self.loc0p = self.loc[0]*2+1
    self.loc1m = -self.loc[1]*2-1
    self.loc1p = 1

  def draw_sprite(self):
    glBindTexture(GL_TEXTURE_2D, self.texture)
    
    glEnable(GL_CULL_FACE)
    glColor4f(.25,.25,.25,0)

    glBegin(GL_QUADS)
	
    glNormal3f(0.0, 0.0, 1.0)
    glTexCoord2f(0.0, 0.0); glVertex3f(self.loc0m, self.loc1m,  -1.0)	# Bottom Left Of The Texture and Quad
    glTexCoord2f(0.0, self.loc[1]); glVertex3f(self.loc0m, self.loc1p,  -1.0)	# Top Left Of The Texture and Quad
    glTexCoord2f(self.loc[0], self.loc[1]); glVertex3f(self.loc0p, self.loc1p,  -1.0)	# Top Right Of The Texture and Quad
    glTexCoord2f(self.loc[0], 0.0); glVertex3f(self.loc0p, self.loc1m,  -1.0)	# Bottom Right Of The Texture and Quad

    glEnd();

    glEnable(GL_DEPTH_TEST)
    glDisable(GL_BLEND)
    glDisable(GL_CULL_FACE)
    glColor4f(1,1,1,1)

  def loadTexture(self):
    fullname = os.path.join('data','skins',skin.SKIN,'background.png')

    #implement singleton method here so images don't get loaded multiple times
    try:
      self.texture = Block.textures[fullname]
    except:
      Block.textures[fullname] = loadTexture(fullname)
      self.texture = Block.textures[fullname]


class Immobile (Block):
  def __init__(self, immobile):
    self.loc = (immobile.rect.centerx/16.0,immobile.rect.centery/16.0)
    self.immobile = immobile
    Block.__init__(self)

  def loadTexture(self):
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
      # Items float
      self.float = True
    elif isinstance(self.immobile, barrier.Door):
      fullname = os.path.join('data','skins',skin.SKIN,'door.png')
    else: #wall
      fullname = os.path.join('data','skins',skin.SKIN,'wall.png')

    #implement singleton method here so images don't get loaded multiple times
    try:
      self.texture = Block.textures[fullname]
    except:
      Block.textures[fullname] = loadTexture(fullname)
      self.texture = Block.textures[fullname]

class Mobile (Block):
  def __init__(self, mobile):
    self.loc = (mobile.rect.centerx/16.0,mobile.rect.centery/16.0)
    self.mobile = mobile
    Block.__init__(self)
    self.exited = False

  def move(self):
    self.loc = (self.mobile.rect.centerx/16.0,self.mobile.rect.centery/16.0)
    self.update_loc()
#    print self.imageList
#    for i in self.imageList:
#      try:
#        print i.getImage()
#      except:
#        print i
    try:
      self.texture = self.imageList[self.mobile.direction].getImage()
    except:
      pass

  def loadTexture(self):
    loadConfig(self, self.mobile.classType, loadFunc = loadTexture)
    self.texture = self.imageList[SOUTH].getImage()


def handle_keys(key, disp):
  global filter, light, xspeed, yspeed, blend, cull

  if key == K_ESCAPE:
    return 0
  if key == K_f:
    filter = filter + 1
    if filter == 3:
      filter = 0
#  elif key == K_c:
#    cull = not cull
#    if cull:
#      glEnable( GL_CULL_FACE )
#      glCullFace( GL_FRONT )
#    else:
#      glDisable( GL_CULL_FACE )
  elif key == K_l:
    light = not light
    if not light:
      glDisable(GL_LIGHTING)
    else:
      glEnable(GL_LIGHTING)
#  elif key == K_b:
#    blend = not blend
#    if blend:
#      glEnable(GL_BLEND)
#      glDisable(GL_DEPTH_TEST)
#    else:
#      glEnable(GL_DEPTH_TEST)
#      glDisable(GL_BLEND)
  elif key == K_a:
    disp.x -= 1.0
  elif key == K_d:
    disp.x += 1.0
  elif key == K_w:
    disp.y += 1.0
  elif key == K_s:
    disp.y -= 1.0
  elif key == K_PAGEUP:
    disp.z -= 5.00
  elif key == K_PAGEDOWN:
    disp.z += 5.00
  elif key == K_UP:
    xspeed -= 0.05
  elif key == K_DOWN:
    xspeed += 0.05
  elif key == K_LEFT:
    yspeed -= 0.05
  elif key == K_RIGHT:
    yspeed += 0.05

  return 1

##\brief Loads an image
##
##Loads an image as a texture using the filename and its path
##
##\param fullname Filename and its path to the image
##\return None
__TEXTURES__ = {}
def loadTexture ( fullname ):
  global verbose
  #Try to return an already loaded image
  try:
    return __TEXTURES__[fullname]
  except:
    pass
  #Load the image
  try:
    if verbose:
      print fullname, 'loading...'
    image = pygame.image.load(fullname)
    __TEXTURES__[fullname] = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, __TEXTURES__[fullname])
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
    if image.get_alpha() is None:
      image = image.convert()
      textureData = pygame.image.tostring(image, "RGB", 1)
      glTexImage2D( GL_TEXTURE_2D, 0, GL_RGB, image.get_width(), image.get_height(), 0,
                    GL_RGB, GL_UNSIGNED_BYTE, textureData )
    else:
      #image = image.convert_alpha()
      textureData = pygame.image.tostring(image, "RGBX", 1)
      glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, image.get_width(), image.get_height(), 0,
                    GL_RGBA, GL_UNSIGNED_BYTE, textureData )
  except pygame.error, message:
    print 'Cannot load image:', '"'+fullname+'"'
    raise SystemExit, message
  except:
    print 'Cannot load image:', '"'+fullname+'"'
  return __TEXTURES__[fullname]



# This function is for testing purposes only. It only gets called when
# this script is run by itself.
# Right now this is broken for some reason, something to do with options
def main():

  video_flags = OPENGL|DOUBLEBUF|FULLSCREEN
  resolution = (800,600)

  pygame.init()
  surface = pygame.display.set_mode(resolution, video_flags)

  #skin.SKIN = 'pacman'
  disp = PygameDisplay()

  disp.resize(resolution)
  disp.init()

  frames = 0
  ticks = pygame.time.get_ticks()
  while 1:
    event = pygame.event.poll()
    if event.type == QUIT:
      break
    if event.type == KEYDOWN:
      if handle_keys(event.key, disp) == 0:
        break

    disp.draw()
    pygame.display.flip()
    frames = frames+1

  print "fps:  %d" % ((frames*1000)/(pygame.time.get_ticks()-ticks))


if __name__ == '__main__': main()
