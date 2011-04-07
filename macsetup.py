#Copyright 2006 Josef Spjut
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
"""
Script for building pygauntlet on Mac OS X.

Usage:
    python macsetup.py py2app

For list of available commands run:
    python macsetup.py py2app help
"""
from distutils.core import setup
# This is probably not needed for the regular setup
import bdist_mpkg
import py2app
from setup_data import *

import sys
sys.path.append('src')

# This is a list of things to include in the application plist
# 
plist = dict(
    CFBundleIconFile=NAME,
    CFBundleName=NAME,
    CFBundleVersion=''.join([VERSION]),
    CFBundleShortVersionString=VERSION,
    CFBundleGetInfoString=' '.join([NAME, VERSION]),
    CFBundleExecutable=NAME,
)

# These options are for the following:
# argv_emulation - Allows the application to boot from the bundle
# iconfile - Makes a nice looking bundle. The icon while running still needs
#    to be set in the game.
py2app_options = dict(
    argv_emulation=True,
    iconfile='data/images/icon.icns',
    )

setup(
    data_files=['./data'],
    app=[
        dict(script="pygauntlet.py", plist=plist),
    ],
#    app=['gauntlet.py'],
    options=dict(py2app=py2app_options,),
    name=NAME,
    version=VERSION,
    author='PyGauntlet Team',
    author_email='http://groups.google.com/group/pygauntlet',
    url='http://code.google.com/p/pygauntlet/',
    description='Python Gauntlet Game',
)
