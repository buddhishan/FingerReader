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

t=TimeTaker()

subprocess.call(['sh','/home/root/initial.sh']);
led1=mraa.Gpio(36);
led2=mraa.Gpio(48);
led1.dir(mraa.DIR_OUT);
led2.dir(mraa.DIR_OUT);
led1.write(1);
led2.write(0);


# inside a python interrupt you cannot use 'basic' types so you'll need to use
# objects


def test(gpio):
  #print "edge detected"
  subprocess.call(['sh','/home/root/do.sh'])
    
  c.count+=1


subprocess.call(['sh','fix_nameserver.sh']);
subprocess.call(['rfkill','unblock','bluetooth']);
subprocess.call(['pactl', 'set-default-sink', 'bluez_sink.00_E5_68_21_20_80']);

#45
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
        x.isr(mraa.EDGE_RISING, test, x)
  
        while (1):
		a=5;
        #var = raw_input("Press ENTER to stop")
        x.isrExit()
except ValueError as e:
    print(e)
