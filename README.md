#About Pygauntlet
Pygauntlet is a project started at the UCR department of Computer Science for a class in software engineering. The project is currently maintained by Josef Spjut, but is not actively being worked on.

#Mac Install Directions
Assuming you have homebrew installed.

  1. Install pygame. [source](https://bitbucket.org/pygame/pygame/issue/82/homebrew-on-leopard-fails-to-install#comment-627494)
  2. Install pyopengl. [source](http://pyopengl.sourceforge.net/)

How to install pygame in your path:
```
brew install sdl sdl_image sdl_mixer sdl_ttf smpeg portmidi 
sudo pip install hg+http://bitbucket.org/pygame/pygame
```
How to install pygame in homebrew python install:
```
brew install python
brew install sdl sdl_image sdl_mixer sdl_ttf smpeg portmidi 
/usr/local/share/python/pip install hg+http://bitbucket.org/pygame/pygame
```
How to install pyopengl
```
pip install PyOpenGL PyOpenGL_accelerate
```

#Other OS
Should work fine, but you are on your own until I find the time to update this...

#Blog
There is an [http://pygauntlet.blogspot.com old blog] but it's basically dead.



#OLD README BELOW

README - version 0.7.9

Requirements:
  python - http://www.python.org/download
  pygame - http://www.pygame.org/download.shtml

Optional Packages:
  pyopengl - http://pyopengl.sourceforge.net

Installation/Execution:
  In the following instructions you should replace the x.x in
  pygaultlet-x.x.tar.gz with the actual version you have.

  Windows:
    uncompress "pygauntlet-x.x.tar.gz" file into a new directory
    run "gauntlet.py" found in the new directory with a 
    python interpreter
  Linux:
    tar -xvzf pygauntlet-x.x.tar.gz
    cd pygauntlet-x.x
    python gauntlet.py
  Mac:
    tar -xvzf pygauntlet-x.x.tar.gz
    cd pygauntlet-x.x
    pythonw gauntlet.py

Initialization:
  The game starts at the main menu where you can choose to start the
  game, change skins, or quit. Once you choose to start the game, each
  player can choose his or her character by pressing up and down. Once
  all players have chosen, press enter to begin the game.

Controls:
  The default controls are as follows:

  Player #1
    Up		w
    Down	s
    Left	a
    Right	d
    Attack	v
    Magic	b
  Player #2
    Up		up
    Down	down
    Left	left
    Right	right
    Attack	k
    Magic	l
  Player #3
    Up		HOME
    Down	END
    Left	DELETE
    Right	PAGEDOWN
    Attack	BACKSPACE
    Magic	BACKSLASH
  Player #4
    Up		NUMPAD_8
    Down	NUMPAD_2
    Left	NUMPAD_4
    Right	NUMPAD_6
    Attack	NUMPAD_+
    Magic	NUMPAD_ENTER
    *these apply to the numpad

Gameplay:
  Advance through the game by finding exits and moving on top of them in order
  to teleport to the next level. Eliminate monsters as you proceed through the
  game in order to avoid dying as well as accumulating points. There are three
  tactics used to destroy enemy monsters. Firstly, simply moving your character
  onto monster performs a melee attack but at the risk of taking damage.
  Secondly, projectiles can be thrown using the player's attack button (each
  player has an unlimited number of projectiles that can be thrown). Lastly,
  magic can be used to kill monsters within a radius of the character using
  magic, however, in order to use magic the player must have a magic potion for
  every magic use. The results of all of the actions are based on the stats of
  the characters and vary for each class. Various items can be picked up
  throughout the game: food increases the player's health, keys open doors that
  will prevent the player from reaching exits, treasure increases the player's
  gold, and potions allow magic use. Monster generators will also randomly
  appear in the game which create monster characters that will attempt to end
  the player's quest(s).

Notes:
  Custom maps and series of maps can also be loaded by following the
  instructions found in the MAP_EDITOR_README.

  Custom skins/appearance can be created following the instructions in
  SKIN_README.

  Custom monster behavior can be programmed following the instructions
  in STATE_MACHINE_README.
