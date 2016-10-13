import httplib, urllib, base64,json
import requests

#Converting jpeg to byte array
from array import array
f = open("/home/root/bin/ffmpeg/image.jpeg", "rb")
bytes = bytearray(f.read())

#Sending the POST request to FR cloud
r = requests.post("https://fingerreaderbasicapp.herokuapp.com/fingerreader", data=bytes)
print(str(r.text))

#manipulating the requestObject to get the desired text
jsonString = str(r.text);
for ch in ['{"',  '"}',  '":"', '","']:
    if ch in jsonString :
        jsonString=jsonString.replace(ch,'+');
jsonSplit=jsonString.split('+');
print jsonSplit;

file=open("./textFile.txt","w");
if jsonSplit[2]=='success' :
    file.write(jsonSplit[-2]);
else :
    file.write("Error : " + jsonSplit[-2]);
file.close();


