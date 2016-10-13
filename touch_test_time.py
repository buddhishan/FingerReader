
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
  stage=0; #there are time stages 1 and 2
  val_x_1=0;
  val_y_1=0;
  val_x_2=0;
  val_y_2=0;
  val_x_3=0;
  val_y_3=0;  
  stage_1_count=1; #each stage counts the no of touches to normalise, 1 to avoid zero division error
  stage_2_count=1;
  stage_3_count=1;

  sub_stage=0;
  stage_11_count=1;
  stage_12_count=1;
  stage_13_count=1;

  stage_21_count=1;
  stage_22_count=1;
  stage_23_count=1;

  stage_31_count=1;
  stage_32_count=1;
  stage_33_count=1;

  mean_x_1=0;
  mean_x_2=0;
  mean_x_3=0;
  mean_y_1=0;
  mean_y_2=0;
  mean_y_3=0;
  threshold_r=150;  # this is the value determining the senstitivity of the swipes, Change accordingly!
  threshold_l=150; 
  threshold_u=95;
  threshold_d=95;
  dtt=10; #double tap threshold


c = Counter()

# inside a python interrupt you cannot use 'basic' types so you'll need to use
# objects



  



def test(gpio):
  #print "***********************************edge***********";
  if (c.flag==0):
    c.start_time=time.time();
    c.flag=1;
    c.stage=1;
    c.stage_1_count=1;
    c.stage_2_count=1;
    c.stage_3_count=1;
    c.val_x_1=0;
    c.val_x_2=0;
    c.val_x_3=0;
    c.val_y_1=0;
    c.val_y_2=0;
    c.val_y_3=0;

    c.stage_11_count=0;
    c.stage_12_count=0;
    c.stage_13_count=0;
    c.stage_21_count=0;
    c.stage_22_count=0;
    c.stage_23_count=0;
    c.stage_31_count=0;
    c.stage_32_count=0;
    c.stage_33_count=0;


    
  print "....";
  #print c.start_time;
  #print("pin " + repr(gpio.getPin(True)) + " = " + repr(gpio.read()))
  c.count+=1
  #check();
  
  


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
    	  touched();
          time_elapsed=(time.time() - c.start_time);
	  if (time_elapsed>0.6):

            c.stage=0;
	    c.sub_stage=0;
	    c.mean_x_1 = c.val_x_1*100/c.stage_1_count;
	    c.mean_x_2 = c.val_x_2*100/c.stage_2_count;
	    c.mean_x_3 = c.val_x_3*100/c.stage_3_count;
	    c.mean_y_1 = c.val_y_1*100/c.stage_1_count;
	    c.mean_y_2 = c.val_y_2*100/c.stage_2_count;
	    c.mean_y_3 = c.val_y_3*100/c.stage_3_count;

	    if (c.flag==1):
	      print "x1 : " + str(c.mean_x_1);
	      print "x2 : " + str(c.mean_x_2);
	      print "x3 : " + str(c.mean_x_3);
	      print "y1 : " + str(c.mean_y_1);
              print "y2 : " + str(c.mean_y_2);
              print "y3 : " + str(c.mean_y_3);
	      print "stage-1-count :" +str(c.stage_1_count);
	      print "stage-2-count :" +str(c.stage_2_count);
	      print "stage-3-count :" +str(c.stage_3_count);
#	      print "\nstage-11-count :" +str(c.stage_11_count);
#	      print "stage-12-count :" +str(c.stage_12_count);
#	      print "stage-13-count :" +str(c.stage_13_count);	
#	      print "stage-21-count :" +str(c.stage_21_count);	
#	      print "stage-22-count :" +str(c.stage_22_count);	
#	      print "stage-23-count :" +str(c.stage_23_count);	
#	      print "stage-31-count :" +str(c.stage_31_count);	
#	      print "stage-32-count :" +str(c.stage_32_count);	
#	      print "stage-33-count :" +str(c.stage_33_count);	
	    
 	      if (((c.mean_x_2-c.mean_x_1)>c.threshold_r) and (c.mean_x_2!=0) and (c.mean_x_1!=0)) or (((c.mean_x_3-c.mean_x_2)>c.threshold_r) and (c.mean_x_2!=0) and (c.mean_x_3!=0)):
	        print "\n*********** RIGHT *******************\n";
		subprocess.call(['sh','/home/root/audio/play_right.sh']);

 	      elif (((c.mean_x_1-c.mean_x_2)>c.threshold_l) and (c.mean_x_2!=0) and (c.mean_x_1!=0)) or (((c.mean_x_2-c.mean_x_3)>c.threshold_l) and (c.mean_x_2!=0) and (c.mean_x_3!=0)):
	        print "\n*********** LEFT *******************\n";
		subprocess.call(['sh','/home/root/audio/play_left.sh']);

	      elif ((c.stage_11_count >c.dtt) or (c.stage_12_count >c.dtt)) and  ((c.stage_12_count <c.dtt) or (c.stage_13_count <c.dtt) or (c.stage_21_count <c.dtt) or (c.stage_22_count <c.dtt) or (c.stage_23_count <c.dtt) or (c.stage_31_count <c.dtt) or (c.stage_32_count <c.dtt)) and ((c.stage_32_count >c.dtt) or (c.stage_33_count >c.dtt)):
	        print "\n*********** DOUBLE TAP**************\n";
  		subprocess.call(['sh','/home/root/audio/play_double_tap.sh']);
	    
 	      elif (((c.mean_y_2-c.mean_y_1)>c.threshold_u) and (c.mean_y_2!=0) and (c.mean_y_1!=0)) or (((c.mean_y_3-c.mean_y_2)>c.threshold_u) and (c.mean_y_2!=0) and (c.mean_y_3!=0)):
	        print "\n*********** UP *******************\n";
		subprocess.call(['sh','/home/root/audio/play_up.sh']);

 	      elif (((c.mean_y_1-c.mean_y_2)>c.threshold_d) and (c.mean_y_2!=0) and (c.mean_y_1!=0)) or (((c.mean_y_2-c.mean_y_3)>c.threshold_d) and (c.mean_y_2!=0) and (c.mean_y_3!=0)):
	        print "\n*********** DOWN *******************\n";
		subprocess.call(['sh','/home/root/audio/play_down.sh']);

	      
	      elif (c.stage_1_count==1) and (c.stage_1_count==1):
		a=1;
	      else:
		print "\n*************TAP********************\n";
		subprocess.call(['sh','/home/root/audio/play_tap.sh']);

            c.flag=0;


	    
          
	  elif ((time_elapsed<0.6) and (time_elapsed>0.1)):
	    c.stage=3;
# 	    if (time_elapsed>0.1) and (time_elapsed<0.2) :
 #  	      c.sub_stage=31;
#	    elif (time_elapsed>0.2) and (time_elapsed <0.3):
#	      c.sub_stage=32;
#	    elif (time_elapsed >0.3) and (time_elapsed <0.5):
#	      c.sub_stage=33;		


          elif ((time_elapsed<0.1)and (time_elapsed>0.05)):
	    c.stage=2;
#	    if (time_elapsed>0.05) and (time_elapsed <0.065):
#             c.sub_stage=21;
#           elif (time_elapsed>0.065 ) and (time_elapsed <0.08):
 #	      c.sub_stage=22;
#	    elif (time_elapsed >0.08 ) and (time_elapsed <1):
#	      c.sub_stage=23;


          elif (time_elapsed<0.05):
	    c.stage=1;
#	    if (time_elapsed <0.01):
#	      c.sub_stage=11;
#	    elif (time_elapsed>0.01 ) and (time_elapsed <0.03) :
#	      c.sub_stage=12;
#	    elif (time_elapsed>0.03) and (time_elapsed <0.05):
#	      c.sub_stage=13;


  	  #print "flag  "+str(c.flag);
          
          if (c.flag==1):
	    i=touched();
	    #print i;
            if (c.stage==1):
		  if (i >0):
		    c.stage_1_count+=1;
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
	
		  	
	    elif (c.stage==2):
		  if (i >0):
		    c.stage_2_count+=1;
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
	
	    elif (c.stage==3):
		  if (i >0):
		    c.stage_3_count+=1;
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
	
#           if (i>0):
#	      if (c.sub_stage==11):
#	        c.stage_11_count+=1;
#	      elif (c.sub_stage==12):
#		c.stage_12_count+=1;
#	      elif (c.sub_stage==13):
#		c.stage_13_count+=1;
#	      elif (c.sub_stage==21):
#		c.stage_21_count+=1;
#	      elif (c.sub_stage==22):
#		c.stage_22_count+=1;
#	      elif (c.sub_stage==23):
#		c.stage_23_count+=1;
#	      elif (c.sub_stage==31):
#		c.stage_31_count+=1;
#	      elif (c.sub_stage==32):
#		c.stage_32_count+=1;
#	      elif (c.sub_stage==33):
#		c.stage_33_count+=1;
		


            
          #elif (c.flag==0):
            #print " Now the flag is 0 ";
        x.isrExit()
except ValueError as e:
    print(e)
