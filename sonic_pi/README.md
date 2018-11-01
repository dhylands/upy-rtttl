# Additions for using RTTL with Sonic Pi #
The files in this folder enable the data retrieved from the songs.py file
to be parsed by rtttl.py and for the resulting frequency and time pairs
to be transferred for playing on the music program Sonic Pi using its
built in chiplead synth.
Sonic Pi can be downloaded from **sonic-pi.net**

Two methods are employed:
1. utilising a **json** format file
1. utilising **OSC messages**, which can be broadcast to play on several synced Sonic Pi machines

The first method uses the two files **sp_json.py** and **ringtone.rb** The former python script 
is run in a terminal using `./sp_json.py` It requires read/write acces to its location as it generates a data file
named **sptune.json** This is subsequently read by the program **ringtone.rb** which is run in Sonic Pi.
The second requirement for the python script is that it needs the files rtttl.py and songs.py. Since these are in the 
parent folder you need soft links to these from the sonic_pi folder using

```ln -s ../rtttl.py rtttl.py```

and

```ln -s ../songs.py songs.py```

respectively. I have created these in the distribution for you.

The second method is more elegant, not requiring any intermediate data file. However you will have to install
an additional python library using

```pip3 install python-osc```

Once again two files are required. A python script called **spOSC2.py** and a Sonic Pi program called **ringtoneOSC.rb**
A third (optional) Sonic Pi player script called **ringtoneSLAVE.rb** can be run on any additional Sonic Pi computers,
and they will play the tune currently being broadcast, all synchronised together.

The **spOSC2.py** script has three functions. First it runs a OSC server listening form messages on port 8000. It is configured to
respond to two messages addressed to **"/name"** and to **"/abort"** The first of these messages expects one piece of data,
the name of the rtttl tune to be played. The second message can be used to abort a tune before it finishes playing.
The second function is to retrieve the frequency/duration paris of data for the notes in the tune, and this utilises the
rtttl.py parser functions and uses tune data from the songs.py file. Once again, you need the aliases
pointing to these files to created in the soinc_pi folder as described above. The retrieveal of teh data is carried out in
the **getData** function in the script. The third function is also carried out in the same **getData** function and that is
to broadcast the frequency/duration pairs using an OSC message addressed to "/ringdata" This is subsequently picked up by any
Sonic Pi computer on the same local network listening on port 4559. The script is hardwired to use local newtwork broadcast
address 192.168.1.255, but you can alte that if your local network uses a differnt range, eg 10.0.0.255 The getData script also
broadcasts an OSC message addressed to "/finished" to signify the end of each tune when all its data has been broadcast.

The associated Sonic Pi program **ringtoneOSC.rb** has two live_loops. The second of these named **:PlaySong** contains
a list of the rtttl tunes in the songs.py script. It chooses one of these at random storing the name in the variable **name**
and then sends an osc message `osc "/name",name` to the osc server running on the python script spOSC2.py.
It then waits for a returned osc message "/finished" sent back from the python script. Note that Sonic Pi inserts some
information at the front of the received message and so the script looks for the message `/osc*/finished` where * is a wild card
which allows the program to work with both the existing 3.1 or 3.01 releases, but also with new features
in the current 3.2dev version of Sonic Pi. When this is received it continues the live_loop with a subsequent tune.
The first live_loop named **:playring** waits to receive broadcast messages from the python script addressed to  "/ringdata"
Again Sonic Pi will present this as `"/osc*/ringdata"` It extracts the freq and duration data and then plays the note using
the chiplead synth which simulates the sound produced in a nokia phone. The frequency is first converted to a midi number (which can
for Sonic Pi have a fractional part) and I then lower it an octave by subtracting 12. Frequency values of 0
(which are used for rests) are ignored.The note decays over its duration.
The final point to note, is that if you wish to stop a tune while it is playing you can send an osc message `"/abort"`
to the python script from Sonic Pi. Once ringtoneSP.rb is running, you can uncomment the two lines
```
##| osc "/abort"
##| stop
```
and then rerun the program WITHOUT stopping it first. This will just send the osc abort message but will leave the live loops
running, and the playSong loop will receive a finished message and will immediately start a fresh song playing. Of course
if you do stop the Sonic Pi scrpit completely, you will have to comment out the two lines again.
