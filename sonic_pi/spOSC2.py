#!/usr/bin/env python3
#This script is controlled by an incoming osc message from Sonic Pi containing
#the name of one of the rtttl pieces in the songs.py file
#it extracts the frequency and duration (msec) data for this song
#and sends each corresponding pair of data items in a broadcast osc message
#These can be picked up by Sonic Pi and played using the chiplead synth
#The data processing is similar to that in the pc_test.py script
#it requires the libarary python-osc to be installed
#using sudo pip3 install python-osc
 
from rtttl import RTTTL
import songs
import argparse
from time import sleep
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server
playing=False #global flag used to abort playing
broadcastAddress='192.168.1.255' #adjust for the network you want to use
#note 4559 is Sonic Pi port for incoming OSC cues
#set up client udp broadcast (broadcast enabled by third parameter True)
client = udp_client.SimpleUDPClient(broadcastAddress, 4559,True)

def getData(unused_addr,args,name): #broadcasts data for ringtone name
    global playing
    playing=True  
    tune = RTTTL(songs.find(name))  
    print("Playing ringtone {}".format(name))
    for freq, msec in tune.notes(): #send the data pairs for the notes
        msg=[] #prepare data message
        msg.append(freq)
        msg.append(msec)
        client.send_message("/ringdata",msg) #broadcast next data pair
        sleep(msec/1000.0) #sleep for duration of note
        #stop current song if playing set to False by received "/abort" message
        if playing==False: 
            break 
    client.send_message("/finished",True) #broadcasts osc msg when finished
    
def killPlay(unused_addr): #sets playing flag to False when "/abort" received
    global playing    
    playing=False
    print("Playing stopped")

try:
    #set up dispatcher to handle incoming OSC messages
    dispatcher = dispatcher.Dispatcher() #initialise dispatcher
    #check incoming OSC messages and dispatch handlers for matching ones
    #handler for "/name" calls getData with name of ringtone as a parameter
    dispatcher.map("/name", getData,"name") #get name of ringtone to play
    #handler for "/abort" calls killPlay
    dispatcher.map("/abort",killPlay) #this dispatcher is used to abort playing
    #set up server on localhost linked to dispatcher
    server = osc_server.ThreadingOSCUDPServer( ('127.0.0.1', 8000), dispatcher)
    #print configuration data on terminal screen
    print("Serving on {}".format(server.server_address))
    print("Data broadcast to {} to port {}".format(broadcastAddress,4559))
    #start serving    
    server.serve_forever()

#allow clean ctrl-C exit
except KeyboardInterrupt:
    print("\nProgram exit")
