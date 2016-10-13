import mraa
import time
import sys
import subprocess

class Counter:
  count = 0
  _fake_count=0;

c = Counter()

class TimeTaker:
  _time=0
  _start_time=0
  _mode = 'fake'
  _a=0;
  _time_flag=0;
  _positive_flag=0;

t=TimeTaker()


led1=mraa.Gpio(36);
led2=mraa.Gpio(48);
led1.dir(mraa.DIR_OUT);
led2.dir(mraa.DIR_OUT);

subprocess.call(['rfkill','unblock','bluetooth'])
#check whether BT is connected before saying ready
time.sleep(2);
while (1):
    out=subprocess.check_output(["pactl", "list","sinks"])
    if ('rboldu' in out ):
        subprocess.call(['sh','initial.sh']);
        led1.write(1);
        led2.write(0);
        break;          
    else:
        print "BT Error";
        led1.write(1);
        led2.write(1);
        time.sleep(0.4);
        led1.write(0);
        led2.write(0);
        time.sleep(0.4);


# inside a python interrupt you cannot use basic types 

def test(gpio):

  if (gpio.read()==0) :
    print 'negative egde'
    t._start_time=time.time();
    t._time_flag=0;
    t._positive_flag=0;
    while  ((time.time()-t._start_time)<4) :
      t._a=0;
      if (gpio.read()==1) :
        t._positive_flag=1;
        t._time=time.time() - t._start_time;
        break;
    if (t._positive_flag==1):
      print " small button detected";
      if (t._time >0.5 and t._time <2.5 ) :
        print "0.5 to 2.5"
        if (t._mode =='real'):
	  print 'real reading'
          subprocess.call(['sh','/home/root/do.sh'])
        elif (t._mode == 'fake'):
          print "fake readings start";
          if (c._fake_count==0):
            print "fake book is reading"
            subprocess.call(['sh','/home/root/do_fake_book.sh'])
            c._fake_count=1;
	    led1.write(1);
	    led2.write(1);

          elif (c._fake_count==1):
            print "fake paper is reading"
	    subprocess.call(['sh','/home/root/do_fake_paper.sh'])
            c._fake_count=0;
	    led1.write(1);
	    led2.write(0);
      else :
        print "make no sense";
##
    
    elif (t._positive_flag==0):
      print "change mode";
      print "changing mode";
      if (t._mode=='fake'):
        t._mode='real';
        print "mode changed to real"
        led1.write(0);
        led2.write(1);
      elif (t._mode=='real'):
        t._mode='fake';
        print "mode changed to fake"
        c._fake_count=0;
        led1.write(1);
        led2.write(0);    

      

  else :
    print 'physical positive edge'

  
  c.count+=1







subprocess.call(['sh','fix_nameserver.sh']);
subprocess.call(['rfkill','unblock','bluetooth']);
pin = 45;

#while(1):
if (len(sys.argv) == 2):
  try:
    pin = int(sys.argv[1], 10)
  except ValueError:
    printf("Invalid pin " + sys.argv[1])
try:	
	edge=0;
        x = mraa.Gpio(pin)
        print("Starting ISR for pin " + repr(pin))
        x.dir(mraa.DIR_IN)
        x.isr(mraa.EDGE_BOTH, test, x)
  
        while (1):
		#a=5;
                out=subprocess.check_output(["pactl", "list","sinks"])
                if ('rboldu' in out ):
                    a=5;
                    if(t._mode=='fake'):
                        led1.write(1);
                        if (c._fake_count==0):
                            led2.write(0);
 			elif (c._fake_count==1):
                            led2.write(1);
                    elif (t._mode=='real'):
                        led1.write(0);
                        led2.write(1);
                else:
                    print "BT Error";
                    led1.write(1);
                    led2.write(1);
                    time.sleep(0.4);
                    led1.write(0);
                    led2.write(0);
                    time.sleep(0.4);
        #var = raw_input("Press ENTER to stop")
        x.isrExit()
except ValueError as e:
    print(e)
