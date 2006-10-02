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


##\brief Error objects for error handling
##
##to be used for exception handling

class Error ( Exception ):

  ##\brief Error constructor
  ##
  ##\param message the error message to be displayed
  ##\return None

  def __init__ ( self, message ):
    self.__message = message

  ##\brief Error string conversion
  ##
  ##returns the error message for printing
  ##
  ##\return message representing the error message

  def __str__ ( self ):
    return self.__message
