
import mraa;
import time;
import subprocess;

i2c = mraa.I2c(1);
i2c.address(0x5a);
#i2c.writeReg(0x41,0x1a);
#time.sleep(1);
#a= i2c.readReg(0x41);
#print a;

MPR121_I2CADDR_DEFAULT = 0x5A;

MPR121_TOUCHSTATUS_L = 0x00
MPR121_TOUCHSTATUS_H = 0x01
MPR121_FILTDATA_0L  =0x04
MPR121_FILTDATA_0H = 0x05
MPR121_BASELINE_0  = 0x1E
MPR121_MHDR        = 0x2B
MPR121_NHDR        = 0x2C
MPR121_NCLR        = 0x2D
MPR121_FDLR       =  0x2E
MPR121_MHDF        = 0x2F
MPR121_NHDF         =0x30
MPR121_NCLF        = 0x31
MPR121_FDLF        = 0x32
MPR121_NHDT        = 0x33
MPR121_NCLT        = 0x34
MPR121_FDLT        = 0x35

MPR121_TOUCHTH_0   = 0x41
MPR121_RELEASETH_0  =  0x42
MPR121_DEBOUNCE =0x5B
MPR121_CONFIG1 =0x5C
MPR121_CONFIG2 =0x5D
MPR121_CHARGECURR_0 =0x5F
MPR121_CHARGETIME_1 =0x6C
MPR121_ECR =0x5E
MPR121_AUTOCONFIG0 =0x7B
MPR121_AUTOCONFIG1 =0x7C
MPR121_UPLIMIT   =0x7D
MPR121_LOWLIMIT  =0x7E
MPR121_TARGETLIMIT = 0x7F

MPR121_GPIODIR  =0x76
MPR121_GPIOEN  =0x77
MPR121_GPIOSET = 0x78
MPR121_GPIOCLR = 0x79
MPR121_GPIOTOGGLE = 0x7A

MPR121_SOFTRESET =0x80

def setThresholds(touch,release):
	for i in range (0,12):
		i2c.writeReg(MPR121_TOUCHTH_0 + 2*i, touch);
    		i2c.writeReg(MPR121_RELEASETH_0 + 2*i, release);



def begin() :

	i2c.writeReg(MPR121_SOFTRESET, 0x63);
	time.sleep(1);

	i2c.writeReg(MPR121_ECR, 0x0);
	c = i2c.readReg(MPR121_CONFIG2);
	if (c!= 0x24) :
		return False;

 	#12,6
	setThresholds(25,25);

	i2c.writeReg(MPR121_MHDR, 0x01);
  	i2c.writeReg(MPR121_NHDR, 0x01);
  	i2c.writeReg(MPR121_NCLR, 0x0E);
  	i2c.writeReg(MPR121_FDLR, 0x00);

	i2c.writeReg(MPR121_MHDF, 0x01);
  	i2c.writeReg(MPR121_NHDF, 0x05);
  	i2c.writeReg(MPR121_NCLF, 0x01);
  	i2c.writeReg(MPR121_FDLF, 0x00);

 	i2c.writeReg(MPR121_NHDT, 0x00);
  	i2c.writeReg(MPR121_NCLT, 0x00);
  	i2c.writeReg(MPR121_FDLT, 0x00);

  	i2c.writeReg(MPR121_DEBOUNCE, 0);
  	i2c.writeReg(MPR121_CONFIG1, 0x10); #default, 16uA charge current
  	i2c.writeReg(MPR121_CONFIG2, 0x20); # 0.5uS encoding, 1ms period
  	i2c.writeReg(MPR121_ECR, 0x8F);
	return True;

def filteredData (t):
	if (t>12) :
 		return 0;
	return i2c.readWordReg(MPR121_FILTDATA_0L + t*2);


def baselineData (t) :
	if (t>12) :
		return 0;
	bl = i2c.readReg(MPR121_BASELINE_0 + t);
	return (bl << 2);

def touched ():
	t = i2c.readWordReg(MPR121_TOUCHSTATUS_L);
  	return t & 0x0FFF;






############  Touch recognition Program starts   ************

#remember the last pins touched so can know the buttons released
lasttouched = 0;
currtouched = 0;
print "Starting..."

if (begin()==False): 
    	print "TOuch Panel not found, check wiring?";
    	while True:
		a=1;

print "TOuch panel found!";




import sys

class Counter:
  count = 0
  start_time=0
  flag=0  # when flag is 1, readings are recorded
   
  touches=[];
  val_x_1=0;
  val_x_2=0;
  val_x_3=0;
  val_y_1=0;
  val_y_2=0;
  val_y_3=0;
  threshold_r=600;
  threshold_l=600;
  threshold_u=600;
  threshold_d=600;

c = Counter()

# inside a python interrupt you cannot use 'basic' types so you'll need to use
# objects


def test(gpio):
  #print "***********************************edge***********";
  if (c.flag==0):
    c.start_time=time.time();
    c.flag=1;
    c.touches=[];
    c.val_x_1=0;
    c.val_x_2=0;
    c.val_x_3=0;
    c.val_y_1=0;
    c.val_y_2=0;
    c.val_y_3=0;

  c.count+=1

  
  


pin = 46;
if (len(sys.argv) == 2):
  try:
    pin = int(sys.argv[1], 10)
  except ValueError:
    printf("Invalid pin " + sys.argv[1])
try:
	x = mraa.Gpio(pin)
	print("Starting ISR for pin " + repr(pin))
	x.dir(mraa.DIR_IN)
        
	x.isr(mraa.EDGE_BOTH, test, x)
	while (1):
	  a=22;
    	  k=touched();
          if (c.flag==1):
	    c.touches.append(k);
	    if (k==0) :
		c.flag=0;
		#print c.touches;
		if (len(c.touches)>10):
		  temp_list=c.touches;
		  l= len(temp_list);
#		  print c.touches[0:l/3];
#		  print c.touches[l/3:2*l/3];
#		  print c.touches[2*l/3:l];
 		  for i in temp_list[0:l/3]:	
	#	    print i;
    		    if ((i & 0b111) > 0 ) and ((i&0b111111000)==0 ):
  	              c.val_x_1+=(-3);
		    elif ((i & 0b111000) >0) and ((i & 0b111) >0) and ((i&0b111000000)==0) :
		      c.val_x_1+=(-2);
		    elif ((i & 0b111000000) >0) and ((i & 0b111000) >0) and ((i&0b111)==0):
		      c.val_x_1+=2;
		    elif ((i & 0b111000000) > 0 ) and ((i&0b111111)==0 ):	 
		      c.val_x_1+=3; 

		    if ((i & 0b100100001) > 0 ) and ((i&0b011011110)==0 ):
	              c.val_y_1+=(-3);
		    elif ((i & 0b100100001) >0) and ((i & 0b010001010) >0) and ((i&0b001010100)==0) :
		      c.val_y_1+=(-2);
		    elif ((i & 0b010001010) >0) and ((i & 0b001010100) >0) and ((i&0b100100001)==0):
		      c.val_y_1+=2;
		    elif ((i & 0b001010100) > 0 ) and ((i&0b110101011)==0 ):	 
		      c.val_y_1+=3; 

 		  for i in temp_list[l/3:2*l/3]:	
#		    print "**********************";
 #		    print i;
    		    if ((i & 0b111) > 0 ) and ((i&0b111111000)==0 ):
  	              c.val_x_2+=(-3);
		    elif ((i & 0b111000) >0) and ((i & 0b111) >0) and ((i&0b111000000)==0) :
		      c.val_x_2+=(-2);
		    elif ((i & 0b111000000) >0) and ((i & 0b111000) >0) and ((i&0b111)==0):
		      c.val_x_2+=2;
		    elif ((i & 0b111000000) > 0 ) and ((i&0b111111)==0 ):	 
		      c.val_x_2+=3; 

		    if ((i & 0b100100001) > 0 ) and ((i&0b011011110)==0 ):
	              c.val_y_2+=(-3);
		    elif ((i & 0b100100001) >0) and ((i & 0b010001010) >0) and ((i&0b001010100)==0) :
		      c.val_y_2+=(-2);
		    elif ((i & 0b010001010) >0) and ((i & 0b001010100) >0) and ((i&0b100100001)==0):
		      c.val_y_2+=2;
		    elif ((i & 0b001010100) > 0 ) and ((i&0b110101011)==0 ):	 
		      c.val_y_2+=3; 

 		  for i in temp_list[2*l/3:l]:	
#		    print "**********************";
 #		    print i;		
    		    if ((i & 0b111) > 0 ) and ((i&0b111111000)==0 ):
  	              c.val_x_3+=(-3);
		    elif ((i & 0b111000) >0) and ((i & 0b111) >0) and ((i&0b111000000)==0) :
		      c.val_x_3+=(-2);
		    elif ((i & 0b111000000) >0) and ((i & 0b111000) >0) and ((i&0b111)==0):
		      c.val_x_3+=2;
		    elif ((i & 0b111000000) > 0 ) and ((i&0b111111)==0 ):	 
		      c.val_x_3+=3; 

		    if ((i & 0b100100001) > 0 ) and ((i&0b011011110)==0 ):
	              c.val_y_3+=(-3);
		    elif ((i & 0b100100001) >0) and ((i & 0b010001010) >0) and ((i&0b001010100)==0) :
		      c.val_y_3+=(-2);
		    elif ((i & 0b010001010) >0) and ((i & 0b001010100) >0) and ((i&0b100100001)==0):
		      c.val_y_3+=2;
		    elif ((i & 0b001010100) > 0 ) and ((i&0b110101011)==0 ):	 
		      c.val_y_3+=3; 


		  print "l : " + str(l);
		  print "val_x_1 : " + str(c.val_x_1);
		  print "val_x_2 : " + str(c.val_x_2);
		  print "val_x_3 : " + str(c.val_x_3);
		  print "val_y_1 : " + str(c.val_y_1);
		  print "val_y_2 : " + str(c.val_y_2);
		  print "val_y_3 : " + str(c.val_y_3);
                  
		  right_dev = max((c.val_x_2-c.val_x_1),(c.val_x_3 - c.val_x_2));
		  left_dev= max((c.val_x_1-c.val_x_2),(c.val_x_2 - c.val_x_3));
		  up_dev = max((c.val_y_2-c.val_y_1),(c.val_y_3 - c.val_y_2));
		  down_dev= max((c.val_y_1-c.val_y_2),(c.val_y_2 - c.val_y_3));

		  print "right dev : " +str(right_dev);
		  print "left dev: " + str (left_dev);
		  print "up dev : " + str(up_dev);
		  print "down dev : " + str(down_dev);
		  
		  if (right_dev > left_dev) and (right_dev > up_dev) and (right_dev > down_dev) and (right_dev > c.threshold_r):
		    print "\n****************RIGHT*******************\n";

		  elif (left_dev > right_dev) and (left_dev > up_dev) and (left_dev > down_dev) and (left_dev > c.threshold_l):
		    print "\n****************LEFT*******************\n";

		  elif (up_dev > left_dev) and (up_dev > right_dev) and (up_dev > down_dev) and (up_dev > c.threshold_u):
		    print "\n****************UP*******************\n";

		  elif (down_dev > left_dev) and (down_dev > up_dev) and (down_dev > right_dev) and (down_dev > c.threshold_d):
		    print "\n****************DOWN*******************\n";
		  else :
		    print "\n****************TAP********************\n";

            
          #elif (c.flag==0):
            #print " Now the flag is 0 ";
        x.isrExit()
except ValueError as e:
    print(e)
