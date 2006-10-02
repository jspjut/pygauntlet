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
try:
  import map
  import mapgenerate
except ImportError, err:
  print "Could not load module. %s" % (err)
  sys.exit(2)

MAP_SIZE = 35


# A class to keep track of which map to load next
class MapLoader:

  # Gets the mapList from a file, or a single map
  def __init__ ( self, mapList ):
    if mapList is None:
      self.mapList = []
    elif mapList.endswith(".map"):
      self.mapList = [mapList]
    else:
      try:
        mapFile = open(mapList)
        tempMapList = mapFile.readlines()
        self.mapList = []
        for m in tempMapList:
          self.mapList.append(m.strip())
      except:
        print 'Error opening %s, using random maps.' % (mapList)
        self.mapList = []
    # Reverse the list so that we start popping at the front
    self.mapList.reverse()
    self.currentLevel = 1

  # Loads the next map in the list or loads a random map
  def nextMap ( self, currentLevel ):
    random = False
    if len(self.mapList) > 0:
      fullpath = os.path.join('data','map',self.mapList.pop())
      try:
        nextMap = map.Map(fullpath)
      except:
         random = True
    else:
      random = True
    if random:
      mapgenerator = mapgenerate.MapGenerator(MAP_SIZE)
      mapgenerator.createMap('random.map')
      fullpath = os.path.join('data','map','random.map')
      nextMap = map.Map(fullpath)
    self.currentLevel += 1
    return nextMap
