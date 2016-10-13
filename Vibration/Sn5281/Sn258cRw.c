#include <linux/videodev2.h>
#include <errno.h>
#include <sys/ioctl.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>


/*
 * Dynamic controls
 */

#define UVC_CTRL_DATA_TYPE_RAW		0
#define UVC_CTRL_DATA_TYPE_SIGNED	1
#define UVC_CTRL_DATA_TYPE_UNSIGNED	2
#define UVC_CTRL_DATA_TYPE_BOOLEAN	3
#define UVC_CTRL_DATA_TYPE_ENUM		4
#define UVC_CTRL_DATA_TYPE_BITMASK	5

/* ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */

#define V4L2_CID_BASE_EXTCTR_SONIX					0x0A0c4501
#define V4L2_CID_BASE_SONIX                       	V4L2_CID_BASE_EXTCTR_SONIX
#define V4L2_CID_ASIC_CTRL_SONIX                    V4L2_CID_BASE_SONIX+1
#define V4L2_CID_I2C_CTRL_SONIX						V4L2_CID_BASE_SONIX+2
#define V4L2_CID_SF_READ_SONIX                      V4L2_CID_BASE_SONIX+3
#define V4L2_CID_LAST_EXTCTR_SONIX					V4L2_CID_IMG_SETTING_SONIX

/* ---------------------------------------------------------------------------- */

#define UVC_GUID_SONIX_USER_HW_CONTROL       	{0x70, 0x33, 0xf0, 0x28, 0x11, 0x63, 0x2e, 0x4a, 0xba, 0x2c, 0x68, 0x90, 0xeb, 0x33, 0x40, 0x16}

// ----------------------------- XU Control Selector ------------------------------------
#define XU_SONIX_ASIC_CTRL 				0x01   // 与control 1 相对应
#define XU_SONIX_I2C_CTRL				0x02
#define XU_SONIX_SF_READ 				0x03

//#define XU_SONIX_H264_FMT  			0x06
//#define XU_SONIX_H264_QP   			0x07
//#define XU_SONIX_H264_BITRATE 		0x08
//#define XU_SONIX_FRAME_INFO  			0x06
//#define XU_SONIX_H264_CTRL   			0x07
//#define XU_SONIX_MJPG_CTRL		 		0x08
//#define XU_SONIX_OSD_CTRL	  			0x09
//#define XU_SONIX_MOTION_DETECTION		0x0A
//#define XU_SONIX_IMG_SETTING	 		0x0B

// ----------------------------- XU Control Selector ------------------------------------




#define UVC_CONTROL_SET_CUR	(1 << 0)
#define UVC_CONTROL_GET_CUR	(1 << 1)
#define UVC_CONTROL_GET_MIN	(1 << 2)
#define UVC_CONTROL_GET_MAX	(1 << 3)
#define UVC_CONTROL_GET_RES	(1 << 4)
#define UVC_CONTROL_GET_DEF	(1 << 5)
/* Control should be saved at suspend and restored at resume. */
#define UVC_CONTROL_RESTORE	(1 << 6)
/* Control can be updated by the camera. */
#define UVC_CONTROL_AUTO_UPDATE	(1 << 7)

#define UVC_CONTROL_GET_RANGE   (UVC_CONTROL_GET_CUR | UVC_CONTROL_GET_MIN | \
                                 UVC_CONTROL_GET_MAX | UVC_CONTROL_GET_RES | \
                                 UVC_CONTROL_GET_DEF)

struct uvc_xu_control_info {
    __u8 entity[16];
    __u8 index;
    __u8 selector;
    __u16 size;
    __u32 flags;
};

struct uvc_xu_control_mapping {
    __u32 id;
    __u8 name[32];
    __u8 entity[16];
    __u8 selector;

    __u8 size;
    __u8 offset;
    enum v4l2_ctrl_type v4l2_type;
    __u32 data_type;
};

struct uvc_xu_control {
    __u8 unit;
    __u8 selector;
    __u16 size;
    __u8 *data;
};

#define UVCIOC_CTRL_ADD		_IOW('U', 1, struct uvc_xu_control_info)
#define UVCIOC_CTRL_MAP		_IOWR('U', 2, struct uvc_xu_control_mapping)
#define UVCIOC_CTRL_GET		_IOWR('U', 3, struct uvc_xu_control)
#define UVCIOC_CTRL_SET		_IOW('U', 4, struct uvc_xu_control)

#define LENGTH_OF_SONIX_XU_CTR (3)
#define LENGTH_OF_SONIX_XU_MAP (3)

static struct uvc_xu_control_info sonix_xu_ctrls[] =
{
    {
        .entity   = UVC_GUID_SONIX_USER_HW_CONTROL,
        .selector = XU_SONIX_ASIC_CTRL,
        .index    = 0,
        .size     = 4,
        .flags    = UVC_CONTROL_SET_CUR | UVC_CONTROL_GET_MIN | UVC_CONTROL_GET_MAX |
                    UVC_CONTROL_GET_DEF | UVC_CONTROL_AUTO_UPDATE | UVC_CONTROL_GET_CUR
    },
    {
        .entity   = UVC_GUID_SONIX_USER_HW_CONTROL,
        .selector = XU_SONIX_I2C_CTRL,
        .index    = 1,
        .size     = 8,
        .flags    = UVC_CONTROL_SET_CUR | UVC_CONTROL_GET_CUR
    },
    {
        .entity   = UVC_GUID_SONIX_USER_HW_CONTROL,
        .selector = XU_SONIX_SF_READ,
        .index    = 2,
        .size     = 11,
        .flags    = UVC_CONTROL_SET_CUR | UVC_CONTROL_GET_CUR
    },

};

//  SONiX XU Ctrls Mapping
static struct uvc_xu_control_mapping sonix_xu_mappings[] =
{
    {
        .id        = V4L2_CID_ASIC_CTRL_SONIX,
        .name      = "SONiX: Asic Control",
        .entity    = UVC_GUID_SONIX_USER_HW_CONTROL,
        .selector  = XU_SONIX_ASIC_CTRL,
        .size      = 4,
        .offset    = 0,
        .v4l2_type = V4L2_CTRL_TYPE_INTEGER,
        .data_type = UVC_CTRL_DATA_TYPE_SIGNED
    },
    {
        .id        = V4L2_CID_I2C_CTRL_SONIX,
        .name      = "SONiX: I2C Control",
        .entity    = UVC_GUID_SONIX_USER_HW_CONTROL,
        .selector  = XU_SONIX_I2C_CTRL,
        .size      = 8,
        .offset    = 0,
        .v4l2_type = V4L2_CTRL_TYPE_INTEGER,
        .data_type = UVC_CTRL_DATA_TYPE_UNSIGNED
    },
    {
        .id        = V4L2_CID_SF_READ_SONIX,
        .name      = "SONiX: Serial Flash Read",
        .entity    = UVC_GUID_SONIX_USER_HW_CONTROL,
        .selector  = XU_SONIX_SF_READ,
        .size      = 11,
        .offset    = 0,
        .v4l2_type = V4L2_CTRL_TYPE_INTEGER,
        .data_type = UVC_CTRL_DATA_TYPE_UNSIGNED
    },


};

int XU_Init_Ctrl(int fd)
{
    int i=0;
    int err=0;
    /* try to add all controls listed above */
    for ( i=0; i<LENGTH_OF_SONIX_XU_CTR; i++ )
    {
        printf("Adding XU Ctrls - %s\n", sonix_xu_mappings[i].name);
        if ((err=ioctl(fd, UVCIOC_CTRL_ADD, &sonix_xu_ctrls[i])) < 0 )
        {
            if ((errno == EEXIST) || (errno != EACCES))
            {
                printf("UVCIOC_CTRL_ADD - Ignored, uvc driver had already defined\n");
                return (-EEXIST);
            }
            else if (errno == EACCES)
            {
                printf("Need admin previledges for adding extension unit(XU) controls\n");
                printf("please run 'SONiX_UVC_TestAP --add_ctrls' as root (or with sudo)\n");
                return  (-1);
            }
            else perror("Control exists");
        }
    }
    /* after adding the controls, add the mapping now */
    for ( i=0; i<LENGTH_OF_SONIX_XU_MAP; i++ )
    {
        printf("Mapping XU Ctrls - %s\n", sonix_xu_mappings[i].name);
        if ((err=ioctl(fd, UVCIOC_CTRL_MAP, &sonix_xu_mappings[i])) < 0)
        {
            if ((errno!=EEXIST) || (errno != EACCES))
            {
                printf("UVCIOC_CTRL_MAP - Error");
                return (-2);
            }
            else if (errno == EACCES)
            {
                printf("Need admin previledges for adding extension unit(XU) controls\n");
                printf("please run 'SONiX_UVC_TestAP --add_ctrls' as root (or with sudo)\n");
                return  (-1);
            }
            else perror("Mapping exists");
        }
    }
    return 0;
}
int XU_ASIC_Get_Data(int fd, int Addr, __u8 *uData)
{
    printf("XU_ASIC_Get_Data ==>\n");
    int i = 0;
    int ret = 0;
    int err = 0;
    __u8 ctrldata[4]={0};

    struct uvc_xu_control xctrl = {
            4,										/* bUnitID 				*/
            XU_SONIX_ASIC_CTRL,					   /* function selector	*/
            4,										/* data size			*/
            &ctrldata								/* *data				*/
        };

    // Switch command
    xctrl.data[0] = Addr & 0xFF;				// Tag
    xctrl.data[1] = (Addr & 0xFF00)>>8;
    xctrl.data[3] = 0xff;                       // Dummy

    if ((err=ioctl(fd, UVCIOC_CTRL_SET, &xctrl)) < 0)
    {
        printf("XU_ASIC_Get_Data ==> Switch cmd : ioctl(UVCIOC_CTRL_SET) FAILED (%i)11 == \n",err);
        if(err==EINVAL)
            printf("Invalid arguments\n");
        return err;
    }

    if ((err=ioctl(fd, UVCIOC_CTRL_GET, &xctrl)) < 0)
    {
        printf("XU_ASIC_Get_Data ==> ioctl(UVCIOC_CTRL_GET) FAILED (%i) == \n",err);
        if(err==EINVAL)
            printf("Invalid arguments\n");
        return err;
    }

    printf("   == XU_ASIC_Get_Data Success == \n");
    for(i=0; i<4; i++)
            printf("      Get data[%d] : 0x%x\n", i, xctrl.data[i]);
    *uData = xctrl.data[2];

    return ret;

}

int XU_ASIC_Set_Data(int fd, int Addr, __u8 uData)
{
    printf("XU_ASIC_Set_Data ==>\n");
    int ret = 0;
    int err = 0;
    __u8 ctrldata[4]={0};

    struct uvc_xu_control xctrl = {
            4,										/* bUnitID 				*/
            XU_SONIX_ASIC_CTRL,					   /* function selector	*/
            4,										/* data size			*/
            &ctrldata								/* *data				*/
        };

    // Switch command
    xctrl.data[0] = Addr & 0xFF;				// Tag
    xctrl.data[1] = (Addr & 0xFF00)>>8;
    xctrl.data[2] = uData;
    xctrl.data[3] = 0x0;                       // Dummy

    if ((err=ioctl(fd, UVCIOC_CTRL_SET, &xctrl)) < 0)
    {
        printf("XU_ASIC_Set_Data ==> Switch cmd : ioctl(UVCIOC_CTRL_SET) FAILED (%i)11 == \n",err);
        if(err==EINVAL)
            printf("Invalid arguments\n");
        return err;
    }

    printf("   == XU_ASIC_Set_Data Success == \n");
    return ret;

}

int XU_SF_Get_Data(int fd, int DataLen, int Addr, __u8 uData[])
{
    //printf("XU_SF_Get_Data ==>\n");
    int i = 0;
    int ret = 0;
    int err = 0;
    __u8 ctrldata[11]={0};
    //*Data = 0;

    struct uvc_xu_control xctrl = {
            4,										/* bUnitID 				*/
            XU_SONIX_SF_READ,					   /* function selector	*/
            11,										/* data size			*/
            &ctrldata								/* *data				*/
        };

    // Switch command
    xctrl.data[0] = Addr & 0xFF;				// Tag
    xctrl.data[1] = (Addr & 0xFF00)>>8;
    xctrl.data[2] = DataLen| 0x80;

    if ((err=ioctl(fd, UVCIOC_CTRL_SET, &xctrl)) < 0)
    {
        printf("XU_SF_Get_Data ==> Switch cmd : ioctl(UVCIOC_CTRL_SET) FAILED (%d)11 == \n",err);
        
        if(err==EINVAL)
            printf("Invalid arguments\n");
        return err;
    }
    if ((err=ioctl(fd, UVCIOC_CTRL_GET, &xctrl)) < 0)
    {
        printf("XU_I2C_Get_Data ==> ioctl(UVCIOC_CTRL_GET) FAILED (%i) == \n",err);
        if(err==EINVAL)
            printf("Invalid arguments\n");
        return err;
    }

    //printf("   == XU_SF_Get_Data Success == \n");
    i = 0;
    do{
        uData[i] = xctrl.data[i+3];
        DataLen --;
        i++;
    }while(DataLen != 0);


    //printf("XU_I2C_Get_Data (%x)<==\n", *Data);
    return ret;
}
int sf_read_8bytes(int dev, unsigned short addr, __u8 myData[])
{
    memset(myData, 0, 8);
    if(XU_SF_Get_Data(dev, 8, addr, myData) < 0)
    {
        printf("xu_sf_get_data error.\r\n");
        return -1;
    }
    return 0;
}

int SonixSFRead(int dev, unsigned short uStartAddr, __u8 uData[], long llength)
{
    int i;
    int count = llength/8;
    int last = llength%8;
    __u8 myData[8];
    __u8 lastData[last];
    int memaddr = uData;
    unsigned short addr = uStartAddr;
    for(i = 0; i < count; i++)
    {
        if(sf_read_8bytes(dev, addr, myData) < 0)
        {
            printf("sf_read_8bytes error.\r\n");
            return -1;
        }

        addr += 8;
        memcpy(memaddr, myData, 8);
        memaddr += 8;
    }
    if(last > 0)
    {
        if(XU_SF_Get_Data(dev, last, addr, lastData) < 0)
        {
            printf("xu_sf_get_data error.\r\n");
            return -1;
        }
        memcpy(memaddr, lastData, last);
    }

    return 0;
}

int XU_SF_Set_Data(int fd, int DataLen, int Addr, __u8 uData[])
{
    //printf("XU_SF_Set_Data ==>\n");
    int i = 0;
    int ret = 0;
    int err = 0;
    __u8 ctrldata[11]={0};
    //*Data = 0;

    struct uvc_xu_control xctrl = {
            4,										/* bUnitID 				*/
            XU_SONIX_SF_READ,					   /* function selector	*/
            11,										/* data size			*/
            &ctrldata								/* *data				*/
        };

    // Switch command
    xctrl.data[0] = Addr & 0xFF;				// Tag
    xctrl.data[1] = (Addr & 0xFF00)>>8;
    xctrl.data[2] = DataLen & 0x3F;

    for(i = 0; i < DataLen; i ++)
    {
        xctrl.data[i+3] = uData[i];
    }


    if ((err=ioctl(fd, UVCIOC_CTRL_SET, &xctrl)) < 0)
    {
        printf("XU_SF_Set_Data ==> Switch cmd : ioctl(UVCIOC_CTRL_SET) FAILED (%i)11 == \n",err);
        if(err==EINVAL)
            printf("Invalid arguments\n");
        return err;
    }

    //printf("   == XU_SF_Set_Data Success == \n");

    return ret;
}

int sf_write_8bytes(int dev, unsigned short addr, __u8 myData[])
{
    if(XU_SF_Set_Data(dev, 8, addr, myData) < 0)
    {
        printf("XU_SF_Set_Data error!\r\n");
        return -1;
    }

    return 0;

}

int SonixSFWrite(int dev, unsigned short uStartAddr, __u8 uData[], long llength)
{
    int i;
    int count = llength / 8;
    int last = llength % 8;
    __u8 myData[8];
    __u8 lastData[last];
    int memaddr = uData;
    unsigned short addr = uStartAddr;

    for(i = 0; i < count; i++)
    {
        memcpy(myData, memaddr, 8);
        memaddr += 8;
        if(sf_write_8bytes(dev, addr, myData) < 0)
        {
            printf("sf_write_8bytes error!\r\n");
            return -1;
        }

        addr += 8;
    }

    if(last > 0)
    {
        memcpy(lastData, memaddr, last);
        if(XU_SF_Set_Data(dev, last, addr, lastData) < 0)
        {
            printf("xu_sf_set_data error! \r\n");
            return -1;
        }

    }

    return 0;

}

int XU_SF_Erase_Data(int fd)
{
    int ret = 0;
    int err = 0;
    __u8 ctrldata[11]={0};
    //*Data = 0;

    struct uvc_xu_control xctrl = {
            4,										/* bUnitID 				*/
            XU_SONIX_SF_READ,					   /* function selector	*/
            11,										/* data size			*/
            &ctrldata								/* *data				*/
        };

    // Switch command
    //xctrl.data[0] = Addr & 0xFF;				// Tag
    //xctrl.data[1] = (Addr & 0xFF00)>>8;
    xctrl.data[2] = 0xC0;


    if ((err=ioctl(fd, UVCIOC_CTRL_SET, &xctrl)) < 0)
    {
        //printf("XU_SF_Erase_Data ==> Switch cmd : ioctl(UVCIOC_CTRL_SET) FAILED (%i)11 == \n",err);
       // if(err==EINVAL)
       //     printf("Invalid arguments\n");
       // return err;
    }


    return ret;
}

int Write_SF_From_File(int dev, const char *filename)
{
    //erase
    XU_SF_Erase_Data(dev);
    sleep(1);

    //write
    __u8 uWriteBuffer[65536];
    int wr_dev = open(filename, O_RDONLY);
    if(wr_dev < 0)
    {
        close(wr_dev);
        printf("Open 258c bin file error.\r\n");
        return -1;
    }
    ssize_t n_buffers = read(wr_dev, uWriteBuffer, 65536);
    close(wr_dev);

    if(n_buffers < 0)
    {
        printf("read() error.\r\n");
        return -1;
    }
    printf("Read %d bytes .\r\n", n_buffers);

    if(SonixSFWrite(dev, 0x0000, uWriteBuffer, 65536) < 0)
    {
        printf("SonixSFWrite error!\r\n");
        return -1;
    }


    return 0;
}

int Read_SF_To_File(int dev, const char *filename)
{
    __u8 uReadBuffer[65536];

    if(SonixSFRead(dev, 0x0000, uReadBuffer, 65536) < 0)
    {
        printf("SonixSFRead error.\r\n");
        return -1;
    }


    int Rd_dev = open(filename, O_RDWR | O_CREAT | O_TRUNC);

    if(Rd_dev < 0)
    {
        close(Rd_dev);
        printf("creat bin file error.\r\n");
        return -1;
    }

    ssize_t n_buffers = write(Rd_dev, uReadBuffer, 65536);
    if(n_buffers < 0)
    {
        printf("write() error.\r\n");
        return -1;
    }
    close(Rd_dev);

    printf("Write %d bytes to file\r\n", n_buffers);

    return 0;
}

int Verify_SF(int dev, const char *filename)
{
    printf("Verify...\r\n");
    __u8 uWriteBuffer[65536];
    int wr_dev = open(filename, O_RDONLY);
    if(wr_dev < 0)
    {
        close(wr_dev);
        printf("Open 258c bin file error.\r\n");
        return -1;
    }
    ssize_t n_buffers = read(wr_dev, uWriteBuffer, 65536);
    close(wr_dev);

    if(n_buffers < 0)
    {
        printf("read() error.\r\n");
        return -1;
    }
    //printf("Read %d bytes .\r\n", n_buffers);

    __u8 uReadBuffer[65536];

    if(SonixSFRead(dev, 0x0000, uReadBuffer, 65536) < 0)
    {
        printf("SonixSFRead error.\r\n");
        return -1;
    }

    if(strncmp(uWriteBuffer, uReadBuffer, 65536) != 0)
    {
        printf("Verify error!\r\n");
        return -1;
    }

    printf("Verify OK...\r\n");
    return 0;
}

int XU_I2C_Get_Data(int fd, int SlaveID, int DataLen, int Addr, __u8 uData[])
{
    //printf("XU_I2C_Get_Data ==>\n");
    int i = 0;
    int ret = 0;
    int err = 0;
    __u8 ctrldata[8]={0};

    struct uvc_xu_control xctrl = {
            4,										/* bUnitID 				*/
            XU_SONIX_I2C_CTRL,					/* function selector	*/
            8,										/* data size			*/
            &ctrldata								/* *data				*/
        };

    // Switch command
    xctrl.data[0] = SlaveID;				// Tag
    xctrl.data[1] = DataLen;
    xctrl.data[2] = Addr;
    xctrl.data[7] = 0xFF;

    if ((err=ioctl(fd, UVCIOC_CTRL_SET, &xctrl)) < 0)
    {
        printf("XU_I2C_Get_Data ==> Switch cmd : ioctl(UVCIOC_CTRL_SET) FAILED (%i) == \n",err);
        printf("errno=%d", errno);
        if(err==EINVAL)
            printf("Invalid arguments\n");
        return err;
    }

    memset(xctrl.data, 0, xctrl.size);
    if ((err=ioctl(fd, UVCIOC_CTRL_GET, &xctrl)) < 0)
    {
        printf("XU_I2C_Get_Data ==> ioctl(UVCIOC_CTRL_GET) FAILED (%i) == \n",err);
        if(err==EINVAL)
            printf("Invalid arguments\n");
        return err;
    }

    //printf("   == XU_I2C_Get_Data Success == \n");
    for(i=0; i<8; i++)
            printf("      Get data[%d] : 0x%x\n", i, xctrl.data[i]);

    //get Data
    i = 0;
    do{
        uData[i] = xctrl.data[i + 3];
        DataLen --;
        i++;
    }while(DataLen != 0);

    //printf("XU_I2C_Get_Data (%d)<==\n", *Data);
    return ret;
}

int XU_I2C_Set_Data(int fd, int SlaveID, int DataLen, int Addr, __u8 uData[])
{
    //printf("XU_I2C_Set_Data (%d) ==>\n", Data);
    int ret = 0;
    int err = 0;
    int i = 0;
    __u8 ctrldata[8]={0};

    struct uvc_xu_control xctrl = {
            4,										/* bUnitID 				*/
            XU_SONIX_I2C_CTRL,						/* function selector	*/
            8,										/* data size			*/
            &ctrldata								/* *data				*/
        };


    xctrl.data[0] = SlaveID;
    xctrl.data[1] = DataLen;
    xctrl.data[2] = Addr;
    xctrl.data[7] = 0;

    for(i = 0; i < DataLen; i ++)
    {
        xctrl.data[i+3] = uData[i];
    }

    if ((err=ioctl(fd, UVCIOC_CTRL_SET, &xctrl)) < 0)
    {
        printf("XU_I2C_Set_Data ==> Switch cmd : ioctl(UVCIOC_CTRL_SET) FAILED (%i) == \n",err);
        if(err==EINVAL)
            printf("Invalid arguments\n");
        return err;
    }


    //printf("XU_I2C_Set_Data <== Success \n");
    return ret;

}

int i2c_send_4bytes(int fd, int SlaveID, int Addr, __u8 myData[])
{
    if(XU_I2C_Set_Data(fd, SlaveID, 4, Addr, myData) < 0)
    {
        printf("XU_I2C_Set_Data error!\r\n");
        return -1;
    }

    return 0;
}


int i2c_recv_4bytes(int fd, int SlaveID, int Addr, __u8 myData[])
{
    memset(myData, 0, 4);

    if(XU_I2C_Get_Data(fd, SlaveID, 4, Addr, myData) < 0)
    {
        printf("XU_I2C_Get_Data error!\r\n");
        return -1;
    }
    return 0;
}

int SonixI2cSend(int fd, int SlaveID, int Addr, __u8 uData[], long llength)
{
    int i;
    int count = llength / 4;
    int last = llength % 4;
    __u8 myData[4];
    __u8 lastData[last];
    int memaddr = uData;

    for(i = 0; i < count; i++)
    {
        memcpy(myData, memaddr, 4);
        memaddr += 4;
        if(i2c_send_4bytes(fd, SlaveID, Addr, myData) < 0)
        {
            printf("sf_write_8bytes error!\r\n");
            return -1;
        }

    }

    if(last > 0)
    {
        memcpy(lastData, memaddr, last);
        if(XU_I2C_Set_Data(fd, SlaveID, last,  Addr, lastData) < 0)
        {
            printf("xu_i2c_set_data error! \r\n");
            return -1;
        }

    }

    return 0;
}

int SonixI2cRecv(int fd, int SlaveID, int Addr, __u8 uData[], long llength)
{
    int i;
    int count = llength/4;
    int last = llength%4;
    __u8 myData[4];
    __u8 lastData[last];
    int memaddr = uData;
    for(i = 0; i < count; i++)
    {
        if(i2c_recv_4bytes(fd, SlaveID, Addr, myData) < 0)
        {
            printf("i2c_recv_4bytes error.\r\n");
            return -1;
        }

        memcpy(memaddr, myData, 4);
        memaddr += 4;
    }
    if(last > 0)
    {
        if(XU_I2C_Get_Data(fd, SlaveID, last, Addr, lastData) < 0)
        {
            printf("XU_I2C_Get_Data error.\r\n");
            return -1;
        }
        memcpy(memaddr, lastData, last);
    }

    return 0;
}

//get device
int video_open(const char *devname)
{
    int dev = open(devname, O_RDWR );
    return dev;
}

int main(int argc, char *argv[])
{
    int dev;
    __u8 uData1[2];
    __u8 uData2[2];
    uData2[0] = 0x10;
    uData2[1] = 0x10;
    dev = video_open("/dev/video0");
    XU_Init_Ctrl(dev);
    //printf("initialized\n");

    //asic RW
#if 0
    //printf("if 0\n");
    XU_ASIC_Get_Data(dev, 0x1003, &uData1[0]);

    printf("udata0 = %x\r\n", uData1[0]);

    uData2 = uData1[0] & 0xFE;

    XU_ASIC_Set_Data(dev, 0x1003, uData2);
#endif

    //i2c RW
#if 1
    //printf("if 1\n");
    SonixI2cRecv(dev, 0x21, 0x0c, uData1, 1);
    SonixI2cSend(dev, 0x21, 0x0c, uData2, 2);
    printf("udata1 is %x\r\n", uData1[0]);
#endif

    //Flash RW
#if 0
    printf("start write flash...\r\n");
    if(Write_SF_From_File(dev, "SOURCE-AIO.SRC") < 0)
    {
        printf("write sf wrong!\r\n");
        return -1;
    }
    printf("write flash from file success.\r\n");

    if(Verify_SF(dev, "SOURCE-AIO.SRC") < 0)
    {
        return -1;
    }
#endif

#if 0
    printf("start read flash...\r\n");
    if(Read_SF_To_File(dev, "my_258c_new_tp.bin") < 0)
    {
        printf("read sf wrong!\r\n");
        return -1;
    }

    printf("read  flash to file success.\r\n");
#endif
    close(dev);
    return 0;
}
















