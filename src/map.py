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

import sys
import os
import pygame
import immobile
import barrier
import errors
import character
import monstergenerator
import exit
import item
from config import *

# This is causing a warning when the game starts.
nextid=4

##\namespace Map
##\brief Map class. Responsible for parsing map files
##
##Main Map Class. Will input a map file or description
##and generate map cells for use in the game Gauntlet

class Map:
#  """
#  Map Class...Responsible for parsing the map file or map description from
#              elsewhere
#  """
#
# this should be included above the class definition somewhere
#

  ##\brief Constructor.
  ##
  ##\param filename The filename of the map to load
  ##\return None

  def __init__ ( self, filename ):
    # Class variables
    self.immobileList = pygame.sprite.RenderPlain()
    self.doorList = pygame.sprite.RenderPlain()
    orig = (TILE_SIZE, TILE_SIZE)

    self.startList = [orig for i in range(MAX_PLAYERS + 1)]
    self.monsterList = pygame.sprite.RenderPlain()
    
    # Attempt to load the map file
    try:
      fullName = filename
      mapFile = open(fullName)
    except:
      raise TypeError, "Map file %s could not be loaded."%filename

    # Read the lines of the map file
    mapLines = mapFile.readlines()
    mapStarted = False
    lineNum = 1
    x = 0
    y = 0

    # Parse each line separately
    for line in mapLines:
      # Check if we have started reading the map tiles
      if mapStarted:
        #try:
          x = 0
          for tile in line.split():
            if tile[0] == '*':
              newWall = barrier.Barrier((x,y))
              self.immobileList.add( newWall )
            elif tile == '.':
              pass
            elif tile == 'D':
              newDoor = barrier.Door((x,y))
              self.doorList.add( newDoor )
              self.immobileList.add( newDoor )
            elif tile[0] == 'P':
              #set the starting point
              if tile[1] == '#':
                self.startList[0] = [ x, y ]
                for startPos in range(len(self.startList)):
                  if self.startList[startPos] == orig:
                    self.startList[startPos] = [ x, y ]
              else:
                self.startList[int(tile[1])] = [ x, y ]
            elif tile[0] == '!':
              # Powerup
              newItem = item.Item([x,y],int(tile[1]))
              self.immobileList.add(newItem)
              
            elif tile[0] == 'M':
              # Monster
              global nextid
              nextid += 1
              self.monsterList.add \
              (character.Character([x,y],MONSTER_CLASS + int(tile[1]),nextid))
                
            elif tile[0] == 'G':
              # Generator
              global nextid
              nextid += 1
              genLevel = 3
              newGenerator = monstergenerator.MonsterGenerator\
                             ([x,y],GENERATOR_CLASS + int(tile[1]), \
                              genLevel, nextid)
              self.monsterList.add(newGenerator)
              
              
            elif tile[0] == 'X':
              # Exit or teleporter
              if tile[1] == '0':
                #teleporter
                pass
              else:
                #exit
                newExit = exit.Exit([x,y],int(tile[1]))
                self.immobileList.add(newExit)
              pass
            else:
              #default to clear for now
              pass
            x += TILE_SIZE
          y += TILE_SIZE
        #except:
          pass

      elif line.startswith('author'):
        self.author = line[7:-2]
      else:
        # Try to get the map size
        try:
          lineList = line.split()
          self.width = int(lineList[0])
          self.height = int(lineList[1])
          mapStarted = True
        except ValueError:
          mapStarted = False
      # Keep track of the line number for error messages
      lineNum += 1

  ##\brief returns a list of sprites
  ##
  ##\param None
  ##\return sprites A list of sprites
  def getImmobiles (self):
    return self.immobileList

  ##\brief returns a list of starting positions
  ##
  ##\param None
  ##\return startList A list of starting positions indexed by player number
  def getStartList (self):
    return self.startList

  ##\brief returns a list of doors
  ##
  ##\param None
  ##\return sprites A list of doors
  def getDoors (self):
    return self.doorList

  ##\brief returns a list of monster sprites
  ##
  ##\param None
  ##\return sprites A list of monster sprites
  def getMonsterList(self):
    return self.monsterList
  
  ##\brief returns the width of the map
  ##
  ##\param None
  ##\return width The width in pixels
  def getWidth (self):
    return self.width

  ##\brief returns the height of the map
  ##
  ##\param None
  ##\return width The height in pixels
  def getHeight (self):
    return self.height

  ##\brief Overloaded string function
  ##
  ##\param None
  ##\return The actual map list
  def __str__ ( self ):
    return self.__map
