#!/bin/bash
value=$(<textFile.txt)
echo "$value"

#this will send the followning text to IBM server and return the .Wav file to the /root folder
#curl -X POST -u "86423f19-7d0c-4908-8773-3c7086634e74:6G4QUG1Swp5p" --header "Content-Type: application/json" --header "Accept: audio/wav" --data "{\"text\":\"Augmented Human Lab\"}" --output text_audio.wav  "https://stream.watsonplatform.net/text-to-speech/api/v1/synthesize"
#curl -X POST -u "8bf9961b-3375-46e8-b324-436e63cc981a:VT0it11k2VP2" --header "Content-Type: application/json" --header "Accept: audio/wav" --data "{\"text\":\"Augmented Human Lab\"}" --output text_audio.wav  "https://stream.watsonplatform.net/text-to-speech/api/v1/synthesize"


#curl -X POST -u "86423f19-7d0c-4908-8773-3c7086634e74:6G4QUG1Swp5p" --header "Content-Type: application/json" --header "Accept: audio/wav" --data "{\"text\":\" ${value}\"}" --output text_audio.wav  "https://stream.watsonplatform.net/text-to-speech/api/v1/synthesize"

##### Constants
language="en-US"
tmpFile="text_audio.wav"
text=""

##### Main

if [ $# == 1 ]; then
	 text="${1}"
else
   language="${1}"
   text="${2}"   
fi

pico2wave -l=${language} -w=${tmpFile} "`cat ${text}`"
