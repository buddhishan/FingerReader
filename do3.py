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
        time.sleep(0.3);
        led1.write(0);
        led2.write(0);
        time.sleep(0.3);


# inside a python interrupt you cannot use basic types 

def test(gpio):

  if (gpio.read()==0) :
    print 'negative egde'

     

  else :
    print 'physical positive edge'
    if (c._fake_count ==0 ):
        print 'fake book is reading'
	time.sleep(1);
        subprocess.call(['sh','do_fake_book.sh'])
        led1.write(1);
        led2.write(1);
        c._fake_count =1;
    elif (c._fake_count==1):
        print 'fake paper is reading'
        time.sleep(1);
        subprocess.call(['sh','do_fake_book.sh'])
        led1.write(1);
        led2.write(0);
        c._fake_count=0;


  
  c.count+=1







subprocess.call(['sh','fix_nameserver.sh']);
subprocess.call(['rfkill','unblock','bluetooth']);

#47 is the pin for hardcoded camera button
pin = 47;

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
