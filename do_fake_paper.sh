#!/bin/bash

cd /home/root/
#sudo sh fix_nameserver.sh &
rfkill unblock bluetooth &
#pactl set-default-sink bluez_sink.00_E5_68_21_20_80 &
#pactl set-sink-volume @DEFAULT_SINK@ 20% 20% &

wait
#gst-launch-1.0 filesrc location= /home/root/fingerreader_is_reading.wav ! wavparse ! pulsesink  &
#sudo sh capture_test.sh &

wait
#sudo python send_to_ms_server.py
#sudo sh text_to_speech.sh textFile.txt
gst-launch-1.0 filesrc location= fake_paper.wav ! wavparse ! pulsesink
sudo sh thermal_check.sh

cd

