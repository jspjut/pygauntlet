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

import pygame
import os

##\namespace Configuration values
##\brief The main configuration values for Gauntlet
##
##The configuration values are used to reduce the amount of "magic numbers" in
##our code. All system-wide values are to be declared here.

#TILE_SIZE is the size of each map tile as well as each sprite in the map.
#It should be a power of 2. 32 is the default
TILE_SIZE = 32

# Until the skin loader is completed, put a custom skin here to load it as
# the default.
# Moving SKIN to skin.py JS
#SKIN = "gauntlet"
#SKIN = "reverse"

# Find the path to the current directory
# This is to reduce the number of times we need to find the path
PATH = os.path.abspath('.')

#RESOLUTION is the screen resolution.
RESOLUTION = [640,480]  #20x15 tile maps (VGA)
#RESOLUTION = [768,576]  #24x18 tile maps
#RESOLUTION = [896,672]  #28x21 tile maps
#RESOLUTION = [1024,768] #32x24 tile maps (XGA)
HALF_RESOLUTION = [RESOLUTION[0] / 2,RESOLUTION[1] / 2]

#server/client role variables
REGULAR = 0
SERVER = 1
CLIENT = 2

#MAX_PLAYERS is the max number of players allowed
MAX_PLAYERS = 4

#CHARACTER TYPES
WARRIOR = 0
WIZARD = 1
VALKYRIE = 2
ARCHER = 3

PLAYERS = []
PLAYERS.append(WARRIOR)
PLAYERS.append(WIZARD)
PLAYERS.append(VALKYRIE)
PLAYERS.append(ARCHER)

#This is for when we develop configurable skins
PLAYER_NAMES = {}
PLAYER_NAMES[WARRIOR] = 'Warrior'
PLAYER_NAMES[WIZARD] = 'Wizard'
PLAYER_NAMES[VALKYRIE] = 'Valkyrie'
PLAYER_NAMES[ARCHER] = 'Archer'

#MONSTER TYPES
MONSTER_CLASS = 4
GHOST = MONSTER_CLASS + 0
GRUNT = MONSTER_CLASS + 1
DEMON = MONSTER_CLASS + 2
LOBBER = MONSTER_CLASS + 3
SORCERER = MONSTER_CLASS + 4
DEATH = MONSTER_CLASS + 5
THIEF = MONSTER_CLASS + 6

MONSTERS = []
MONSTERS.append(GHOST)
MONSTERS.append(GRUNT)
MONSTERS.append(DEMON)
MONSTERS.append(LOBBER)
MONSTERS.append(SORCERER)
MONSTERS.append(DEATH)
MONSTERS.append(THIEF)

#ITEM TYPES
KEY = 0
FOOD = 1
POTION = 2
GOLD = 3

#GENERATOR TYPES
GENERATOR_CLASS = 50
GHOSTGENERATOR = GENERATOR_CLASS + 0
GRUNTGENERATOR = GENERATOR_CLASS + 1

#PROJECTILES
PROJECTILE = 100
PROJECTILE_WARRIOR = PROJECTILE + WARRIOR
PROJECTILE_WIZARD = PROJECTILE + WIZARD
PROJECTILE_VALKYRIE = PROJECTILE + VALKYRIE
PROJECTILE_ARCHER = PROJECTILE + ARCHER
PROJECTILE_OTHER = PROJECTILE + PROJECTILE

PLAYER_PROJECTILES = []
PLAYER_PROJECTILES.append(PROJECTILE_WARRIOR)
PLAYER_PROJECTILES.append(PROJECTILE_WIZARD)
PLAYER_PROJECTILES.append(PROJECTILE_VALKYRIE)
PLAYER_PROJECTILES.append(PROJECTILE_ARCHER)

#DIRECTION VARIABLES
NORTH = 1
SOUTH = 2
EAST = 3
WEST = 4
NORTHEAST = 5
NORTHWEST = 6
SOUTHEAST = 7
SOUTHWEST = 8

#Attack and magic values
ATTACK = 9
MAGIC = 10

#DIRECTIONS
TOP = 0
BOTTOM = 1
LEFT = 2
RIGHT = 3

#Holds default key configurations for players
PLAYER_KEYS = {}

PLAYER1 = {}
PLAYER1[NORTH] = pygame.K_w
PLAYER1[SOUTH] = pygame.K_s
PLAYER1[WEST] = pygame.K_a
PLAYER1[EAST] = pygame.K_d
PLAYER1[ATTACK] = pygame.K_v
PLAYER1[MAGIC] = pygame.K_b

PLAYER_KEYS[1] = PLAYER1

PLAYER2 = {}
PLAYER2[NORTH] = pygame.K_UP
PLAYER2[SOUTH] = pygame.K_DOWN
PLAYER2[WEST] = pygame.K_LEFT
PLAYER2[EAST] = pygame.K_RIGHT
PLAYER2[ATTACK] = pygame.K_k
PLAYER2[MAGIC] = pygame.K_l

PLAYER_KEYS[2] = PLAYER2

PLAYER3 = {}
PLAYER3[NORTH] = pygame.K_HOME
PLAYER3[SOUTH] = pygame.K_END
PLAYER3[WEST] = pygame.K_DELETE
PLAYER3[EAST] = pygame.K_PAGEDOWN
PLAYER3[ATTACK] = pygame.K_BACKSPACE
PLAYER3[MAGIC] = pygame.K_BACKSLASH
PLAYER_KEYS[3] = PLAYER3

PLAYER4 = {}
PLAYER4[NORTH] = pygame.K_KP8
PLAYER4[SOUTH] = pygame.K_KP2
PLAYER4[WEST] = pygame.K_KP4
PLAYER4[EAST] = pygame.K_KP6
PLAYER4[ATTACK] = pygame.K_KP_PLUS
PLAYER4[MAGIC] = pygame.K_KP_ENTER
PLAYER_KEYS[4] = PLAYER4

#The millisecond delay between CPU TickEvents
DELAY = 1
SLEEP_DELAY = DELAY / 2000.0
TURN_TICKS = 8
#The number of delays required for DisplayTickEvents
DISPLAY_DELAY = 5

#RANGE VALUES FOR STATS
STAT_MAX = 50.0
AVE_STAT = 20.0
STAT_MIN = 0.0

#Related to mobile movement
MOVE_SPEED = 4
PROJECTILE_MULTIPLIER = 3
REST_TIME = 1
ATTACK_TIME = 25 * REST_TIME
AVE_DEX = AVE_STAT
AVE_STR = AVE_STAT
AVE_DEF = AVE_STAT

#the radius around each character (number of tiles) where mobiles are updated
VISION = 8

#the number of ticks that must pass before a monster is generated
MONSTER_GENERATE_TIMER = 200

#Remove pygame to avoid wasting memory
del(pygame)
