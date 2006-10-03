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


#
# This file is for generic setup for distribution
# It uses the MANIFEST.in to choose which files to include.

from distutils.core import setup
from setup_data import *

setup(name=NAME,
      version=VERSION,
      author='PyGauntlet Team',
      author_email='http://groups.google.com/group/pygauntlet'
      url='http://code.google.com/p/pygauntlet/',
      description='Python Gauntlet Game',

      )

      #py_modules=['barrier', 'character', 'config', 'cpucontroller',\
      #            'display', 'errors', 'eventmanager', 'events', 'exit',\
      #            'game', 'gauntlet', 'immobile', 'item', \
      #            'keyboardcontroller', 'mapgenerate', 'map', 'menu', \
      #            'mobile', 'monstergenerator', 'projectile', \
      #            'pygamedisplay', 'pyopengldisplay', 'sound', 'stats', \
      #            'textdisplay'],