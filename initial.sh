cd /home/root/
rfkill unblock bluetooth;
pactl set-default-sink bluez_sink.00_E5_68_21_20_80 & 
#wait
#pactl set-sink-volume @DEFAULT_SINK@ 20% 20%

wait

#!/bin/bash
#touch samplefile.txt;

echo "Error!!, Please check the Camera and Internet Connectivity" > /home/root/textFile.txt;

gst-launch-1.0 filesrc location= /home/root/ready.wav ! wavparse ! pulsesink 

cd
