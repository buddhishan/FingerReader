import subprocess
while (1):
    out=subprocess.check_output(["pactl", "list","sinks"])
    #print out;
    if ('rboldu' in out ):
        print "yes";
    else:
        print "no";