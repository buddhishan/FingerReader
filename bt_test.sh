#!/bin/bash   
       
VAR="$(pactl list sinks)"


 
if [[ "$VAR" =~ "rboldu" ]]; then
    echo "matched"
else
    echo "didn't match"
fi
