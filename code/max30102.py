from machine import I2C, Pin
# i2c = I2C(1, sda=Pin(0), scl=Pin(1),freq=400000)
from utime import sleep

I2C_ADDR = 0x57 
REG_INTR_STATUS_1 = 0x00
REG_INTR_STATUS_2 = 0x01
REG_INTR_Enable_1 = 0x02
REG_INTR_Enable_2 = 0x03

REG_FIFO_WR_PTR = 0x04
REG_OVF_COUNTER = 0x05
REG_FIFO_RD_PTR = 0x06
REG_FIFO_DATA = 0x07
REG_FIFO_CONFIG = 0x08

REG_MODE_CONFIG = 0x09
REG_SPO2_CONFIG = 0x0A

REG_LED1_PA = 0x0C
REG_LED2_PA = 0x0D

REG_PILOT_PA = 0x10
REG_MULTI_LED_CTRL1 = 0x11
REG_MULTI_LED_CTRL2 = 0x12

REG_TEMP_INTR = 0x1F
REG_TEMP_FRAC = 0x20
REG_TEMP_CONFIG = 0x21
REG_PROX_INT_THRESH = 0x30
REG_REV_ID = 0xFE
REG_PART_ID = 0xFF

class Max30102():
    def __init__(self,i2c,addr = I2C_ADDR):
        self.i2c = i2c
        self.address = addr
        self.reset()
        sleep(1)
        reg_data = self.i2c.readfrom_mem(self.address, REG_INTR_STATUS_1, 1)
        self.setup() 
    def reset(self):
        self.i2c.writeto_mem(self.address,REG_MODE_CONFIG,b'\x40')# 0100 0000
    def setup(self):
        # INTR setting
        # 0xc0 : A_FULL_EN and PPG_RDY_EN = 当fifo几乎满且新fifo数据就绪时，将触发中断
        self.i2c.writeto_mem(self.address,REG_INTR_Enable_1,b'\xc0') # 1100 0000
        self.i2c.writeto_mem(self.address,REG_INTR_Enable_2,b'\xc0') # 1100 0000

        # 清空寄存器数据
        # FIFO_WR_PTR[4:0]
        self.i2c.writeto_mem(self.address,REG_FIFO_WR_PTR,b'\x00') # 0000 0000
        # OVF_COUNTER[4:0]
        self.i2c.writeto_mem(self.address,REG_OVF_COUNTER,b'\x00') # 0000 0000
        # FIFO_RD_PTR[4:0]
        self.i2c.writeto_mem(self.address,REG_FIFO_RD_PTR,b'\x00') # 0000 0000

        # 0b 0100 1111
        # 样本平均 = 4 =>010, fifo rollover = false => 0 , FIFO_A_FULL = 0xF => 1111
        self.i2c.writeto_mem(self.address,REG_FIFO_CONFIG,b'\x4f') # 0100 1111

        # 0x02 为只读 , 0x03 为 SpO2 模式, 0x07 为 multi-mode LED
        self.i2c.writeto_mem(self.address,REG_MODE_CONFIG,b'\x03') # 0000 0011


        # 0b 0010 0111
        # SPO2_ADC 范围 = 4096nA =>01, SPO2 速率 = 100Hz =>001, LED pulse-width = 411uS =>11
        self.i2c.writeto_mem(self.address,REG_SPO2_CONFIG,b'\x27') # 0010 0111

        # 为 LED1 选择 ~7mA   
        self.i2c.writeto_mem(self.address,REG_LED1_PA,b'\x40') # 0100 0000
        # 为 LED2 选择 ~7mA
        self.i2c.writeto_mem(self.address,REG_LED2_PA,b'\x40') # 0100 0000
        # 为 Pilot LED 选择 ~25mA  
        self.i2c.writeto_mem(self.address,REG_PILOT_PA,b'\x7f') # 0111 1111
    def read_fifo(self):
        # 从寄存器中读取 1 个字节（值被丢弃）
        reg_INTR1 = self.i2c.readfrom_mem(self.address, REG_INTR_STATUS_1, 1)
        reg_INTR2 = self.i2c.readfrom_mem(self.address, REG_INTR_STATUS_2, 1)
        red_led = None
        ir_led = None

        # 从设备中读取 6 个字节的数据
        self.i2c.write(self.address, bytearray([REG_FIFO_DATA]))
        d = self.i2c.read(self.address, 6)
        # mask MSB [23:18]
        red_led = (d[0] << 16 | d[1] << 8 | d[2]) & 0x03FFFF #0011 1111 1111 1111 1111
        ir_led = (d[3] << 16 | d[4] << 8 | d[5]) & 0x03FFFF #0011 1111 1111 1111 1111
        return red_led, ir_led