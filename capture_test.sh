#!/bin/bash


cd /home/root/bin/ffmpeg;
rm image.jpeg;

#to get a single capture
./ffmpeg -s 640x640 -f video4linux2 -i /dev/video0 -vframes 1 image.jpeg;

#to get several frames,,,, -r 0.5 -  0.5 is frame rate
#./ffmpeg -s 320x240 -f video4linux2 -i /dev/video0 -vframes 2 image_%02d.jpeg;


cd;

#this will save the image file on bin/ffmpeg

