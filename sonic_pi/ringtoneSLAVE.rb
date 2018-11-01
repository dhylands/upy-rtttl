#ringtoneSLAVE.rb
#by Robin Newman, November 2018
#This script can run a Sonic Pi on the same local network as the one
#running the ringtoneOSC.rb file
#it will receive and play broadcast data from the associated spOSC2.py python script

live_loop :playring do #this live_loop receives and plays broadcast daat from the OSC server
  use_real_time
  use_synth :chiplead
  b= sync "/osc*/ringdata"
  play hz_to_midi(b[0])-12,release: b[1]/1000.0 if b[0] > 0
end

