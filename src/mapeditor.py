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

import os
import sys
import pygame

MAP_SIZE = 25
WINDOW_SIZE = [ 600, 600]

MONSTER_TYPE = 0
NUM_MONSTERS = 6

GENERATOR_TYPE = 0
NUM_GENERATORS = 6

WALL = '*'
FLOOR  = '.'
EXIT = 'X1'
DOOR = 'D'
KEY = '!0'
FOOD = '!1'
POTION = '!2'
GOLD = '!3'

GENERATOR0 = 'G0'
GENERATOR1 = 'G1'
GENERATOR2 = 'G2'
GENERATOR3 = 'G3'
GENERATOR4 = 'G4'
GENERATOR5 = 'G5'

MONSTER0 = 'M0'
MONSTER1 = 'M1'
MONSTER2 = 'M2'
MONSTER3 = 'M3'
MONSTER4 = 'M4'
MONSTER5 = 'M5'

PLAYER1 = 'P1'
PLAYER2 = 'P2'
PLAYER3 = 'P3'
PLAYER4 = 'P4'
image_map = {}

##\brief CellSprite Extends the Sprite Class
##
##CellSprite is the core of our visualizer.  It does the actual
##displaying of each cell

class CellSprite(pygame.sprite.Sprite):
    wall = None
    floor = None
    door = None
    exit = None
    key = None
    food = None
    generator0 = None
    generator1 = None
    gold = None
    potion = None
    monster0 = None
    monster1 = None
    monster2 = None
    monster3 = None
    monster4 = None
    monster5 = None
    player1 = None
    player2 = None
    player3 = None
    player4 = None
    def __init__(self, initial_position, identity, size):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = initial_position
	self.identity = identity
	
	self.size = size
        self.x_size = size[0]
	self.y_size = size[1]

	self.filename = os.path.join('data', 'images','old', 'floor.png')

	if CellSprite.floor is None:
		CellSprite.floor = pygame.image.load(self.filename).convert()
		CellSprite.floor = pygame.transform.scale(CellSprite.floor, size)
       
	self.image = pygame.Surface(size)
	self.image = CellSprite.floor.convert()

	self.rect = self.image.get_rect()
	self.rect.topleft = self.pos()
	
    def update(self):
	self.image = CellSprite.floor.convert()
	self.identity = image_map[self.x, self.y]

	if self.identity == WALL:
		if CellSprite.wall is None:
			CellSprite.wall = pygame.image.load("data/skins/gauntlet/wall.png")
			CellSprite.wall = pygame.transform.scale(CellSprite.wall, self.size)
		self.image.blit(CellSprite.wall, CellSprite.wall.get_rect())
	elif self.identity == FLOOR: 
		if CellSprite.floor is None:
			CellSprite.floor = pygame.image.load("data/images/old/floor.png")
			CellSprite.floor = pygame.transform.scale(CellSprite.floor, self.size)
		self.image.blit(CellSprite.floor, CellSprite.floor.get_rect())
	elif self.identity == DOOR: 
		if CellSprite.door is None:
			CellSprite.door = pygame.image.load("data/skins/gauntlet/door.png")
			CellSprite.door = pygame.transform.scale(CellSprite.door, self.size)
		self.image.blit(CellSprite.door, CellSprite.door.get_rect())
	elif self.identity == EXIT: 
		if CellSprite.exit is None:
			CellSprite.exit = pygame.image.load("data/skins/gauntlet/exit.png")
			CellSprite.exit = pygame.transform.scale(CellSprite.exit, self.size)
		self.image.blit(CellSprite.exit, CellSprite.exit.get_rect())
	elif self.identity == KEY:
		if CellSprite.key is None:
			CellSprite.key = pygame.image.load("data/skins/gauntlet/keyhoriz.png")
			CellSprite.key = pygame.transform.scale(CellSprite.key, self.size)
		self.image.blit(CellSprite.key, CellSprite.key.get_rect())
	elif self.identity == FOOD:
		if CellSprite.food is None:
			CellSprite.food = pygame.image.load("data/images/food2.png")
			CellSprite.food = pygame.transform.scale(CellSprite.food, self.size)
		self.image.blit(CellSprite.food, CellSprite.food.get_rect())
	elif self.identity == POTION:
		if CellSprite.potion is None:
			CellSprite.potion = pygame.image.load("data/images/magicpotion.png")
			CellSprite.potion = pygame.transform.scale(CellSprite.potion, self.size)
		self.image.blit(CellSprite.potion, CellSprite.potion.get_rect())
	elif self.identity == GOLD:
		if CellSprite.gold is None:
			CellSprite.gold = pygame.image.load("data/skins/gauntlet/treasure.png")
			CellSprite.gold = pygame.transform.scale(CellSprite.gold, self.size)
		self.image.blit(CellSprite.gold, CellSprite.gold.get_rect())
	elif self.identity == GENERATOR0:
		if CellSprite.generator0 is None:
			CellSprite.generator0 = pygame.image.load("data/skins/gauntlet/ghostgenbig.png")
			CellSprite.generator0 = pygame.transform.scale(CellSprite.generator0, self.size)
		self.image.blit(CellSprite.generator0, CellSprite.generator0.get_rect())
	elif self.identity == GENERATOR1:
		if CellSprite.generator1 is None:
			CellSprite.generator1 = pygame.image.load("data/skins/gauntlet/gen3.png")
			CellSprite.generator1 = pygame.transform.scale(CellSprite.generator1, self.size)
		self.image.blit(CellSprite.generator1, CellSprite.generator1.get_rect())
	elif self.identity == GENERATOR2:
		if CellSprite.generator1 is None:
			CellSprite.generator1 = pygame.image.load("data/skins/gauntlet/gen3.png")
			CellSprite.generator1 = pygame.transform.scale(CellSprite.generator1, self.size)
		self.image.blit(CellSprite.generator1, CellSprite.generator1.get_rect())
	elif self.identity == GENERATOR3:
		if CellSprite.generator1 is None:
			CellSprite.generator1 = pygame.image.load("data/skins/gauntlet/gen3.png")
			CellSprite.generator1 = pygame.transform.scale(CellSprite.generator1, self.size)
		self.image.blit(CellSprite.generator1, CellSprite.generator1.get_rect())
	elif self.identity == GENERATOR4:
		if CellSprite.generator1 is None:
			CellSprite.generator1 = pygame.image.load("data/skins/gauntlet/gen3.png")
			CellSprite.generator1 = pygame.transform.scale(CellSprite.generator1, self.size)
		self.image.blit(CellSprite.generator1, CellSprite.generator1.get_rect())
	elif self.identity == GENERATOR5:
		if CellSprite.generator1 is None:
			CellSprite.generator1 = pygame.image.load("data/skins/gauntlet/gen3.png")
			CellSprite.generator1 = pygame.transform.scale(CellSprite.generator1, self.size)
		self.image.blit(CellSprite.generator1, CellSprite.generator1.get_rect())
	elif self.identity == MONSTER0:
		if CellSprite.monster0 is None:
			CellSprite.monster0 = pygame.image.load("data/skins/gauntlet/whiteghostD.png")
			CellSprite.monster0 = pygame.transform.scale(CellSprite.monster0, self.size)
		self.image.blit(CellSprite.monster0, CellSprite.monster0.get_rect())
	elif self.identity == MONSTER1:
		if CellSprite.monster1 is None:
			CellSprite.monster1 = pygame.image.load("data/skins/gauntlet/gruntD.png")
			CellSprite.monster1 = pygame.transform.scale(CellSprite.monster1, self.size)
		self.image.blit(CellSprite.monster1, CellSprite.monster1.get_rect())
	elif self.identity == MONSTER2:
		if CellSprite.monster2 is None:
			CellSprite.monster2 = pygame.image.load("data/skins/gauntlet/demonD.png")
			CellSprite.monster2 = pygame.transform.scale(CellSprite.monster2, self.size)
		self.image.blit(CellSprite.monster2, CellSprite.monster2.get_rect())
	elif self.identity == MONSTER3:
		if CellSprite.monster3 is None:
			CellSprite.monster3 = pygame.image.load("data/skins/gauntlet/lobberD.png")
			CellSprite.monster3 = pygame.transform.scale(CellSprite.monster3, self.size)
		self.image.blit(CellSprite.monster3, CellSprite.monster3.get_rect())
	elif self.identity == MONSTER4:
		if CellSprite.monster4 is None:
			CellSprite.monster4 = pygame.image.load("data/skins/gauntlet/sorceD.png")
			CellSprite.monster4 = pygame.transform.scale(CellSprite.monster4, self.size)
		self.image.blit(CellSprite.monster4, CellSprite.monster4.get_rect())
	elif self.identity == MONSTER5:
		if CellSprite.monster5 is None:
			CellSprite.monster5 = pygame.image.load("data/skins/gauntlet/deathD.png")
			CellSprite.monster5 = pygame.transform.scale(CellSprite.monster5, self.size)
		self.image.blit(CellSprite.monster5, CellSprite.monster5.get_rect())
	elif self.identity == PLAYER1:
		if CellSprite.player1 is None:
			CellSprite.player1 = pygame.image.load("data/skins/gauntlet/warriorD.png")
			CellSprite.player1 = pygame.transform.scale(CellSprite.player1, self.size)
		self.image.blit(CellSprite.player1, CellSprite.player1.get_rect())
	elif self.identity == PLAYER2:
		if CellSprite.player2 is None:
			CellSprite.player2 = pygame.image.load("data/skins/gauntlet/wizardD.png")
			CellSprite.player2 = pygame.transform.scale(CellSprite.player2, self.size)
		self.image.blit(CellSprite.player2, CellSprite.player2.get_rect())
	elif self.identity == PLAYER3:
		if CellSprite.player3 is None:
			CellSprite.player3 = pygame.image.load("data/skins/gauntlet/valkyrieD.png")
			CellSprite.player3 = pygame.transform.scale(CellSprite.player3, self.size)
		self.image.blit(CellSprite.player3, CellSprite.player3.get_rect())
	elif self.identity == PLAYER4:
		if CellSprite.player4 is None:
			CellSprite.player4 = pygame.image.load("data/skins/gauntlet/archer_south.png")
			CellSprite.player4 = pygame.transform.scale(CellSprite.player4, self.size)
		self.image.blit(CellSprite.player4, CellSprite.player4.get_rect())
	
    def pos( self ):
	return [self.x_size * self.x,self.y_size * self.y]
				
def update_pos(key, cur_x, cur_y, height, width):
	if key == pygame.K_DOWN: 
		if(cur_y < height - 1):
			cur_y += 1
	if key == pygame.K_UP:
		if(cur_y > 0):
			cur_y -= 1
			
	if key == pygame.K_LEFT:
		if(cur_x > 0):
			cur_x  -= 1
	if key == pygame.K_RIGHT:
		if(cur_x < width -1 ):
			cur_x += 1

	return cur_x, cur_y

def image_update(key, x, y):
	global MONSTER_TYPE
	global GENERATOR_TYPE

	if key == pygame.K_w:
		return WALL
	elif key == pygame.K_t:
		return FLOOR
	elif key == pygame.K_k:
		return KEY
	elif key == pygame.K_f:
		return FOOD
	elif key == pygame.K_p:
		return POTION
	elif key == pygame.K_g:
		return GOLD
	elif key == pygame.K_n:
		GENERATOR_TYPE = (GENERATOR_TYPE + 1)%NUM_GENERATORS
		if GENERATOR_TYPE == 0:
			return GENERATOR0
		elif GENERATOR_TYPE == 1:
			return GENERATOR1
		elif GENERATOR_TYPE == 2:
			return GENERATOR2
		elif GENERATOR_TYPE == 3:
			return GENERATOR3
		elif GENERATOR_TYPE == 4:
			return GENERATOR4
		else:
			return GENERATOR1		
	elif key == pygame.K_m:
		MONSTER_TYPE = ( MONSTER_TYPE + 1)%NUM_MONSTERS
		if MONSTER_TYPE == 0:
			return MONSTER0
		elif MONSTER_TYPE == 1:
			return MONSTER1
		elif MONSTER_TYPE == 2:
			return MONSTER2
		elif MONSTER_TYPE == 3:
			return MONSTER3
		elif MONSTER_TYPE == 4:
			return MONSTER4
		else :
			return MONSTER5
        elif key == pygame.K_d:
		return DOOR
        elif key == pygame.K_e:
		return EXIT
	elif key == pygame.K_1:
		return PLAYER1
	elif key == pygame.K_2:
		return PLAYER2
	elif key == pygame.K_3:
		return PLAYER3
        elif key == pygame.K_4:
		return PLAYER4
	return image_map[x,y]

def loadMyMap(filename):
    # Attempt to load the map file
    try:
      fullName = filename
      mapFile = open(fullName)
    except:
      print "Map file %s could not be loaded."%filename
      sys.exit(1)
    # Read the lines of the map file
    mapLines = mapFile.readlines()
    mapStarted = False
    lineNum = 1
    x = 0
    y = 0
    mapwidth = 20
    mapheight = 20


    # Parse each line separately
    for line in mapLines:
      # Check if we have started reading the map tiles
      if mapStarted:
        #try:
          x = 0
          for tile in line.split():
            if tile[0] == '*':
              image_map[x,y] = WALL
            elif tile == '.':
              image_map[x,y] = FLOOR
            elif tile == 'D':
              image_map[x,y] = DOOR
            elif tile == '!0':
              image_map[x,y] = KEY
            elif tile == '!1':
              image_map[x,y] = FOOD
            elif tile == '!2':
              image_map[x,y] = POTION
            elif tile == '!3':
              image_map[x,y] = GOLD
            elif tile[0] == 'M':
	    	if tile[1] == '0':
                	image_map[x,y] = MONSTER0
		elif tile[1] == '1':
		    	image_map[x,y] = MONSTER1
		elif tile[1] == '2':
		    	image_map[x,y] = MONSTER2
		elif tile[1] == '3':
		    	image_map[x,y] = MONSTER3
		elif tile[1] == '4':
		    	image_map[x,y] = MONSTER4
		else:
			image_map[x,y] = MONSTER5
            elif tile[0] == 'G':
            	if tile[1] == '0':
		  	image_map[x,y] = GENERATOR0
		elif tile[1] == '1':
		    	image_map[x,y] = GENERATOR1
		elif tile[1] == '2':
		    	image_map[x,y] = GENERATOR2
		elif tile[1] == '3':
		    	image_map[x,y] = GENERATOR3
		elif tile[1] == '4':
		    	image_map[x,y] = GENERATOR4
		else:
			image_map[x,y] = GENERATOR5
            elif tile[0] == 'X':
              image_map[x,y] = EXIT
            elif tile == 'P1':
              image_map[x,y] = PLAYER1
            elif tile == 'P2':
              image_map[x,y] = PLAYER2
            elif tile == 'P3':
              image_map[x,y] = PLAYER3
            elif tile == 'P4':
              image_map[x,y] = PLAYER4
            else:
              pass
            x += 1
          y += 1
        #except:
          pass

      elif line.startswith('author'):
        author = line
      else:
        # Try to get the map size
        try:
          lineList = line.split()
          mapwidth = int(lineList[0])
          mapheight = int(lineList[1])
          mapStarted = True
        except ValueError:
          mapStarted = False
      # Keep track of the line number for error messages
      lineNum += 1
    mapFile.close()
    
    tuple = [mapwidth, mapheight]
    return tuple

def test(width, height):
	for x in range(width):
		for y in range(height):
			print x, y
			print image_map[x,y]
def main():
	keepGoing  = True
        
	loadMap = False
	if  len(sys.argv) == 2:
		loadMap = True
		mapName = sys.argv[1]
	else:
		input_size = raw_input("What size map would you like to make?")
		if int(input_size) > 0 and int(input_size) < 50:
			MAP_SIZE = int(input_size)
  
	pygame.init()
	
	if loadMap:
		 width, height = loadMyMap(mapName)
	else:
		height = MAP_SIZE
		width = MAP_SIZE
		#set up initial values
		for x in range(0, height ):
			for y in range(0, width):
				image_map[x,y] = FLOOR 


	X_SIZE = WINDOW_SIZE[0]/width
	Y_SIZE = WINDOW_SIZE[1]/height
	
	screen = pygame.display.set_mode(WINDOW_SIZE)	
	

        background = pygame.Surface(screen.get_size())
	filename = os.path.join('data', 'images', 'background.png')
	background = pygame.image.load(filename).convert()
	
	#make a new sprites group
	sprites = pygame.sprite.RenderUpdates()
	x = 0
	y = 0
        try:
          lfilename = os.path.join('data', 'images', 'cursor.png')
          cursor = pygame.image.load(lfilename)
          cursor = pygame.transform.scale(cursor, (X_SIZE,Y_SIZE))
        except:
          pass

	for x in range(width):
	 	for y in range(height):
			newSprite = CellSprite([x,y], image_map[x,y], [X_SIZE, Y_SIZE])
			sprites.add(newSprite)

	x_pos = 0
	y_pos = 0
	
	while keepGoing:
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				keepGoing = False
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				keepgoing = False
			elif event.type ==pygame.KEYDOWN and (event.key == pygame.K_DOWN or event.key == pygame.K_UP or event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT):
				x_pos, y_pos = update_pos(event.key, x_pos, y_pos, height, width)	
			elif event.type == pygame.KEYDOWN:
				image_map[x_pos,y_pos]= image_update(event.key, x_pos, y_pos)
				
		sprites.update()
		screen.blit(background, (0,0))
		rectList = sprites.draw(screen)
                try:
                  screen.blit(cursor,(x_pos*X_SIZE,y_pos*Y_SIZE))
                except:
                  pass  
		pygame.display.update(rectList)


	answer = raw_input("Would you like to save your work(Yes/No):")
	if answer[0] == 'Y' or answer[0] == 'y':
		if loadMap:
			file_name = mapName
			file = open(file_name, 'w')
			file.write('title(Edited Copy)\n')
			file.write('version(a new one)\n')
		
		else:
        		#write a new file if we have no file to
			file_name = 'newlevel.map'
			file = open(file_name, 'w')
			file.write('title(Map Editor)\n')
			file.write('version(1)\n')

		file.write('author(Penetrode)\n')
		file.write(str(height) + ' ' + str(width))
       		file.write('\n')

		for y in range(0, height):
			for x in range(0, width):
				if image_map[x,y] == WALL or image_map[x,y] == FLOOR or\
				image_map[x,y] == DOOR:
					file.write(str(image_map[x,y]) + '  ') 
				else:
					file.write(str(image_map[x,y]) + ' ') 
				
	        	file.write('\n')		

		file.close()
		print 'Saved to ', file_name

if __name__ == "__main__":
	main()
