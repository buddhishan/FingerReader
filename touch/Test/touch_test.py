
import mraa;
import time;

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




#Program starts

#remember the last pins touched so can know the buttons released
lasttouched = 0;
currtouched = 0;
print "Starting..."

if (begin()==False): 
    	print "MPR121 not found, check wiring?";
    	while True:
		a=1;

	

print "MPR121 found!";

while True:
	#get the cuurntly touched pad
	currtouched = touched();
	for i in range(0,12):
		# it if *is* touched and *wasnt* touched before, alert!	
		if ( (currtouched & (1<<i)) and ((lasttouched & (1<<i))==False) ):
			print "Touched " +str(i);

		#if it *was* touched and now *isnt*, alert!
		if (((currtouched & (1<<i))==False) and (lasttouched & (1<<i)) ):
			print "Released " +str(i);

	lasttouched = currtouched;
  	

	
