
from machine import I2C
import time

class LCD:
    def __init__(self,i2c_addr = 0x27,backlight = True,scl=30,sda=31):

        #device constants
        self.I2C_ADDR = i2c_addr
        self.LCD_WIDTH = 16 # max. characters per line
        self.LCD_CHR = 1 #mode - sending data
        self.LCD_CMD = 0 #mode - sending command
        self.LCD_LINE_1 = 0x80 # lcd ram addr for line one
        self.LCD_LINE_2 = 0xC0 # lcd ram addr for line two

        if backlight:
            self.LCD_BACKLIGHT = 0x08 #lcd on

        else:
            self.LCD_BACKLIGHT = 0x00 #lcd off

        self.ENABLE = 0b00000100 # enable bit ， E RW RS 三个由高到低构成了控制位，所以enbale bit：0b00000100

        # Timing constants
        self.E_PULSE = 0.0001
        self.E_DELAY = 0.0001
        self.E_CYCLE = 0.0002
        self.i2c = I2C(I2C.I2C0, mode=I2C.MODE_MASTER,freq=100000, scl=scl, sda=sda)

        #initialise display
        self.lcd_byte(0x33,self.LCD_CMD) # 110011 initialise
        self.lcd_byte(0x32,self.LCD_CMD) # 110010 Initialise
        self.lcd_byte(0x06,self.LCD_CMD) # 000110 Cursor move direction
        self.lcd_byte(0x0C,self.LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
        self.lcd_byte(0x28,self.LCD_CMD) # 101000 Data length, number of lines, font size 4 line mode
        #self.lcd_byte(0x38,self.LCD_CMD) # 101000 Data length, number of lines, font size 8 line mode

        self.lcd_byte(0x01,self.LCD_CMD) # 000001 Clear display

    def lcd_byte(self,bits,mode):
        #send byte to data pins
        #bits = data
        #mode = 1 for data,0 for command


        ##four line mode:

        bits_high = mode | (bits & 0xF0) | self.LCD_BACKLIGHT
        bits_low = mode | (bits<<4 & 0xF0) | self.LCD_BACKLIGHT
        print(bits_high,'--',bits_low)

        #high bits
        self.i2c.writeto(self.I2C_ADDR,bytearray([bits_high]))
        self.toggle_enable(bits_high)

        #low bits
        self.i2c.writeto(self.I2C_ADDR,bytearray([bits_low]))
        self.toggle_enable(bits_low)




    def toggle_enable(self, bits):
        time.sleep(self.E_CYCLE)
        self.i2c.writeto(self.I2C_ADDR,bytearray([(bits | self.ENABLE)]))

        time.sleep(self.E_PULSE)
        self.i2c.writeto(self.I2C_ADDR,bytearray([(bits | ~self.ENABLE)]))

        time.sleep(self.E_DELAY)

    def message(self, string, line = 1, position = None):
       # display message string on LCD line 1 or 2
       if line == 1:
           lcd_line = self.LCD_LINE_1
       elif line == 2:
           lcd_line = self.LCD_LINE_2
       else:
           raise ValueError('line number must be 1 or 2')

       #print('string length :',len(string),string)

       # set where will String be displayed at
       self.lcd_byte(lcd_line, self.LCD_CMD)


       for i in range(len(string)):
           #print(string[i],':')
           self.lcd_byte(ord(string[i]), self.LCD_CHR)



    def clear(self):
        # clear LCD display
        self.lcd_byte(0x01, self.LCD_CMD)

    #scan i2c slave devices addr and print
    def i2c_scan(self):
        devices = self.i2c.scan()
        print(devices)


lcd = LCD(0x27,scl=30,sda=31)
lcd.i2c_scan()
lcd.clear()
lcd.message('123567890',1)
#lcd.message('BluejazzChn11',2)














