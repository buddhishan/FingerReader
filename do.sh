#!/bin/bash

cd /home/root/
sh fix_nameserver.sh &
rfkill unblock bluetooth &

pactl set-default-sink bluez_sink.00_E5_68_21_20_80 &
#pactl set-sink-volume @DEFAULT_SINK@ 24% 25% &

wait
gst-launch-1.0 filesrc location= /home/root/fingerreader_is_reading.wav ! wavparse  ! pulsesink  &
sh capture_test.sh &
wait
python send_to_ms_server.py
sh text_to_speech.sh textFile.txt
sh convert_wav.sh
gst-launch-1.0 filesrc location= text_audio.wav ! wavparse ! pulsesink 
sh thermal_check.sh

cd

