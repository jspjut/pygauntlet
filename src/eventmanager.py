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
from socket import *
import cPickle as marshal
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
    self.checkingBuffers = False
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
    self.listenUDPSock = socket(AF_INET,SOCK_DGRAM)
    self.listenUDPSock.setblocking( False )
    self.listenUDPSock.bind(addr)

    # register with the server if this is a client
    if self.role == CLIENT:
      self.network_post(marshal.dumps({'eventid':REGISTERCLIENT}),
                        self.serveraddr)

  def checkBuffers(self):
    if self.checkingBuffers:
      return False
    self.checkingBuffers = True
    buf=1024
    # Receive messages
    try:
      data,addr = self.listenUDPSock.recvfrom(buf)
      #    if addr not in addrList:
      #      addrList.append(addr)
      if not data:
        print "no data!"
      else:
        dictdata = marshal.loads(data)
        if self.role == CLIENT:
#          print "Client received message "
          if dictdata['eventid'] == TICKEVENT:
            event = events.TickEvent()
            for listener in self.listeners.keys():
              listener.notify(event)
          elif dictdata['eventid'] == DISPLAYTICKEVENT:
            event = events.DisplayTickEvent()
            for listener in self.listeners.keys():
              listener.notify(event)
          elif dictdata['eventid'] == STARTGAMEEVENT:
            event = self.startevent
            for listener in self.listeners.keys():
              listener.notify(event)
          elif dictdata['eventid'] == GAMEOVEREVENT:
            event = events.GameOverEvent()
            for listener in self.listeners.keys():
              listener.notify(event)
          elif dictdata['eventid'] == CHARACTERMOVEPRESS:
            event = events.CharacterMovePress(dictdata['charID'],
                                              dictdata['dir'])
            for listener in self.listeners.keys():
              listener.notify(event)
            
          elif dictdata['eventid'] == ADDPLAYERCHARACTER:
            print "network receive client addplayer"
            event = events.AddPlayerCharacter(dictdata['pos'],
                                              dictdata['classType'],
                                              dictdata['ID'])
            for listener in self.listeners.keys():
              listener.notify(event)
          elif dictdata['eventid'] == ADDPLAYERCONTROLLER:
            event = events.AddPlayerController(dictdata['ID'])
            for listener in self.listeners.keys():
              listener.notify(event)
            
            
          elif dictdata['eventid'] == CHARACTERMOVERELEASE:
            event = events.CharacterMoveRelease(dictdata['charID'],
                                                dictdata['dir'])
            for listener in self.listeners.keys():
              listener.notify(event)
          elif dictdata['eventid'] == CHARACTERATTACKPRESS:
            event = events.CharacterAttackPress(dictdata['charID'])
            for listener in self.listeners.keys():
              listener.notify(event)
          elif dictdata['eventid'] == CHARACTERATTACKRELEASE:
            event = events.CharacterAttackRelease(dictdata['charID'])
            for listener in self.listeners.keys():
              listener.notify(event)
          elif dictdata['eventid'] == CHARACTERMAGICPRESS:
            event = events.CharacterMagicPress(dictdata['charID'])
            for listener in self.listeners.keys():
              listener.notify(event)
          elif dictdata['eventid'] == CHARACTERMAGICRELEASE:
            event = events.CharacterMagicRelease(dictdata['charID'])
            for listener in self.listeners.keys():
              listener.notify(event)
          elif dictdata['eventid'] == CHARACTERMAGICATTACK:
            event = events.CharacterMagicAttack(dictdata['charID'])
            for listener in self.listeners.keys():
              listener.notify(event)

        elif self.role == SERVER:
#          print "Server received message "
          if dictdata['eventid'] == REGISTERCLIENT:
            self.registerClient(addr[0])
          else:
            if dictdata['eventid'] == ADDPLAYERCHARACTER:
              print "network receive server addplayer"
            for key in self.clients.keys():
              print "posting to "+str(self.clients[key])+": "+str(data) 
              self.network_post( data, self.clients[key] )
      self.checkingBuffers = False
      return True
    except error:
      self.checkingBuffers = False
      return False

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

  def registerClient ( self, ip ):
    self.clients[self.nextClientID] = ip
    self.nextClientID += 1

  def unregisterClient ( self, client ):
    if client in self.clients.keys():
      del self.clients[clients]


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
      #post events that are meant for the network
      if isinstance( event, events.TickEvent ):
        for key in self.clients.keys():
          self.network_post(marshal.dumps({'eventid':TICKEVENT}),
                       self.clients[key])
      elif isinstance( event, events.DisplayTickEvent ):
        for key in self.clients.keys():
          self.network_post(marshal.dumps({'eventid':DISPLAYTICKEVENT}),
                       self.clients[key])
      elif isinstance( event, events.GameOverEvent ):
        for key in self.clients.keys():
          self.network_post(marshal.dumps({'eventid':GAMEOVEREVENT}),
                       self.clients[key])
      elif isinstance( event, events.AddPlayerCharacter ):
        print "network post server addplayer"
        for key in self.clients.keys():
          self.network_post(marshal.dumps({'eventid':ADDPLAYERCHARACTER,
                                           'pos':event.position,
                                           'classType':event.classType,
                                           'ID':event.ID}),
                       self.clients[key])
      elif isinstance( event, events.AddPlayerController ):
        for key in self.clients.keys():
          self.network_post(marshal.dumps({'eventid':ADDPLAYERCONTROLLER,
                                           'ID':event.ID}),
                       self.clients[key])
      elif isinstance( event, events.StartGameEvent ):
        for key in self.clients.keys():
          self.network_post(marshal.dumps({'eventid':STARTGAMEEVENT}),
                            self.clients[key])

      #even if it's meant for the network, it gets posted locally
      for listener in self.listeners.keys():
        listener.notify(event)
    
      while self.checkBuffers():
        pass
    if self.role == CLIENT:
      if isinstance( event,events.CharacterMovePress ):
        self.network_post(marshal.dumps({'eventid':CHARACTERMOVEPRESS,
                                    'charID':event.characterID,
                                    'dir':event.direction}),
                     self.serveraddr)
      elif isinstance( event, events.AddPlayerCharacter ):
        print "network post client addplayer"
        self.network_post(marshal.dumps({'eventid':ADDPLAYERCHARACTER,
                                         'pos':event.position,
                                         'classType':event.classType,
                                         'ID':event.ID}),
                          self.serveraddr)
      elif isinstance( event, events.AddPlayerController ):
        self.network_post(marshal.dumps({'eventid':ADDPLAYERCONTROLLER,
                                           'ID':event.ID}),
                          self.serveraddr)
      elif isinstance( event, events.StartGameEvent ):
        self.startevent = event
      elif isinstance( event,events.CharacterMoveRelease ):
        self.network_post(marshal.dumps({'eventid':CHARACTERMOVERELEASE,
                                    'charID':event.characterID,
                                    'dir':event.direction}),
                     self.serveraddr)
          
      elif isinstance( event,events.CharacterAttackPress ):
        self.network_post(marshal.dumps({'eventid':CHARACTERATTACKPRESS,
                                    'charID':event.characterID}),
                     self.serveraddr)
            
      elif isinstance( event,events.CharacterAttackRelease ):
        self.network_post(marshal.dumps({'eventid':CHARACTERATTACKRELEASE,
                                    'charID':event.characterID}),
                     self.serveraddr)
              
      elif isinstance( event,events.CharacterMagicPress ):
        self.network_post(marshal.dumps({'eventid':CHARACTERMAGICPRESS,
                                    'charID':event.characterID}),
                     self.serveraddr)
                
      elif isinstance( event,events.CharacterMagicRelease ):
        self.network_post(marshal.dumps({'eventid':CHARACTERMAGICRELEASE,
                                    'charID':event.characterID}),
                     self.serveraddr)
      elif isinstance( event,events.CharacterMagicAttack ):
        self.network_post(marshal.dumps({'eventid':CHARACTERMAGICATTACK,
                                    'charID':event.characterID}),
                     self.serveraddr)
      else:
        #initially, you think these should get posted locally, too.
        #However, the server re-posts these to the network, so...
        for listener in self.listeners.keys():
          listener.notify(event)

#quitevent should be handled (convert to character die or something like that)
#        events.QuitEvent ( Event ):

        while self.checkBuffers():
          pass
  def network_post(self,postdata,address):
    host = address
    if self.role == SERVER:
      port = 21568
    else:
      port = 21567
    buf = 1024
    addr = (host,port)

    # Create socket
    UDPSock = socket(AF_INET,SOCK_DGRAM)
    
    # Send messages
#    postdata = "test write"
    if(UDPSock.sendto(postdata,addr)):
      pass
#      print "Sending message '",postdata,"' to address"+str(postdata)+".....<done>"
#    data,addr = UDPSock.recvfrom(buf)
#    print data
    
    # Close socket
    UDPSock.close()
