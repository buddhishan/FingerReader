import httplib, urllib, base64,json

#Converting jpeg to byte array
from array import array
f = open("/home/root/bin/ffmpeg/image.jpeg", "rb")
bytes = bytearray(f.read())

headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': 'f91fb02b98784d7a9d7b5d89c34b9ba0',
}

params = urllib.urlencode({
     #Request parameters
    'language': 'unk',
    'detectOrientation ': 'true',
})

#try:
conn = httplib.HTTPSConnection('api.projectoxford.ai')
conn.request("POST", "/vision/v1.0/ocr?%s" % params, bytes, headers)

#conn = httplib.HTTPSConnection('10.21.115.184:3000')
#conn.request("POST", "/fingerreader?%s" % params, bytes, headers)

#conn = httplib.HTTPSConnection('requestb.in')
#conn.request("POST", "/13cvw471?%s" % params, bytes, headers)

response = conn.getresponse()
data = response.read()
print(data)

#print ("Status of Response : ")
#print (response.status)

conn.close()

#replacing unwanted chatacters to get the prefered text.
data=data.replace('}:{','');
data=data.replace('},{','');
for ch in ['":"', '","', '"}', '""' ]:
    if ch in data:
        data=data.replace(ch," ");

data=data.split();
text="";

#creating prefered 'text'
for i in range(len(data)) :
    if i == len(data)-1 :
        break;
    else:
        if data[i]=='text':
            text=text+" "+data[i+1];
            
print text;

file=open("./textFile.txt","w");
if (text==""):
    file.write("No Readable text recognised")
    print "No Readable text recognised";
else :
    file.write(text);
file.close();




#except Exception as e:
    #print("[Errno {0}] {1}".format(e.errno, e.strerror))

##
##
##if (response.status == 200):
##    print "OCR Positive Reply";
##elif (response.status == 400):
##    print "Could not extract image features, Try again";
##else :
##    print "Someother error";

    
