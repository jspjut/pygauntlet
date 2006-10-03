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

from config import *
from weakref import WeakKeyDictionary
import events
from events import *

REGISTERCLIENT = 0

##\brief The event manager
##
##used for posting/notifying components of our game about events

##be extended to allow a pygame or opengl display class to work.
#do this later to make our program more efficient:
#  only send certain events to certain listeners so
#  that the listeners only hear what they should hear
class EventManager:

  ##\brief EventManger constructor
  ##
  ##\param options the options sent from the command-line and menu
  ##\param role networking variable
  ##\return None

  def __init__ ( self, options, role=REGULAR ):
    #self.listeners = WeakKeyDictionary()
    self.listeners = {}
    self.verbose = options.verbose
    self.nextClientID = 1
    self.role = role
    try:
      if options.netmaster:
        self.role=SERVER
      elif options.serveraddr != "":
        print "serveraddr is "+str(options.serveraddr)
        self.serveraddr = "127.0.0.1"
        self.role = CLIENT
    except AttributeError:
      pass
    self.clients = {}
    if self.role == SERVER or \
       self.role == CLIENT:
      self.startListening()

  def startListening(self):
    
    # Set the socket parameters
    host = "127.0.0.1"
    if self.role == SERVER:
      port = 21567
    else:
      port = 21568
    buf = 1024
    addr = (host,port)
    addrList = []
    
    # Create socket and bind to address

    # register with the server if this is a client
    if self.role == CLIENT:
      pass

  def stopListening(self):
    # Close socket
    self.listenUDPSock.close()
  
    
  def setRole( self, role=1,serveraddr="127.0.0.1"):
    self.role = role
    if role == CLIENT:
      self.serveraddr = serveraddr
      self.network_post(marshal.dumps({'eventid':REGISTERCLIENT}),
                        self.serveraddr)

  ##\brief registers a listener
  ##
  ##registers a listener to listen for events posted
  ##
  ##\param listener the listener to register
  ##\return None

  def registerListener ( self, listener ):
    self.listeners[listener] = 1

  ##\brief unregisters a listener
  ##
  ##unregisters a listener to listen for events posted
  ##
  ##\param listener the listener to unregister
  ##\return None

  def unregisterListener ( self, listener ):
    if listener in self.listeners.keys():
      del self.listeners[listener]


  ##\brief post an event
  ##
  ##posts an event and tells all listeners
  ##
  ##\param event the event being posted
  ##\return None

  def post ( self, event ):
#    print "event "+str(marshal.dumps(event))
    if self.verbose:
      if not isinstance(event,events.TickEvent) and \
         not isinstance(event,events.DisplayTickEvent) and \
         not isinstance(event,events.CharacterCollisionEvent) and \
         not isinstance(event,events.CharacterMovePress) and \
         not isinstance(event,events.CharacterMoveRelease) and \
         not isinstance(event,events.CharacterMoveEvent):
        print "EventManager: " + str(event)
    if self.role == REGULAR:
      #just post it locally, no network
      for listener in self.listeners.keys():
        listener.notify(event)
    if self.role == SERVER:
      pass
      #post events that are meant for the network

  def network_post(self,postdata,address):
    pass
  
