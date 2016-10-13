#include <stdio.h>
#include <stdlib.h> 
 #include <fcntl.h>
#include <sys/stat.h>
#include <linux/i2c-dev.h>
#include <sys/ioctl.h>
main(){
	//printf("Fdfas");
        //system("echo hello\n");
	int file;
	int adapter_nr =1;
	char filename[20];

	snprintf(filename,19,"/dev/i2c-%d",adapter_nr);
	file = open(filename , O_RDWR);
	if (file<0){
		printf ("error\n");
		exit(1);
	}

        int addr = 0x5a; /* The I2C address */

        if (ioctl(file, I2C_SLAVE, addr) < 0) {
        /* ERROR HANDLING; you can check errno to see what went wrong */
        printf("error");
        exit(1);
        }

        __u8 reg = 0x10; /* Device register to access */
 	 __s32 res;
  	char buf[10];

  	/* Using SMBus commands */
  	res = i2c_smbus_read_word_data(file, reg);
	  if (res < 0) {
  	  /* ERROR HANDLING: i2c transaction failed */
  	} else {
   	 /* res contains the read word */
  	}


	/* Using I2C Write, equivalent of 
     	i2c_smbus_write_word_data(file, reg, 0x6543) */
  	buf[0] = reg;
  	buf[1] = 0x43;
  	buf[2] = 0x65;
  	if (write(file, buf, 3) != 3) {
    	/* ERROR HANDLING: i2c transaction failed */
  	}

  	/* Using I2C Read, equivalent of i2c_smbus_read_byte(file) */
  	if (read(file, buf, 1) != 1) {
   	 /* ERROR HANDLING: i2c transaction failed */
  	} else {
   	 /* buf[0] contains the read byte */
  	}


        

}
