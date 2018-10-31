#ringtone.rb
#this script retrieves ringtone data using a python script
#to create a .json format file containing two lists
#'freqs' which contains a list of note frequencies
#"durs which cotnains a correspending list of durations in msecs.
#the file is loaded into SOnic Pi and teh two data lists extracted
#they are then played using the chiplead synth
#I've transposed the data down an octave in teh play command
#conversion to sonic pi play format is easy using the buit in hz_to_midi command

#the list of songs refers to those songs whose darta in in the songs.py file
path= '/Users/rbn/src/upy-rtttl/' #path to python files adjust for your system.
song_list=[ "Super Mario - Main Theme","Super Mario - Title Music","SMBtheme",
            "SMBwater","SMBunderground","Picaxe","The Simpsons","Indiana","TakeOnMe",
            "Entertainer","Muppets","Xfiles","Looney","20thCenFox","Bond","MASH",
            "StarWars","GoodBad","TopGun","A-Team","Flinstones","Jeopardy",
            "Gadget","Smurfs","MahnaMahna","LeisureSuit","MissionImp"]
song_list.each do|name| #play each song in turn
  
  cmdtext='/usr/local/bin/python3 '+path+'sp_json.py -n "'+name+'"' #alter python3 binary location for your system.
  
  #typical system call to the python script below
  #system('/usr/local/bin/python3 /Users/rbn/src/upy-rtttl/sp_json.py -n "SMBwater"')
  system(cmdtext) #call the python script to generate .json file
  sleep 0.5
  require 'json'
  file = File.read(path+'sptune.json')
  data_hash = JSON.parse(file)
  f= data_hash['freqs']
  d=data_hash['durs']
  use_bpm 60
  puts "playing ringtone #{name}"
  use_synth :chiplead
  f.zip(d).each do |fr,dur|
    play hz_to_midi(fr)-12,release: dur/1000.0 if fr>0 #transposed down an octave
    sleep dur.to_f/1000
  end
end
