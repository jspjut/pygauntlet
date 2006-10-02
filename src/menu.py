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
  import sys
  import os
  import mapeditor  
  import maploader
  import pygame
  import events
  import display
  import character
  import keyboardcontroller
  
  from config import *
  import skin
except ImportError, err:
  print "couldn't load module. %s"% (err)
  sys.exit(2)
  
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def splashScreen ( ):
  return # turn off the splash screen
  screen = pygame.display.set_mode(RESOLUTION)
  sname = os.path.join('data','skins',skin.SKIN,'splash.png')
  splashs = display.loadPng(sname)

  showSplash = True
  n = 0
  while showSplash:
    screen.blit(splashs,(0,0))
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        sys.exit()
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
        pygame.display.toggle_fullscreen()
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        showSplash=False
    n += 1
    if n > 1000:
      showSplash=False
    pygame.display.update()

def mainMenuScreen (eventManager, theGame):
  screen = pygame.display.set_mode(RESOLUTION)
  fontMenu = pygame.font.Font(None,30)
  sname = os.path.join('data','skins',skin.SKIN,'splash.png')
  splashs = display.loadPng(sname)
  background = pygame.Surface(screen.get_size())
  background = background.convert()
  background.fill((0, 0, 0))
  background.blit(splashs,(0,-50))

  inMainMenu = True
  menuSelect = 0
  while inMainMenu:
    screen.blit(background, (0, 0))
    color = WHITE
    if menuSelect == 0:
      color = (0, 255, 155)
    textMenu = fontMenu.render("Start Game", 1, color)
    textPosMenu = textMenu.get_rect()
    textPosMenu.centerx = background.get_rect().centerx
    textPosMenu.top = background.get_rect().bottom - 90
    screen.blit(textMenu, textPosMenu)
    lastTextPos = textPosMenu
    color = WHITE
    if menuSelect == 1:
      color = (0, 255, 155)
    textMenu = fontMenu.render("Choose Skin", 1, color)
    textPosMenu = textMenu.get_rect()
    textPosMenu.centerx =  lastTextPos.centerx
    textPosMenu.top = lastTextPos.bottom
    screen.blit(textMenu, textPosMenu)
    lastTextPos = textPosMenu
    color = WHITE
    if menuSelect == 2:
      color = (0, 255, 155)
    textMenu = fontMenu.render("Quit", 1, color)
    textPosMenu = textMenu.get_rect()
    textPosMenu.centerx =  lastTextPos.centerx
    textPosMenu.top = lastTextPos.bottom
    screen.blit(textMenu, textPosMenu)
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        sys.exit()
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
        pygame.display.toggle_fullscreen()

      #move up
      elif event.type == pygame.KEYDOWN and (event.key == pygame.K_w or \
                                             event.key == pygame.K_UP or \
                                             event.key == pygame.K_HOME or \
                                             event.key == pygame.K_KP8):
        menuSelect -= 1
        if menuSelect < 0:
          menuSelect = 0
      #move down
      elif event.type == pygame.KEYDOWN and (event.key == pygame.K_s or \
                                             event.key == pygame.K_DOWN or \
                                             event.key == pygame.K_END or \
                                             event.key == pygame.K_KP2):
        menuSelect += 1
        if menuSelect > 2:
          menuSelect= 2

      #Process current selection
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
	
	if menuSelect == 0:
	  characterScreen(eventManager, theGame)
          inMainMenu = False
	  
	elif menuSelect == 1:
          configScreen(eventManager, theGame)
#	  fontMenu = pygame.font.Font(None,20)
#	  textMenu = fontMenu.render("Please check your command line", 1, color)
#	  textPosMenu = textMenu.get_rect()
#	  textPosMenu.topleft = ( 400, 230)
#          screen.blit(textMenu, textPosMenu)
#          pygame.display.update()
#	  mapeditor.main()
#	  sys.exit()
	elif menuSelect ==2:
	  sys.exit()
	
    pygame.display.update()

def configScreen( eventManager, theGame ):
  screen = pygame.display.get_surface()
  fontMenu = pygame.font.Font(None,30)
  screen.fill((0, 0, 0))

  # Get the skin list
  skinList = skin.getSkinList()
  inMainMenu = True
  menuSelect = 0
  while inMainMenu:
    # The color for selected text
    selectedColor = (0, 255, 155)
    color = WHITE
    # loop through the skins
    i = 0
    for mySkin in skinList:
      # choose the color if selected
      if menuSelect == i:
        color = selectedColor
      else:
        color = WHITE
      textMenu = fontMenu.render(mySkin, 1, color)
      textPosMenu = textMenu.get_rect()
      try:
        textPosMenu.centerx = lastTextPos.centerx
        textPosMenu.top = lastTextPos.bottom
      except:
        textPosMenu.centerx = screen.get_rect().centerx
        textPosMenu.top = screen.get_rect().top + 90
      screen.blit(textMenu, textPosMenu)
      lastTextPos = textPosMenu
      i = i + 1
    # add Back to menu
    if menuSelect == i:
      color = selectedColor
    else:
      color = WHITE
    textMenu = fontMenu.render('Back', 1, color)
    textPosMenu = textMenu.get_rect()
    try:
      textPosMenu.centerx = lastTextPos.centerx
      textPosMenu.top = lastTextPos.bottom
    except:
      textPosMenu.centerx = screen.get_rect().centerx
      textPosMenu.top = screen.get_rect().top + 90
    screen.blit(textMenu, textPosMenu)
    del(lastTextPos)
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        sys.exit()
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
        pygame.display.toggle_fullscreen()

      #move up
      elif event.type == pygame.KEYDOWN and (event.key == pygame.K_w or \
                                             event.key == pygame.K_UP or \
                                             event.key == pygame.K_HOME or \
                                             event.key == pygame.K_KP8):
        menuSelect -= 1
        if menuSelect < 0:
          menuSelect = 0
      #move down
      elif event.type == pygame.KEYDOWN and (event.key == pygame.K_s or \
                                             event.key == pygame.K_DOWN or \
                                             event.key == pygame.K_END or \
                                             event.key == pygame.K_KP2):
        menuSelect += 1
        if menuSelect > len(skinList):
          menuSelect= len(skinList)

      #Process current selection
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
	
        if menuSelect == len(skinList):
          pass
        else:
          skin.SKIN = skinList[menuSelect]
          mapFilename = os.path.join(PATH,'data','skins',skin.SKIN,'mapList.cfg')
          theGame.mapLoader = maploader.MapLoader(mapFilename)
	inMainMenu = False

    pygame.display.update()
    

def characterScreen ( eventManager, theGame ):
  screen = pygame.display.set_mode(RESOLUTION)
  fontMenu = pygame.font.Font(None,30)
  keyboardControllers = []
  menuSelect = [-1,-1,-1,-1]

  background = pygame.Surface(screen.get_size())
  background = background.convert()
  background.fill((0, 0, 0))

  path = os.path.join('data','skins',skin.SKIN)

  inStartMenu = True
  while inStartMenu:

    screen.blit(background, (0, 0))
    counter = 0

    textMenu = fontMenu.render("Player 1", 1,WHITE)
    textPosMenu = textMenu.get_rect()
    textPosMenu.topleft = 100,10
    screen.blit(textMenu, textPosMenu)
    textMenu = fontMenu.render("Player 2", 1,WHITE)
    textPosMenu = textMenu.get_rect()
    textPosMenu.topleft = 420,10
    screen.blit(textMenu, textPosMenu)
    textMenu = fontMenu.render("Player 3", 1,WHITE)
    textPosMenu = textMenu.get_rect()
    textPosMenu.topleft = 100,250
    screen.blit(textMenu, textPosMenu)
    textMenu = fontMenu.render("Player 4", 1,WHITE)
    textPosMenu = textMenu.get_rect()
    textPosMenu.topleft = 420,250
    screen.blit(textMenu, textPosMenu)

    for player in menuSelect:

      if counter == 0:
        topleft = (0,0)
      elif counter == 1:
        topleft = (320,0)
      elif counter == 2:
        topleft = (0,240)
      elif counter == 3:
        topleft = (320,240)

      color = WHITE
      if menuSelect[counter] == WARRIOR:
        skinfile = open(os.path.join(path, 'warrior.cfg'))
        #picFile = os.path.join(path,'warriorUR.png')
        picFile = os.path.join(path,skinfile.readlines()[1].strip())
        warrior = display.loadPng(picFile)
        warriorPos = warrior.get_rect()
        warrior = pygame.transform.scale(warrior,(96,96))
        warriorPos.topleft = (topleft[0]+25,topleft[1]+50)
        screen.blit(warrior,warriorPos)
        color = (0, 255, 0)
      textMenu = fontMenu.render("Warrior", 1, color)
      textPosMenu = textMenu.get_rect()
      textPosMenu.topleft = ( (topleft[0]+160), topleft[1]+50 )
      screen.blit(textMenu, textPosMenu)

      color = WHITE
      if menuSelect[counter] == WIZARD:
        skinfile = open(os.path.join(path, 'wizard.cfg'))
        picFile = os.path.join(path,skinfile.readlines()[1].strip())
        wizard = display.loadPng(picFile)
        wizardPos = wizard.get_rect()
        wizard = pygame.transform.scale(wizard,(96,96))
        wizardPos.topleft = (topleft[0]+25,topleft[1]+50)
        screen.blit(wizard,wizardPos)
        color = (0, 255, 0)
      textMenu = fontMenu.render("Wizard", 1, color)
      textPosMenu = textMenu.get_rect()
      textPosMenu.topleft = ( (topleft[0]+160), topleft[1]+80 )
      screen.blit(textMenu, textPosMenu)

      color = WHITE
      if menuSelect[counter] == VALKYRIE:
        skinfile = open(os.path.join(path, 'valkyrie.cfg'))
        picFile = os.path.join(path,skinfile.readlines()[1].strip())
        valkyrie = display.loadPng(picFile)
        valkyriePos = valkyrie.get_rect()
        valkyrie = pygame.transform.scale(valkyrie,(96,96))
        valkyriePos.topleft = (topleft[0]+25,topleft[1]+50)
        screen.blit(valkyrie,valkyriePos)
        color = (0, 255, 0)
      textMenu = fontMenu.render("Valkyrie", 1, color)
      textPosMenu = textMenu.get_rect()
      textPosMenu.topleft = ( (topleft[0]+160), topleft[1]+110 )
      screen.blit(textMenu, textPosMenu)

      color = WHITE
      if menuSelect[counter] == ARCHER:
        skinfile = open(os.path.join(path, 'archer.cfg'))
        picFile = os.path.join(path,skinfile.readlines()[1].strip())
        archer = display.loadPng(picFile)
        archerPos = archer.get_rect()
        archer = pygame.transform.scale(archer,(96,96))
        archerPos.topleft = (topleft[0]+25,topleft[1]+50)
        screen.blit(archer,archerPos)
        color = (0, 255, 0)
      textMenu =  fontMenu.render("Archer", 1, color)
      textPosMenu = textMenu.get_rect()
      textPosMenu.topleft = ( (topleft[0]+160), topleft[1]+140 )
      screen.blit(textMenu,textPosMenu)

      counter += 1

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        sys.exit()
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
        pygame.display.toggle_fullscreen()
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
        menuSelect[0] -= 1
        if menuSelect[0] < 0:
          menuSelect[0] = 0
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
        menuSelect[0] += 1
        if menuSelect[0] > 3:
          menuSelect[0] = 3
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
        menuSelect[1] -= 1
        if menuSelect[1] < 0:
          menuSelect[1] = 0
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
        menuSelect[1] += 1
        if menuSelect[1] > 3:
          menuSelect[1] = 3
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_HOME:
        menuSelect[2] -= 1
        if menuSelect[2] < 0:
          menuSelect[2] = 0
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_END:
        menuSelect[2] += 1
        if menuSelect[2] > 3:
          menuSelect[2] = 3
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_KP8:
        menuSelect[3] -= 1
        if menuSelect[3] < 0:
          menuSelect[3] = 0
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_KP2:
        menuSelect[3] += 1
        if menuSelect[3] > 3:
          menuSelect[3] = 3
      #Process current selection
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        counter = 1
        for playerSelect in menuSelect:
          if not playerSelect == -1:
            eventPost = events.AddPlayerCharacter((0,0),playerSelect,counter)
            eventManager.post(eventPost)
            eventPost = events.AddPlayerController(counter)
            eventManager.post(eventPost)
#            player = character.Character((0,0),playerSelect,counter)
#            theGame.characterList.append(player)
#            keyboardControllers.append(keyboardcontroller.PlayerController(eventManager,counter))
          counter += 1
        inStartMenu = False

    pygame.display.update()

  return keyboardControllers
