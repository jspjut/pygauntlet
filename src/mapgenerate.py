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
import random
from config import *


##
##\brief Cell class.
##
##Cell class is used as part of the MapGenerator
##class to generate a suitable map for the game 
##Gauntlet

class Cell:
  def __init__(self):

    #left wall, right wall, top wall, bottom wall
    self.walls = [True for i in range(4)]
    self.visited = False
    self.x = 0
    self.y = 0


##
##\brief Maze Generate class.
##
##Maze Generate will create a randomly created
##map for use in the game Gauntlet

class MapGenerator :

  ##\brief Constructor.
  ##
  ##\param width. Width of generated map
  ##\param height. Height of generated map
  ##\param fileName. File for map to be written to
  ##\return None

  def __init__ ( self , size):
    self.width = (size -1)/3
    self.height = (size -1)/3

    self.maze = []
    for i in xrange(self.height):
      self.maze.append([])
      for j in xrange(self.width):
        self.maze[i].append(Cell())

   #all cells are first marked as unvisited
    for i in xrange(self.height):
      for j in xrange(self.width):
        self.maze[i][j].visited = False
        self.maze[i][j].x = i
        self.maze[i][j].y = j

    #create a maze from our representation
    self.output_maze = []

    #make everything a * sign first
    for i in xrange(self.width*3 +1):
      self.output_maze.append([])
      for j in xrange(self.height* 3 +1):
        self.output_maze[i].append('*')

  def get_cell(self, x, y):
    return self.maze[x][y]

  ##\brief Generates the maze.
  ##
  ##\return None
  ##This function does the core of the work in generating the
  ##maze correctly
  ##
  def generateMap(self):

    visited = []
    nextCell = False
    validDirection  = [True for i in range(4)]
    numCells = self.width * self.height
    curX = random.randint(0, self.width - 1)
    curY = random.randint(0, self.height- 1)

    while len(visited) < numCells:
      #mark cell we are in as visited
      if self.get_cell(curX,curY).visited == False:
        self.get_cell(curX, curY).visited = True
        visited.append(self.get_cell(curX, curY))

      validDirection = [True for i in range(4)]
      randDir = random.randint(1, 4)
      nextCell = False

      while not nextCell:
        if randDir == NORTH:
          if (curY - 1) < 0 or self.get_cell(curX , curY - 1).visited:
            validDirection[0] = False
            randDir = random.randint(1, 4)
          else:
            #bang out two walls to show a corridor
            self.get_cell(curX, curY).walls[TOP] = False
            self.get_cell(curX , curY - 1).walls[BOTTOM] = False
            nextCell = True
            curY = curY - 1
        elif randDir == SOUTH:
          if (curY + 1) > (self.height - 1) or self.get_cell(curX, curY + 1).visited:
            validDirection[1] = False
            randDir = random.randint(1, 4)
          else:
            #bang out two walls to show a corridor
            self.get_cell(curX, curY).walls[BOTTOM] = False
            self.get_cell(curX, curY + 1).walls[TOP] = False
            nextCell = True
            curY = curY + 1
        elif randDir == EAST:
          if (curX + 1) > (self.width - 1) or self.get_cell(curX + 1, curY).visited:
            validDirection[2] = False
            randDir = random.randint(1, 4)
          else:
            #bang out two walls to show a corridor
            self.get_cell(curX, curY).walls[RIGHT] = False
            self.get_cell(curX + 1, curY ).walls[LEFT] = False
            nextCell = True
            curX = curX + 1
        else:
          if (curX - 1) < 0 or self.get_cell(curX - 1, curY).visited:
            validDirection[3] = False
            randDir = random.randint(1, 4)
          else:
            #bang out two walls to show a corridor
            self.get_cell(curX, curY).walls[LEFT] = False
            self.get_cell(curX - 1, curY).walls[RIGHT] = False
            nextCell = True
            curX = curX - 1

        #check to see if all directions have been checked, if so, move onto another cell
        if False in validDirection:
          nextCell = True
          newCell = visited[random.randint(0, len(visited)- 1)]
          curX = newCell.x
          curY = newCell.y

    self.sparsify()
    self.removeDeadEnds()
    self.addRooms()
  
  ##\brief Sparsify the maze
  ##
  ##\return None
  ##This function will look at the maze and delete spots
  ##that are only met by one corridor. This will be proceeded
  ##by adding rooms to the maze to make it a true dungeon
  ##
  def sparsify(self):
    #how many blocks should be removed
    sparsenessCount = self.height/2
    while True:
      y = random.randint(0, self.height -1)
      x = random.randint(0, self.width -1)
      
      #check if a path has only one corridor, i.e a deadend
      if self.get_cell(x,y).walls.count(False) == 1:
        if not self.get_cell(x,y).walls[TOP]:
          self.get_cell(x,y).walls[TOP] = True
          self.get_cell(x, y-1).walls[BOTTOM] = True
        if not self.get_cell(x,y).walls[BOTTOM]:
          self.get_cell(x,y).walls[BOTTOM] = True
          self.get_cell(x, y + 1).walls[TOP] = True
        if not self.get_cell(x,y).walls[RIGHT]:
          self.get_cell(x,y).walls[RIGHT] = True
          self.get_cell(x + 1, y).walls[LEFT] = True
        if not self.get_cell(x,y).walls[LEFT]:
          self.get_cell(x,y).walls[LEFT] = True
          self.get_cell(x-1, y).walls[RIGHT] = True
           
	sparsenessCount -= 1

        if not sparsenessCount:
          return
  
  ##\brief Remove Dead Ends from the maze 
  ##
  ##\param None. 
  ##\return None
  ##
  ##Based on a certain percentage value, remove dead ends from the maze
  def removeDeadEnds(self):
    #make an 80% chance we will remove the dead end
    chance = 80
    nextCell = False
    validDirection = [True for i in range(4)]
    
    for y in range(self.height):
      for x in range(self.width):
        #check to see if we are at a deadend, ie a candidate for removing
        if self.get_cell(x,y).walls.count(False) == 1:
	  choice = random.randint(0,100)
          if choice <= chance: 
            curX = x
	    curY = y
            nextCell = False

            while not nextCell:
              randDir = random.randint(1, 4)
              if randDir == NORTH:
                if (curY - 1) < 0 :  
                  validDirection[0] = False
                  randDir = random.randint(1, 4)
                elif not self.get_cell(curX, curY).walls[TOP]:
		  #we've intersected a corridor, were done
		  nextCell = True
		else:
                  #bang out two walls to show a corridor
                  self.get_cell(curX, curY).walls[TOP] = False
                  self.get_cell(curX , curY - 1).walls[BOTTOM] = False
                  curY = curY - 1
              elif randDir == SOUTH:
                if (curY + 1) > (self.height - 1): 
                  validDirection[1] = False
                  randDir = random.randint(1, 4)
                elif not self.get_cell(curX, curY).walls[BOTTOM]:
		  #we've intersected a corridor, were done
		  nextCell = True
                else:
                  #bang out two walls to show a corridor
                  self.get_cell(curX, curY).walls[BOTTOM] = False
                  self.get_cell(curX, curY + 1).walls[TOP] = False
                  curY = curY + 1
              elif randDir == EAST:
                if (curX + 1) > (self.width - 1):
                  validDirection[2] = False
                  randDir = random.randint(1, 4)
                elif not self.get_cell(curX, curY).walls[RIGHT]:
		  #we've intersected a corridor, were done
		  nextCell = True
                else:
                  #bang out two walls to show a corridor
                  self.get_cell(curX, curY).walls[RIGHT] = False
                  self.get_cell(curX + 1, curY ).walls[LEFT] = False
                  curX = curX + 1
              else:
                if (curX - 1) < 0:
                  validDirection[3] = False
                  randDir = random.randint(1, 4)
                elif not self.get_cell(curX, curY).walls[LEFT]:
		  #we've intersected a corridor, were done
		  nextCell = True
                else:
                  #bang out two walls to show a corridor
                  self.get_cell(curX, curY).walls[LEFT] = False
                  self.get_cell(curX - 1, curY).walls[RIGHT] = False
                  curX = curX - 1

              if not True in validDirection:
	        nextCell = True
  
  
  
  ##\brief Add rooms the to maze --> to make it a dungeon
  ##
  ##\param None
  ##\return None
  ##
  ##Based on a weighting system, the function will find the best
  ##place to put a room by certain rules: where the given room
  ##overlaps a minimum number of corridors and rooms, and yet
  ##still touches at least one corridor
  def addRooms(self):
    
    #roomCount = random.randint(0,min(5, self.height/2)) 
    roomCount = 1
    while roomCount > 0:
      roomWidth = random.randint(2,self.height/2)
      roomHeight= random.randint(2,self.width/2)
	
      
      #create a room of this size
      newRoom = []
      for i in xrange(roomWidth):
        newRoom.append([])
        for j in xrange(roomHeight):
          newRoom[i].append(Cell())
	  #set all the walls
	  newRoom[i][j].walls = [False for m in range(4)]

      #build outside walls to make it a room
      for y in xrange(roomHeight):
        for x in xrange(roomWidth):
          if x == 0:
	    newRoom[x][y].walls[LEFT] = True
          if x == roomWidth -1:
	    newRoom[x][y].walls[RIGHT] = True
          if y == 0:
	    newRoom[x][y].walls[TOP] = True
          if y == roomHeight  -1:
	    newRoom[x][y].walls[BOTTOM] = True
	
    
      placed = 0
      while not placed:
        randX = random.randint(0, self.width - 1)
        randY = random.randint(0, self.height - 1)
        if(randX + roomWidth) < (self.width -1) and (randY + roomHeight) < (self.height -1):
          placed = 1
      for x in xrange(roomWidth):
        for y in xrange(roomHeight):
          #ADD CODE HERE TO MAKE SURE THE ROOMS HAVE WALLS!!!
          self.maze[randX + x][randY + y] = newRoom[x][y]
      
      roomCount -= 1
      placed = 0
         
  ##\brief Puts characters into maze.
  ##
  ##\return None
  ##\param an integer for number of characters
  ##
  ##Will place characters into maze
  def createCharacters(self, numCharacters):
    count = 1
    height = self.height * 3 + 1
    width = self.width * 3 + 1
    
    while count <= numCharacters:
      validSpot = 0
      while not validSpot:
        randX = random.randint(0, min(15, width - 1))
        randY = random.randint(0, min(15, height - 1))
        if self.output_maze[randX][randY] == '.':
          string = 'P' + str(count)
          self.output_maze[randX][randY] = string
	  validSpot = 1
          count += 1
	
  ##\brief Puts an exit into maze.
  ##
  ##\return None
  ##
  ##Will place  an exit into maze
  def createExit(self):
    height = self.height * 3 + 1
    width = self.width * 3 + 1
    validSpot = 0
    while not validSpot:
      randX = random.randint(0,  width - 1)
      randY = random.randint(0,  height - 1)
      if self.output_maze[randX][randY] == '.':
        self.output_maze[randX][randY] = 'X1'
	validSpot = 1
    
  ##\brief Puts monsters into maze.
  ##
  ##\return None
  ##
  ##Will place random monsters into maze
  def createMonsters(self):
    height = self.height * 3 + 1
    width = self.width * 3 + 1
    numMonsters = random.randint(0, width/2)
    for i in range(numMonsters):
      typeMonster = random.randint(0,5)
      monster_string = 'M' + str(typeMonster)
      validSpot = 0
      while not validSpot:
        randX = random.randint(0, width -1)
        randY = random.randint(0, height -1)
        if self.output_maze[randX][randY] == '.':
          self.output_maze[randX][randY] = monster_string
          validSpot = 1

  ##\brief Puts monster generators into maze.
  ##
  ##\return None
  ##
  ##Will place random monster generators into maze
  def createGenerators(self):
    height = self.height * 3 + 1
    width = self.width * 3 + 1
    
    randNum = random.randint(height/10, height/5)

    for i in range(randNum):
      randType = random.randint(0,5)
      generate_string = 'G' + str(randType)
      validSpot = 0
      while not validSpot:
        randX = random.randint(0, width -1)
        randY = random.randint(0, height -1)
        if self.output_maze[randX][randY] == '.':
          self.output_maze[randX][randY] = generate_string 
          validSpot = 1
      
  ##\brief Puts items into maze.
  ##
  ##\return None
  ##
  ##Will place random items into maze
  def createItems(self):
    height = self.height * 3 + 1
    width = self.width * 3 + 1
    
    #place food first
    numFood = random.randint(0, width/2)
    for i in range(numFood):
      validSpot = 0
      while not validSpot:
        randX = random.randint(0, width -1)
        randY = random.randint(0, height -1)
        if self.output_maze[randX][randY] == '.':
          self.output_maze[randX][randY] = '!1'
          validSpot = 1
    
    #place potions 
    numPotions = random.randint(0, width/2)
    for i in range(numPotions):
      validSpot = 0
      while not validSpot:
        randX = random.randint(0, width -1)
        randY = random.randint(0, height -1)
        if self.output_maze[randX][randY] == '.':
          self.output_maze[randX][randY] = '!2'
          validSpot = 1
    
    #place gold 
    numGold = random.randint(0, width/2)
    for i in range(numGold):
      validSpot = 0
      while not validSpot:
        randX = random.randint(0, width -1)
        randY = random.randint(0, height -1)
        if self.output_maze[randX][randY] == '.':
          self.output_maze[randX][randY] = '!3'
          validSpot = 1

  ##\brief Writes the maze to an inputted file
  ##
  ##\param fileName. The file name to write the maze to
  ##\return None
  ##
  ##This function takes and inputted file name and writes the the maze
  ##file in the specified format laid out in the mapformat.txt located
  ##in the /doc directory
  def createMap(self, fileName):

    height = self.height * 3 + 1
    width = self.width * 3 + 1

    self.generateMap()
    
    #create the outputted maze using the representation of one
    #with the cells
    for y in range(self.height):
      for x in range(self.width):
         
         self.output_maze[x*3 + 1][y *3 + 1] = '*'
         if False in self.get_cell(x,y).walls:
           self.output_maze[x*3 + 1][y *3 + 1] = '.'
           self.output_maze[x*3 + 2][y *3 + 1] = '.'
           self.output_maze[x*3 + 1][y *3 + 2] = '.'
           self.output_maze[x*3 + 2][y *3 + 2] = '.'
   	 #if a wall is blown out, then make the corridor open
         if not self.get_cell(x,y).walls[TOP]:
           self.output_maze[x*3 + 1][y *3 ] = '.'
           self.output_maze[x*3 + 2][y *3 ] = '.'
         if not self.get_cell(x,y).walls[BOTTOM]:
           self.output_maze[x*3 + 1][y *3 + 3] = '.'
           self.output_maze[x*3 + 2][y *3 + 3] = '.'
         if not self.get_cell(x,y).walls[RIGHT]:
           self.output_maze[x*3 + 3][y *3 + 1] = '.'
           self.output_maze[x*3 + 3][y *3 + 2] = '.'
         if not self.get_cell(x,y).walls[LEFT]:
           self.output_maze[x*3][y *3 + 1] = '.'
           self.output_maze[x*3][y *3 + 2] = '.'
    
    #checks for the corners between two walls, and compares that to the adjacent cells 
    for y in range(self.height):
      for x in range(self.width):
        if not self.get_cell(x,y).walls[TOP] and not self.get_cell(x,y).walls[RIGHT]:
          if x + 1 >= self.width or (y -1) < 0:
            pass
          else:
           if not self.get_cell(x + 1, y).walls[TOP]:
             if not self.get_cell(x, y-1).walls[RIGHT]:
               self.output_maze[x*3 + 3][y *3] = '.' 
        if not self.get_cell(x,y).walls[TOP] and not self.get_cell(x,y).walls[LEFT]:
          if x - 1 < 0 or (y - 1) < 0:
            pass
          else:
           if not self.get_cell(x - 1, y).walls[TOP]:
             if not self.get_cell(x, y-1).walls[LEFT]:
               self.output_maze[x*3][y*3] = '.' 
        if not self.get_cell(x,y).walls[BOTTOM] and not self.get_cell(x,y).walls[RIGHT]:
          if (x + 1) >= self.width or (y +1) >= self.height:
            pass
          else:
           if not self.get_cell(x + 1, y).walls[BOTTOM]:
             if not self.get_cell(x, y+1).walls[RIGHT]:
               self.output_maze[x*3 + 3][y * 3 + 3] = '.' 
        if not self.get_cell(x,y).walls[BOTTOM] and not self.get_cell(x,y).walls[LEFT]:
          if x - 1 < 0 or (y -1) < 0:
            pass
          else:
           if not self.get_cell(x - 1, y).walls[BOTTOM]:
             if not self.get_cell(x, y-1).walls[LEFT]:
               self.output_maze[x*3][y*3+ 3] = '.' 
        
    self.createCharacters(2)
    self.createExit()
    self.createMonsters()
    self.createItems()
    self.createGenerators()

    #generate the file to be used
    fullName = os.path.join('data', 'map', fileName)
    file = open(fullName, 'w')
    file.write('title(Generated Map)\n')
    file.write('version(Completely Perfect in Every Way)\n')
    file.write('author(MazeGenerator.py)\n')
    file.write(str(width) + ' ' + str(height))

    for i in xrange(height):
      file.write('\n')
      for j in xrange(width):
        file.write(str(self.output_maze[j][i]) + ' ')

    file.close()


if __name__ == "__main__":
  test = MapGenerator(int(sys.argv[1]))
  test.createMap('random.map')
