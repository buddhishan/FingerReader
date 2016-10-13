import subprocess
import time

count=0;
start_time=time.time();
while(1):
    subprocess.call(['sh','do.sh'])
    count=count+1;
    print '\n\n************************************'
    print 'TIME ELAPSED : ' + str(time.time()-start_time) + ', COUNT : '+str(count)
    print '*************************************\n\n'
    time.sleep(5)
        
    
